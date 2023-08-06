"""
pyromod - A monkeypatcher add-on for Pyrogram
Copyright (C) 2020 Cezar H. <https://github.com/usernein>

This file is part of pyromod.

pyromod is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyromod is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyromod.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import functools

import pyrogram

from ..utils import patch, patchable

loop = asyncio.get_event_loop()


class BotMethodInvalid(pyrogram.errors.exceptions.bad_request_400.BotMethodInvalid):
    pass


class UserbotMethodInvalid(Exception):
    ID = "USER_METHOD_INVALID"
    MESSAGE = "This method cannot be used by User Accounts."


class ListenerCanceled(Exception):
    pass


pyrogram.errors.ListenerCanceled = ListenerCanceled


@patch(pyrogram.client.Client)
class Client:
    @patchable
    def __init__(self, *args, **kwargs):
        self.listening = {}
        self.using_mod = True

        self.old__init__(*args, **kwargs)

    @patchable
    async def listen(self, chat_id, filters=None, timeout=None):
        if type(chat_id) != int:
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        future = loop.create_future()
        future.add_done_callback(functools.partial(self.clear_listener, chat_id))
        self.listening.update({chat_id: {"future": future, "filters": filters}})
        return await asyncio.wait_for(future, timeout)

    @patchable
    async def ask(self, chat_id, text, filters=None, timeout=None, *args, **kwargs):
        request = await self.send_message(chat_id, text, *args, **kwargs)
        response = await self.listen(chat_id, filters, timeout)
        response.request = request
        return response

    @patchable
    async def listen_for_callback(
        self,
        chat_id: Union[int, str],
        filters: pyrogram.filters = None,
        timeout: int = None,
    ):
        if not (await self.get_me()).is_bot:
            raise UserMethodInvalid(
                f"[{UserMethodInvalid.ID}]: {UserMethodInvalid.MESSAGE}"
            )

        if type(chat_id) != int:
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        future = loop.create_future()
        future.add_done_callback(functools.partial(self.clear_listener, chat_id))
        self.listening.update(
            {
                chat_id: {
                    "future": future,
                    "filters": filters,
                    "type": "callback",
                }
            }
        )
        return await asyncio.wait_for(future, timeout)

    @patchable
    async def ask_for_callback(
        self,
        chat_id: Union[int, str],
        text: str,
        button_text: str,
        callback_data: str = "pyromod_listener",
        filters: pyrogram.filters = None,
        timeout: int = None,
        *args,
        **kwargs,
    ):
        keyboard = ikb([[(button_text, callback_data)]])
        request = await self.send_message(
            chat_id, text, reply_markup=keyboard, *args, **kwargs
        )
        response = await self.listen_for_callback(chat_id, filters, timeout)
        while response.data.strip() != callback_data:
            response = await self.listen_for_callback(chat_id, filters, timeout)
        response.request = request
        return response

    @patchable
    async def listen_inline_query(
        self, query: str, filters: pyrogram.filters = None, timeout: int = None
    ):
        if not (await self.get_me()).is_bot:
            raise UserMethodInvalid(
                f"[{UserMethodInvalid.ID}]: {UserMethodInvalid.MESSAGE}"
            )
        future = loop.create_future()
        future.add_done_callback(functools.partial(self.clear_listener, query))
        self.listening.update(
            {
                query: {
                    "future": future,
                    "filters": filters,
                    "type": "inline",
                }
            }
        )
        return await asyncio.wait_for(future, timeout)

    @patchable
    async def listen_user_status(
        self,
        user_id: Union[int, str],
        filters: pyrogram.filters = None,
        timeout: int = None,
    ):
        if (await self.get_me()).is_bot:
            raise BotMethodInvalid
        future = loop.create_future()
        future.add_done_callback(functools.partial(self.clear_listener, user_id))
        self.listening.update(
            {
                user_id: {
                    "future": future,
                    "filters": filters,
                    "type": "status",
                }
            }
        )
        return await asyncio.wait_for(future, timeout)

    @patchable
    def clear_listener(self, chat_id, future):
        if future == self.listening[chat_id]["future"]:
            self.listening.pop(chat_id, None)

    @patchable
    def cancel_listener(self, chat_id):
        listener = self.listening.get(chat_id)
        if not listener or listener["future"].done():
            return

        listener["future"].set_exception(ListenerCanceled())
        self.clear_listener(chat_id, listener["future"])


@patch(pyrogram.handlers.message_handler.MessageHandler)
class MessageHandler:
    @patchable
    def __init__(self, callback: callable, filters=None):
        self.user_callback = callback
        self.old__init__(self.resolve_listener, filters)

    @patchable
    async def resolve_listener(self, client, message, *args):
        listener = client.listening.get(message.chat.id)
        if listener and not listener["future"].done():
            listener["future"].set_result(message)
        else:
            if listener and listener["future"].done():
                client.clear_listener(message.chat.id, listener["future"])
            await self.user_callback(client, message, *args)

    @patchable
    async def check(self, client, update):
        listener = client.listening.get(update.chat.id)

        if listener and not listener["future"].done():
            return (
                await listener["filters"](client, update)
                if callable(listener["filters"])
                else True
            )

        return await self.filters(client, update) if callable(self.filters) else True


@patch(pyrogram.types.user_and_chats.chat.Chat)
class Chat(pyrogram.types.Chat):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, *args, **kwargs)

    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, **kwargs)

    @patchable
    def cancel_listener(self):
        return self._client.cancel_listener(self.id)


@patch(pyrogram.types.user_and_chats.user.User)
class User(pyrogram.types.User):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.id, *args, **kwargs)

    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.id, *args, **kwargs)

    @patchable
    def cancel_listener(self):
        return self._client.cancel_listener(self.id)
