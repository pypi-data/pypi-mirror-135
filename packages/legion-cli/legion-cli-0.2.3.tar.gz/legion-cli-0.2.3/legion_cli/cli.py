from contextlib import contextmanager
from functools import lru_cache
from multiprocessing import Process, Event as event
from multiprocessing.synchronize import Event
from os import get_terminal_size
from pathlib import Path
from traceback import print_exc
from typing import Optional, Callable, Tuple, Any, Iterable
from pprint import pformat

import click
from legion_utils import Priority
from robotnikmq import RobotnikConfig, Subscriber, Message
from termcolor import colored
from typeguard import typechecked

from legion_cli.tui.alerts_monitor import run_alerts_monitor_with_keyboard_input
from legion_cli.log import log_to_file


DEFAULT_CONFIG = Path.cwd() / 'config.yaml'
DEFAULT_LOGFILE = Path.home() / '.local' / 'share' / 'legion' / 'legion.log'


@contextmanager
def timeout_process(target=Callable, args=Tuple[Any], timeout: int = 10):
    proc = Process(target=target, args=args)
    proc.start()
    yield
    proc.terminate()
    proc.join(timeout=timeout)
    proc.kill()
    proc.join()


class MessagePrinter:
    def __init__(self,
                 msg_limit_received: Optional[Event] = None,
                 num_msgs: Optional[int] = None):
        self.msg_limit_received = msg_limit_received
        self.num_msgs = num_msgs

    @property
    def term_width(self) -> int:
        return get_terminal_size().columns

    def _priority_color(self, msg: Message) -> Optional[str]:
        if msg.contents['priority'] == 1:
            return 'blue'
        if msg.contents['priority'] == 2:
            return 'yellow'
        if msg.contents['priority'] == 3:
            return 'red'
        if msg.contents['priority'] == 4:
            return 'magenta'
        return None

    @lru_cache
    def _label(self, msg: Message) -> str:
        return f"{Priority(msg.contents['priority']).name}: {msg.timestamp.format()}"

    def _header(self, msg: Message) -> str:
        width = self.term_width
        untrimmed_header = f"{'=' * ((width - 2 - len(self._label(msg))) // 2 + 1)} {self._label(msg)} {'=' * ((width - 2 - len(self._label(msg))) // 2)}"
        return untrimmed_header[:width]

    def _route(self, msg: Message) -> str:
        width = self.term_width
        untrimmed_route = f"{'-' * ((width - 2 - len(msg.routing_key)) // 2 + 1)} {msg.routing_key} {'-' * ((width - 2 - len(msg.routing_key)) // 2)}"
        return untrimmed_route[:width]

    @typechecked
    def watch(self, msg: Message) -> None:
        print(colored(self._header(msg), self._priority_color(msg)))
        print(colored(self._route(msg), self._priority_color(msg)))
        print(colored(pformat(msg.contents), self._priority_color(msg)))
        print(colored('=' * self.term_width, self._priority_color(msg)))
        if self.num_msgs is not None:  # pragma: no cover
            self.num_msgs -= 1
            if self.num_msgs <= 0 and self.msg_limit_received is not None:
                self.msg_limit_received.set()


@typechecked
def _watch_process(exchanges: Optional[Iterable[str]] = None,
                   exchange_routes: Optional[Iterable[Tuple[str, str]]] = None,
                   alert_exchanges: Optional[Iterable[str]] = None,
                   done: Optional[Event] = None,
                   config: Optional[RobotnikConfig] = None,
                   num_msgs: Optional[int] = None):
    try:
        watcher = MessagePrinter(done, num_msgs)
        sub = Subscriber(config=config)
        if exchanges is not None:
            for exchange in exchanges:
                sub.bind(exchange)
        if exchange_routes is not None:
            for exchange, binding in exchange_routes:
                sub.bind(exchange, binding)
        if alert_exchanges is not None:
            for exchange in alert_exchanges:
                sub.bind(exchange, '#.warning')
                sub.bind(exchange, '#.error')
                sub.bind(exchange, '#.critical')
        sub.run(watcher.watch)
    except KeyboardInterrupt:
        pass
    except Exception:  # pylint: disable=W0703
        print_exc()
    finally:
        if done is not None:
            done.set()


@typechecked
def _watch(exchanges: Optional[Iterable[str]] = None,
           exchange_routes: Optional[Iterable[Tuple[str, str]]] = None,
           alert_exchanges: Optional[Iterable[str]] = None,
           msg_limit: Optional[int] = None,
           config: Optional[RobotnikConfig] = None):
    done = event()
    with timeout_process(target=_watch_process, args=(exchanges,
                                                      exchange_routes,
                                                      alert_exchanges,
                                                      done,
                                                      config,
                                                      msg_limit)):
        done.wait()


@click.group()
def cli():
    """A set of utilities for working with legion on the commandline"""


@cli.command()
@click.option('-e', '--exchange', 'exchanges', type=str, multiple=True, default=None,
              help='An exchange to subscribe to (uses the # binding key which returns all messages on the exchange). Can be used multiple times.')
@click.option('-r', '--exchange-route', 'exchange_routes', type=click.Tuple([str, str]), nargs=2,
              multiple=True, default=None,
              help='An exchange and routing key combination which allows us to filter messages on the exchange. Can be used multiple times. See https://www.rabbitmq.com/tutorials/tutorial-five-python.html for more information on routing keys.')
@click.option('-a', '--alerts', 'alert_exchanges', type=str, multiple=True, default=None,
              help='Monitor an exchange for all alerts (warning,error,critical). Equivalent to `-r <EXCHANGE> #.warning -r <EXCHANGE> #.error -r <EXCHANGE> #.critical`')
@click.option('-n', '--msg-limit', default=None, type=int,
              help='If set, this will cause the script to finish after a given number of messages '
                   'has been received.')
@typechecked
def watch(exchanges: Optional[Iterable[str]],
          exchange_routes: Optional[Iterable[Tuple[str, str]]],
          alert_exchanges: Optional[Iterable[str]],
          msg_limit: Optional[int]):
    """Given an exchange name, this utility will monitor all messages going through said
       exchange (subject to optional filters) and output them to STDOUT."""
    _watch(exchanges, exchange_routes, alert_exchanges, msg_limit)


@cli.command()
@click.option('-a', '--alerts', 'alert_exchanges', type=str, multiple=True, required=True,
              help='Monitor an exchange for all alerts (warning,error,critical). Equivalent to `-r <EXCHANGE> #.warning -r <EXCHANGE> #.error -r <EXCHANGE> #.critical`')
@typechecked
def monitor(alert_exchanges: Iterable[str]):
    """Given a series of exchanges, this command will display a TUI for monitoring alerts on those exchanges"""
    log_to_file(DEFAULT_LOGFILE)
    run_alerts_monitor_with_keyboard_input(list(alert_exchanges))
