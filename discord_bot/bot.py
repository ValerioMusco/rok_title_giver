from collections import deque
import threading

import discord
from discord.ext import commands

from custom_types import Title, Kingdom
from config import TITLE_TIMER_TIMEOUT
from discord_bot import title_timer

class Bot():

    # ----- PUBLIC ----- #
    def __init__(
        self,
        p_prefix: str,
        p_intents: bool = True,
    ):

        # -----  PRIVATE ----- #
        self.__m_intents: discord.Intents
        self.__m_prefix: str = p_prefix
        self.__m_scientist_queue: deque = deque()
        self.__m_architect_queue: deque = deque()
        self.__m_duke_queue: deque = deque()
        # self.__m_rok_instance: RokInstance = RokInstance()
        self.__m_scientist_timer: threading.Thread = threading.Thread(
            target=title_timer.timer_handler, args=(1, self.__m_scientist_queue, TITLE_TIMER_TIMEOUT)
        )
        self.__m_architect_timer: threading.Thread = threading.Thread(
            target=title_timer.timer_handler, args=(2, self.__m_architect_queue, TITLE_TIMER_TIMEOUT)
        )
        self.__m_duke_timer: threading.Thread = threading.Thread(
            target=title_timer.timer_handler, args=(3, self.__m_duke_queue, TITLE_TIMER_TIMEOUT)
        )

        # ----- PUBLIC ----- #
        self.bot: commands.bot

        self.__m_intents = discord.Intents.default()
        self.__m_intents.message_content = p_intents
        self.bot = commands.Bot(command_prefix=self.__m_prefix, intents=self.__m_intents, help_command=None)
        self.__m_scientist_timer.start()
        self.__m_architect_timer.start()
        self.__m_duke_timer.start()

    def run(self, p_token):
        self.bot.run(p_token)

    async def on_ready(self):
        print(f"{self.bot.user.name} is ready to give titles")

    async def title(self, ctx, *args):
        args = args[0]
        if len(args) != 4:
            return

        # Parse the command args into individual variable
        try:
            title: Title = Title.__getitem__(args[0].upper())
        except KeyError:
            await ctx.send(f"{args[0]} wasn't recognised as a title.")
            return

        try:
            kingdom: str = Kingdom.__getitem__(args[1].upper())
        except KeyError:
            await ctx.send(f"Kingdom {args[1]} wasn't recognised")
            return

        try:
            coord_x: int = int(args[2])
        except ValueError:
            await ctx.send(f"{args[2]} isn't a valid X coordinate value.")
            return

        try:
            coord_y: int = int(args[3])
        except ValueError:
            await ctx.send(f"{args[3]} isn't a valid Y coordinate value.")
            return

        user = ctx.author
        if (
            user in self.__m_scientist_queue or
            user in self.__m_architect_queue or
            user in self.__m_duke_queue
        ):
            cause: str = "You already requested "
            cause += "Scientist" if user in self.__m_scientist_queue else ""
            cause += "Architect" if user in self.__m_architect_queue else ""
            cause += "Duke" if user in self.__m_duke_queue else ""
            cause += " please use the command `/done` if you're done with your previous title then try again."
            await ctx.reply(cause)
            return

        position_in_queue: int
        match title:
            case Title.SCIENTIST:
                self.__m_scientist_queue.append(user)
                position_in_queue = len(self.__m_scientist_queue)
            case Title.ARCHITECT:
                self.__m_architect_queue.append(user)
                position_in_queue = len(self.__m_architect_queue)
            case Title.DUKE:
                self.__m_duke_queue.append(user)
                position_in_queue = len(self.__m_duke_queue)
            case _:
                await ctx.send("An unexpected error occured (0x00_01) report this to @MrConnare")
        await ctx.reply(f"You're in position {position_in_queue}")

    async def done(self, ctx):
        user = ctx.author

        try:
            if user == self.__m_scientist_queue[0]:
                self.__m_scientist_queue.popleft(0)
        except IndexError:
            pass
        finally:
            return
        try:
            if user == self.__m_architect_queue[0]:
                self.__m_architect_queue.popleft(0)
        except IndexError:
            pass
        finally:
            return
        try:
            if user == self.__m_duke_queue[0]:
                self.__m_duke_queue.popleft(0)
        except IndexError:
            pass
        finally:
            return
