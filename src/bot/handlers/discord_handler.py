import discord
from discord.ext import commands
import asyncio
import sys
from src.bot.managers import TokenManager
from src.bot.commands import ChildBotCommands
from src.bot.channel_monitor import ChannelMonitor
from src.config import DEBUG_MODE


class DiscordConnectionHandler:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.dm_messages = True
        
        self.client = commands.Bot(command_prefix="c!", intents=intents)
        self.token_manager = TokenManager()
        self.max_retries = 5
        self.retry_count = 0
        self.commands_synced = False
        self.monitor = None
    
    async def setup(self):
        @self.client.event
        async def on_ready():
            if not self.commands_synced:
                try:
                    await self.client.tree.sync()
                    self.commands_synced = True
                    if DEBUG_MODE:
                        print(f"Bot logged in as {self.client.user}")
                        print("Commands synced with Discord")
                    
                    if not self.monitor:
                        self.monitor = ChannelMonitor(self.client)
                        self.client.loop.create_task(self.monitor.start_monitoring())
                        if DEBUG_MODE:
                            print("Channel monitor started")
                
                except Exception as e:
                    if DEBUG_MODE:
                        print(f"Failed to sync commands: {e}")
            elif DEBUG_MODE:
                print(f"Bot reconnected as {self.client.user}")
        
        @self.client.event
        async def on_error(event, *args, **kwargs):
            if DEBUG_MODE:
                print(f"Error in {event}: {sys.exc_info()}")
    
    def add_commands(self):
        child_commands = ChildBotCommands(self.client)
        asyncio.create_task(child_commands.register_commands())
    
    async def start_with_retry(self):
        self.retry_count = 0
        
        while True:
            try:
                token = self.token_manager.get_discord_token()
                
                if not token:
                    if DEBUG_MODE:
                        print("No token available, refreshing...")
                    if self.token_manager.refresh_discord_token():
                        token = self.token_manager.get_discord_token()
                    else:
                        await asyncio.sleep(5)
                        continue
                
                if DEBUG_MODE:
                    print("Attempting to connect to Discord...")
                
                await self.client.start(token)
            
            except discord.errors.LoginFailure as e:
                if DEBUG_MODE:
                    print(f"Login failed: {e}")
                
                if self.retry_count < self.max_retries:
                    self.retry_count += 1
                    if DEBUG_MODE:
                        print(f"Refreshing token (attempt {self.retry_count}/{self.max_retries})")
                    
                    if self.token_manager.refresh_discord_token():
                        await asyncio.sleep(2)
                        continue
                    else:
                        await asyncio.sleep(5)
                        continue
                else:
                    if DEBUG_MODE:
                        print("Max retries reached for token refresh")
                    await asyncio.sleep(10)
                    self.retry_count = 0
            
            except Exception as e:
                if DEBUG_MODE:
                    print(f"Error: {type(e).__name__}: {e}")
                await asyncio.sleep(5)
    
    async def run(self):
        self.add_commands()
        await self.start_with_retry()
