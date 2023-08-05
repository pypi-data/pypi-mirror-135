from contextlib import contextmanager
from pprint import pformat
from threading import Lock, Thread
from time import sleep
from typing import List, Optional, Dict, Generator

from arrow.arrow import Arrow
from legion_utils import AlertMsg, Priority
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.status import Status
from rich.table import Table
from rich.text import Text
from robotnikmq import RobotnikConfig
from typeguard import typechecked

from legion_cli.alerts_manager import AlertsManager
from legion_cli.tui.detail_list import DetailList, DetailElement
from legion_cli.tui.keyboard import unbuffered_term, getkey, UP, DOWN


WARNING_STYLE = 'yellow'
WARNING_FOCUSED_STYLE = 'black on yellow'
ERROR_STYLE = 'red'
ERROR_FOCUSED_STYLE = 'black on red'
CRITICAL_STYLE = 'purple'
CRITICAL_FOCUSED_STYLE = 'white on purple'


@typechecked
def style_for(priority: Priority) -> str:
    if priority == Priority.WARNING:
        return WARNING_STYLE
    if priority == Priority.ERROR:
        return ERROR_STYLE
    if priority == Priority.CRITICAL:
        return CRITICAL_STYLE
    return ''


@typechecked
def focused_style_for(priority: Priority) -> str:
    if priority == Priority.WARNING:
        return WARNING_FOCUSED_STYLE
    if priority == Priority.ERROR:
        return ERROR_FOCUSED_STYLE
    if priority == Priority.CRITICAL:
        return CRITICAL_FOCUSED_STYLE
    return ''


@typechecked
class AlertDisplayHeader:
    def __init__(self, exchanges: List[str]):
        self.center_title = '\u2500\u2500[q]<[/q]' + '>\u2500[q]<[/q]'.join(exchanges) + '>\u2500\u2500'
        self._lock = Lock()
        self._num_warnings = 0
        self._num_errors = 0
        self._num_critical = 0
        self.display = Layout()
        self.update()

    @property
    def grid(self) -> Table:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", width=10)
        grid.add_column(justify="center")
        grid.add_column(justify="right", width=10)
        grid.add_row(Status('legion', spinner='circle', speed=0.5),
                     self.center_title, self.counter_title)
        return grid

    def update(self) -> None:
        self.display.update(Panel(self.grid, height=3))

    @property
    def counter_title(self) -> Text:
        return self.warning_title + '/' + self.error_title + '/' + self.critical_title

    @property
    def warning_title(self) -> Text:
        return Text(str(self._num_warnings), style=WARNING_STYLE)

    @property
    def error_title(self) -> Text:
        return Text(str(self._num_errors), style=ERROR_STYLE)

    @property
    def critical_title(self) -> Text:
        return Text(str(self._num_critical), style=CRITICAL_STYLE)

    def add_alert(self, priority: Priority) -> None:
        if priority == Priority.WARNING:
            self.add_warning()
        if priority == Priority.ERROR:
            self.add_error()
        if priority == Priority.CRITICAL:
            self.add_critical()

    def remove_alert(self, priority: Priority) -> None:
        if priority == Priority.WARNING:
            self.remove_warning()
        if priority == Priority.ERROR:
            self.remove_error()
        if priority == Priority.CRITICAL:
            self.remove_critical()

    def add_warning(self) -> None:
        with self._lock:
            self._num_warnings += 1
            self.update()

    def remove_warning(self) -> None:
        with self._lock:
            self._num_warnings -= 1
            self.update()

    def add_error(self) -> None:
        with self._lock:
            self._num_errors += 1
            self.update()

    def remove_error(self) -> None:
        with self._lock:
            self._num_errors -= 1
            self.update()

    def add_critical(self) -> None:
        with self._lock:
            self._num_critical += 1
            self.update()

    def remove_critical(self) -> None:
        with self._lock:
            self._num_critical -= 1
            self.update()


@typechecked
class AlertsMonitor:
    def __init__(self,
                 alert_exchanges: List[str],
                 config: Optional[RobotnikConfig] = None):
        self._first_seen: Dict[str, Arrow] = {}
        self._first_seen_lock = Lock()
        self.detail_list = DetailList[AlertMsg](title='ALERTS',
                                                sort_key=lambda a: (-a.priority,
                                                                    self.first_seen(a.key)))
        self.alerts_manager = AlertsManager(alert_exchanges, config,
                                            on_new=self._new_alert,
                                            on_update=self._update_alert,
                                            on_expire=self._remove_alert)
        self.alerts_header = AlertDisplayHeader(alert_exchanges)
        self._main_layout = Layout(name='main')
        self._main_layout.split_column(Layout(self.alerts_header.display, name='header', height=3, size=3),
                                       self.detail_list.display)

    @property
    def display(self) -> Layout:
        return self._main_layout

    def first_seen(self, key: str) -> Arrow:
        with self._first_seen_lock:
            return self._first_seen[key]

    def element_of(self, alert: AlertMsg) -> DetailElement:
        return DetailElement(identifier=alert.key,
                             element=alert,
                             render_details=AlertsMonitor.details_of,
                             render_overview=self.overview_of,
                             style=style_for(alert.priority),
                             focus_style=focused_style_for(alert.priority))

    def overview_of(self, alert: AlertMsg) -> Panel:
        return Panel(Text(f'Condition Start: {self.first_seen(alert.key).format()}\n{alert.description}'),
                     height=5, title=alert.key.replace('[', '[q][[/q]'))

    @staticmethod
    def details_of(alert: AlertMsg) -> Panel:
        # TODO: Alert contents should be displayed as a tree
        return Panel(Text(pformat(alert.contents)),
                     title=f"{Priority(alert.priority).name}: {alert.msg.timestamp.format()}")

    def _new_alert(self, alert: AlertMsg) -> None:
        with self._first_seen_lock:
            self._first_seen[alert.key] = alert.msg.timestamp
        self.detail_list.add_element(self.element_of(alert))
        self.alerts_header.add_alert(alert.priority)

    def _remove_alert(self, alert: AlertMsg) -> None:
        with self._first_seen_lock:
            del self._first_seen[alert.key]
        self.detail_list.remove_element(alert.key)
        self.alerts_header.remove_alert(alert.priority)

    def _update_alert(self, alert: AlertMsg) -> None:
        # TODO: provide the previous version of the alert along with the new version
        self.detail_list.update_element(alert.key, alert)
        self.detail_list.update_style(alert.key, style_for(alert.priority))
        self.detail_list.update_focused_style(alert.key, focused_style_for(alert.priority))

    @contextmanager
    def run_manager(self):
        am_thread = Thread(target=self.alerts_manager.start)
        am_thread.start()
        try:
            yield
        finally:
            self.alerts_manager.stop()
            am_thread.join()

    def move_focus_up(self) -> None:
        self.detail_list.move_focus_up()

    def move_focus_down(self) -> None:
        self.detail_list.move_focus_down()


def run_alerts_monitor_with_keyboard_input(alert_exchanges: List[str],
                                           config: Optional[RobotnikConfig] = None,
                                           refresh_per_second: int = 4):
    monitor = AlertsMonitor(alert_exchanges, config)
    with unbuffered_term():
        with Live(monitor.display, refresh_per_second=refresh_per_second, screen=True):
            with monitor.run_manager():
                while 42:
                    sleep(0.1)
                    input_char = getkey()
                    if input_char is not None:
                        if input_char == UP:
                            monitor.move_focus_up()
                        if input_char == DOWN:
                            monitor.move_focus_down()
                        if input_char == "q":
                            break
