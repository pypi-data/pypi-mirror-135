from threading import Lock
from typing import Optional, Dict, List, Any, Callable, TypeVar, Union, Generic

from funcy import first
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from typeguard import typechecked

from legion_cli.log import log

DetailedType = TypeVar('DetailedType')


@typechecked
class DetailElement(Generic[DetailedType]):
    def __init__(self, identifier: str, element: DetailedType, render_details: Callable[[DetailedType], Panel],
                 render_overview: Callable[[DetailedType], Panel], style: Optional[str] = None,
                 focus_style: Optional[str] = None):
        self._identifier = identifier
        self._element = element
        self._render_details = render_details
        self._render_overview = render_overview
        self._style = style or ''
        self._focus_style = focus_style or ''
        self._overview_panel = self.render_overview(style)
        self._detail_panel = self.render_details()

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value) -> None:
        self._style = value

    @property
    def focus_style(self) -> str:
        return self._focus_style

    @focus_style.setter
    def focus_style(self, value) -> None:
        self._focus_style = value

    @property
    def element(self) -> DetailedType:
        return self._element

    @element.setter
    def element(self, value: DetailedType) -> None:
        self._element = value
        self._overview_panel = self.render_overview()
        self._detail_panel = self.render_details()

    def render_details(self) -> Panel:
        self._detail_panel = self._render_details(self.element)
        return self._detail_panel

    def render_overview(self, style: Optional[str] = None) -> Panel:
        self._overview_panel = self._render_overview(self.element)
        if style is not None:
            self._overview_panel.style = style
        else:
            self._overview_panel.style = self.style
        return self._overview_panel

    @property
    def overview(self) -> Panel:
        return self._overview_panel

    def focus(self) -> None:
        log.debug(f'Focus -> {self.focus_style}')
        self._overview_panel.style = self.focus_style

    def unfocus(self) -> None:
        log.debug(f'Unfocus -> {self.style}')
        self._overview_panel.style = self.style


@typechecked
class DetailList(Generic[DetailedType]):
    def __init__(self, elements: Optional[List[DetailElement]] = None, title: Optional[str] = None,
                 ratio: int = 2, sort_key: Optional[Callable[[DetailedType], Any]] = None,
                 sort_reverse: bool = False):
        self._elements: Dict[str, DetailElement] = {}
        self._sort_key = (lambda e: sort_key(e.element)) if sort_key else (lambda e: e.element)
        self._sorted_elements: List[DetailElement] = []
        self._display = Layout()
        self._title = title
        self._list_grid = Table.grid(expand=True)
        self._list_panel = Panel(self._list_grid, title=self._title)
        self._list_layout = Layout(self._list_panel, name="list")
        self._details_layout = Layout(name="details", ratio=ratio, visible=False)
        self._display.split_row(self._list_layout, self._details_layout)
        self._focused_on: Optional[DetailElement] = None
        self._update_lock = Lock()
        self._sort_reverse = sort_reverse
        if elements:
            for element in elements:
                self.add_element(element)

    def _render_grid(self) -> None:
        self._list_grid = Table.grid(expand=True)
        for element in self._sorted_elements:
            self._list_grid.add_row(element.overview)
        self._list_panel = Panel(self._list_grid, title=self._title)
        self._list_layout.update(self._list_panel)

    def add_element(self, element: DetailElement) -> None:
        log.debug(f'Adding element: {repr(element)}')
        with self._update_lock:
            self._elements[element.identifier] = element
            self._sorted_elements = sorted(self._sorted_elements + [element], key=self._sort_key,
                                           reverse=self._sort_reverse)
            self._render_grid()

    def update_element(self, identifier: str, element: DetailedType) -> None:
        log.debug(f'Updating element {identifier}: {repr(element)}')
        with self._update_lock:
            self._elements[identifier].element = element
            self._sorted_elements = sorted(self._sorted_elements, key=self._sort_key,
                                           reverse=self._sort_reverse)
            self._focus_on(self._focused_on)
            self._render_grid()

    def update_style(self, identifier: str, style: str) -> None:
        with self._update_lock:
            self._elements[identifier].style = style
            self._render_grid()

    def update_focused_style(self, identifier: str, style: str) -> None:
        with self._update_lock:
            self._elements[identifier].focus_style = style
            self._focus_on(self._focused_on)
            self._render_grid()

    def element(self, element_or_identifier: Union[DetailedType, DetailElement, str]) -> Optional[DetailElement]:
        if isinstance(element_or_identifier, DetailElement):
            return element_or_identifier if element_or_identifier.identifier in self._elements else None
        if isinstance(element_or_identifier, str):
            return self._elements[element_or_identifier] if element_or_identifier in self._elements else None
        return first(e for e in self.elements if e.element is element_or_identifier)

    @property
    def elements(self) -> List[DetailElement]:
        return self._sorted_elements

    def remove_element(self, element_or_identifier: Union[DetailedType, DetailElement, str]) -> Optional[DetailElement]:
        log.debug(f'Removing element {element_or_identifier}')
        with self._update_lock:
            element = self.element(element_or_identifier)
            if element:
                del self._elements[element.identifier]
                self._sorted_elements.remove(element)
                self._render_grid()
                if self._focused_on is element:
                    self._focus_on(None)
                return element
            return element

    @property
    def display(self) -> Layout:
        return self._display

    def _set_details(self, element: Optional[DetailElement]) -> None:
        if element is None:
            self._details_layout.update('')
        else:
            self._details_layout.update(element.render_details())

    def _focus_on(self, element: Optional[DetailElement]) -> None:
        log.debug(f'Currently focused on {repr(self._focused_on)}')
        if self._focused_on is not None:
            self._focused_on.unfocus()
        self._focused_on = element
        if self._focused_on is None:
            self._details_layout.visible = False
        else:
            self._focused_on.focus()
            self._details_layout.visible = True
        self._set_details(self._focused_on)
        log.debug(f'Changed focus to {repr(self._focused_on)}')

    @property
    def focus(self) -> Optional[DetailElement]:
        return self._focused_on

    def move_focus_down(self) -> None:
        with self._update_lock:
            if self.elements:
                if self._focused_on is None:
                    self._focus_on(self.elements[0])
                else:
                    focus = self._sorted_elements.index(self._focused_on) + 1
                    self._focus_on(None if focus >= len(self.elements) else self._sorted_elements[focus])

    def move_focus_up(self) -> None:
        with self._update_lock:
            if self.elements:
                if self._focused_on is None:
                    self._focus_on(self.elements[-1])
                else:
                    focus = self.elements.index(self._focused_on) - 1
                    self._focus_on(None if focus < 0 else self.elements[focus])
