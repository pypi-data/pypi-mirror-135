import json
import logging
import threading
from datetime import datetime

import pandas
from foreverbull_core.models.backtest import EngineConfig, Period, Result
from foreverbull_core.models.socket import Request, Response, SocketConfig
from foreverbull_core.socket.exceptions import SocketClosed, SocketTimeout
from foreverbull_core.socket.nanomsg import NanomsgSocket
from foreverbull_core.socket.router import MessageRouter

from .broker import Broker
from .engine import Engine
from .exceptions import BacktestNotRunning, ConfigError
from .feed import Feed


class Backtest(threading.Thread):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.configuration = SocketConfig(socket_type="replier")
        self.socket = NanomsgSocket(self.configuration)
        self.engine = Engine()
        self.feed = Feed(self.engine)
        self.broker = Broker(self.engine, self.feed)
        self.feed_configuration = self.feed.configuration
        self.broker_configuration = self.broker.configuration
        self.router = MessageRouter()
        self.router.add_route(self.known_assets, "known_assets")
        self.router.add_route(self.info, "info")
        self.router.add_route(self.engine.configure, "configure_backtest", EngineConfig)
        self.router.add_route(self.run_backtest, "run_backtest")
        self.router.add_route(self.run_new_day, "run_new_day")
        self.router.add_route(self.stop_backtest, "stop_backtest")
        self.router.add_route(self._backtest_result, "result")
        self.running = False
        self.session_running = False
        self.result = None
        self._stop_lock = threading.Lock()
        super(Backtest, self).__init__()

    def info(self) -> dict:
        return {
            "socket": self.configuration.dict(),
            "feed": {"socket": self.feed_configuration.dict()},
            "broker": {"socket": self.broker_configuration.dict()},
            "running": self.running,
        }

    def status(self) -> dict:
        return {
            "running": self.running,
            "session_running": self.session_running,
            "configured": self.engine.configured if self.engine else None,
            "day_completed": self.feed.day_completed if self.feed else None,
        }

    def _process_message(self) -> None:
        req_data = self.socket.recv()
        req = Request.load(req_data)
        self.logger.info(f"recieved request: {req.task}")
        rsp = self.router(req)
        self.logger.info(f"sending response for request: {req.task}")
        self.socket.send(rsp.dump())

    def _setup(self, threaded=True) -> None:
        if self.engine is None:
            self.engine = Engine()
        if not self.engine.configured:
            raise ConfigError("needs to be configured before run")
        if self.feed is None:
            self.feed = Feed(self.engine, self.feed_configuration)
        self.engine.set_callbacks(self.initialize, self.feed.handle_data, self.analyze)
        if self.broker is None:
            self.broker = Broker(self.engine, self.feed, self.broker_configuration)

        self.broker.start()

    def run(self):
        self.logger.info("backtest running")
        self.running = True
        while self.running:
            self.logger.debug("waiting for request..")
            try:
                self._process_message()
            except SocketTimeout:
                self.logger.debug("timeout.. did not recieve any request")
                pass
            except SocketClosed:
                return

    def known_assets(self) -> dict:
        return self.engine._get_all_assets()

    def run_backtest(self, threaded=True) -> None:
        self.logger.info("running backtest")
        self._setup(threaded=threaded)
        if threaded:
            self.engine.start()
            return {"status": "ok"}
        self.engine.run()

    def run_new_day(self) -> None:
        if not self.session_running:
            raise BacktestNotRunning("backtest is not running")
        self.feed.lock.set()  # TODO: Maybe change this variable name?

    def initialize(self, _) -> None:
        self.session_running = True

    def analyze(self, _, result: pandas.DataFrame) -> None:
        result.drop("positions", axis=1, inplace=True)
        result.drop("orders", axis=1, inplace=True)
        result.drop("transactions", axis=1, inplace=True)
        result_in_json = result.to_json(orient="records")
        self.result = json.loads(result_in_json)
        self._taredown()
        self.session_running = False

    def _backtest_result(self) -> dict:
        result = Result(periods=[])
        for period in self.result:
            period["period_open"] = datetime.fromtimestamp(period["period_open"] / 1000)
            period["period_close"] = datetime.fromtimestamp(period["period_close"] / 1000)
            period_result = Period(**period)
            result.periods.append(period_result)
        return result.dict()

    def _taredown(self) -> None:
        self._stop_lock.acquire()
        if self.engine and self.engine.is_alive():
            self.engine.stop()
            # self.engine.join()
            self.engine = None
        if self.broker and self.broker.is_alive():
            self.broker.stop()
            self.broker.join()
            self.broker = None
        if self.session_running:
            self.feed.stop()
        self._stop_lock.release()

    def stop_backtest(self) -> None:
        rsp = Response(task="stop_backtest")
        self.socket.send(rsp.dump())
        return self.stop()

    def stop(self) -> None:
        self._taredown()
        self.running = False
        self.socket.close()
        return
