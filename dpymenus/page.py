from typing import Callable, List, Optional, Union

from discord import Embed, Emoji, PartialEmoji

Callback = Optional[Callable]
ButtonList = List[Union[str, Emoji, PartialEmoji]]


class Page:
    """Represents a single page inside a menu.

    Attributes
        :embed: A discord Embed object. Used in place of utilizing the Page as an Embed object itself.
    """
    __slots__ = ('index', 'embed', '_buttons', '_on_next', '_on_fail', '_on_cancel', '_on_timeout')

    def __init__(self, embed: Embed):
        self.index: int = 0
        self.embed: Embed = embed
        self._buttons: ButtonList = []
        self._on_next: Callback = None
        self._on_fail: Callback = None
        self._on_cancel: Callback = None
        self._on_timeout: Callback = None

    def __repr__(self):
        return f"Page(title={self.embed.title} {''.join([f'{k}={v}' for k, v in self.__dict__.items()])})"

    def __str__(self):
        return f'Page {self.index} {self.embed.title}'

    def set_buttons(self, buttons: List) -> 'Page':
        """Generates reaction buttons when the page is displayed. Returns itself for fluent-style chaining."""
        self._buttons = buttons

        return self

    def on_next(self, func: Callable) -> 'Page':
        """Sets the function that will be called when the `next` event runs. Returns itself for fluent-style chaining."""
        self._on_next = func

        return self

    def on_fail(self, func: Callable) -> 'Page':
        """Sets the function that will be called when the `fail` event runs. Returns itself for fluent-style chaining."""
        self._on_fail = func

        return self

    def on_cancel(self, func: Callable) -> 'Page':
        """Sets the function that will be called when the `cancel` event runs. Returns itself for fluent-style chaining."""
        self._on_cancel = func

        return self

    def on_timeout(self, func: Callable) -> 'Page':
        """Sets the function that will be called when the `timeout` event runs. Returns itself for fluent-style chaining."""
        self._on_timeout = func

        return self
