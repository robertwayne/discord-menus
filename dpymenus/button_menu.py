import asyncio
from typing import Dict, Optional, Union
from warnings import warn

from discord import Emoji, PartialEmoji, Reaction
from discord.abc import GuildChannel, User
from discord.ext.commands import Context

from dpymenus import BaseMenu
from dpymenus.constants import GENERIC_BUTTONS
from dpymenus.exceptions import ButtonsError, CallbackError


class ButtonMenu(BaseMenu):
    """
    Represents a button-based response menu.

    :param ctx: A reference to the command context.
    :param timeout: How long (in seconds) to wait before timing out.
    :param data: A dictionary containing variables to pass around menu functions.
    """

    def __init__(self, ctx: Context, timeout: int = 300, data: Optional[Dict] = None):
        super().__init__(ctx, timeout)
        self.data = data if data else {}

    def __repr__(self):
        return f'ButtonMenu(pages={[p.__str__() for p in self.pages]}, timeout={self.timeout}, ' \
               f'active={self.active} page={self.page_index}, data={self.data})'

    async def open(self):
        """The entry point to a new TextMenu instance; starts the main menu loop.
        Manages gathering user input, basic validation, sending messages, and cancellation requests."""
        await super()._validate_pages()
        await self._validate_buttons()

        if await self._start_session() is False:
            return

        self.output = await self.ctx.send(embed=self.page)

        while self.active:
            await self._add_buttons()

            self.input = await self._get_reaction()
            await self._cleanup_reactions()

            await self.page.on_next(self)

    # Internal Methods
    async def _add_buttons(self):
        """Adds reactions to the message object based on what was passed into the page buttons."""
        for button in self.page.buttons:
            await self.output.add_reaction(button)

    async def _get_reaction(self) -> Union[Emoji, str]:
        """Collects a user reaction and places it into the input attribute. Returns an Emoji or Emoji name."""
        try:
            reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=self.timeout,
                                                         check=self._check_reaction)

        except asyncio.TimeoutError:
            await self._timeout()

        else:
            if isinstance(reaction.emoji, (Emoji, PartialEmoji)):
                return reaction.emoji.name
            return reaction.emoji

    async def _cleanup_reactions(self):
        """Removes all reactions from the output message object."""
        if isinstance(self.ctx.channel, GuildChannel):
            await self.output.clear_reactions()

    def _check_reaction(self, r: Reaction, u: User) -> bool:
        """Returns true if the author is the person who reacted and the message ID's match. Checks the pages buttons."""
        if r.emoji in self.page.buttons:
            return u == self.ctx.author and r.message.id == self.output.id
        return False

    async def _validate_buttons(self):
        """Ensures that a button menu was passed the appropriate amount of buttons."""
        _cb_count = 0
        for page in self.pages:
            if page.buttons is None:
                break

            if page.on_next:
                _cb_count += 1

            if len(page.buttons) <= 1:
                raise ButtonsError('Any page with an `on_next` callback must have at least one button.')

            if len(page.buttons) > 5:
                warn('Adding more than 5 buttons to a page at once may result in discord.py throttling the bot client.')

        if self.page.on_fail:
            raise CallbackError('A ButtonMenu can not have an `on_fail` callback.')

        if _cb_count < len(self.pages) - 1:
            raise CallbackError(f'ButtonMenu missing `on_next` callbacks. Expected {len(self.pages) - 1}, found {_cb_count}.')

