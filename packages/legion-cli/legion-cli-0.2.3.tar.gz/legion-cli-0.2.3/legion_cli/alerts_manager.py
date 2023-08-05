from collections import namedtuple
from itertools import count
from pprint import pformat
from threading import Lock, Thread
from time import time, sleep
from traceback import format_exc
from typing import List, Optional, Callable, Set, Dict

from arrow import utcnow
from legion_utils import AlertMsg
from robotnikmq import Subscriber, Message
from robotnikmq.config import RobotnikConfig
from typeguard import typechecked

from legion_cli.log import log

TimestampedAlert = namedtuple('TimestampedAlert', ['received_ts', 'alert'])


@typechecked
class AlertsManager:
    def __init__(self,
                 alert_exchanges: List[str],
                 config: Optional[RobotnikConfig] = None,
                 on_new: Optional[Callable[[AlertMsg], None]] = None,
                 on_update: Optional[Callable[[AlertMsg], None]] = None,
                 on_expire: Optional[Callable[[AlertMsg], None]] = None,
                 num_alerts: Optional[int] = None,
                 expiry_interval: float = 0.5):
        self.robotnik_config = config
        self.alert_exchanges = alert_exchanges
        self.expiry_interval = expiry_interval
        self._expiry_thread = Thread(target=self._run_expiry_thread,
                                     args=(self.expiry_interval,), daemon=True)
        self._active: Dict[str, TimestampedAlert] = {}
        self._on_new = on_new if on_new else lambda a: None
        self._on_update = on_update if on_update else lambda a: None
        self._on_expire = on_expire if on_expire else lambda a: None
        self._alert_limit = num_alerts if num_alerts else float('inf')
        self._stopped = True
        self._update_lock = Lock()

    def fire_new(self, alert: AlertMsg) -> None:
        try:
            self._on_new(alert)
        except Exception:  # pylint: disable=W0703
            log.error(format_exc())

    def fire_update(self, alert: AlertMsg) -> None:
        try:
            self._on_update(alert)
        except Exception:  # pylint: disable=W0703
            log.error(format_exc())

    def fire_expire(self, alert: AlertMsg) -> None:
        try:
            self._on_expire(alert)
        except Exception:  # pylint: disable=W0703
            log.error(format_exc())

    def _run_expiry_thread(self, interval_seconds: float = 1.0) -> None:
        start_time = time()
        for i in count(start=0, step=1):  # pragma: no branch
            sleep(max(0, start_time + i * interval_seconds - time()))
            to_expire: Set[str] = set()
            expired: Set[AlertMsg] = set()
            with self._update_lock:
                for key, ts_alert in self._active.items():
                    if utcnow() >= ts_alert.received_ts.shift(seconds=ts_alert.alert.ttl):
                        to_expire.add(key)
                for key in to_expire:
                    expired.add(self._active[key].alert)
                    del self._active[key]
            for alert in expired:
                self.fire_expire(alert)
            if self._stopped:
                break

    def _on_msg(self, msg: Message) -> None:
        alert: Optional[AlertMsg] = None
        try:
            alert = AlertMsg.of(msg)
        except ValueError:
            log.warning(f'Non-alert message received by AlertManager: {pformat(msg.to_dict())}')
        if alert is not None:
            self._alert_limit -= 1
            with self._update_lock:
                is_update = alert.key in self._active
                self._active[alert.key] = TimestampedAlert(utcnow(), alert)
            if is_update:
                self.fire_update(alert)
            else:
                self.fire_new(alert)
        if self._alert_limit <= 0:
            self.stop()

    def start(self) -> None:
        sub = Subscriber(config=self.robotnik_config)
        for exchange in self.alert_exchanges:
            sub.bind(exchange, '#.warning')
            sub.bind(exchange, '#.error')
            sub.bind(exchange, '#.critical')
        self._stopped = False
        self._expiry_thread = Thread(target=self._run_expiry_thread,
                                     args=(self.expiry_interval,), daemon=True)
        self._expiry_thread.start()
        for msg in sub.consume(inactivity_timeout=1):
            if self._stopped:
                break
            if msg is not None:
                self._on_msg(msg)

    def stop(self) -> None:
        self._stopped = True
        self._expiry_thread.join()
