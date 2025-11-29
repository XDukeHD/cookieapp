import asyncio
import discord
from src.config import GUILD_ID, CHANNEL_ID, DEBUG_MODE
from src.bot.device_identity import DeviceIdentity
from src.bot.message_parser import MessageParser
from src.actions import ActionLoader


class ChannelMonitor:
    def __init__(self, bot):
        self.bot = bot
        self.device_identity = DeviceIdentity()
        self.parser = MessageParser()
        self.poll_interval = 60
    
    async def start_monitoring(self):
        await self.bot.wait_until_ready()
        ActionLoader.load_actions()
        
        while True:
            try:
                await self._check_channel()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                if DEBUG_MODE:
                    print(f"Channel monitor error: {e}")
                await asyncio.sleep(5)
    
    async def _check_channel(self):
        try:
            guild = self.bot.get_guild(int(GUILD_ID))
            if not guild:
                if DEBUG_MODE:
                    print(f"Guild {GUILD_ID} not found")
                return
            
            channel = guild.get_channel(int(CHANNEL_ID))
            if not channel:
                if DEBUG_MODE:
                    print(f"Channel {CHANNEL_ID} not found in guild {GUILD_ID}")
                return
            
            async for message in channel.history(limit=100):
                if self.parser.is_bot_mentioned(self.bot.user.id, message):
                    await self._process_message(message)
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error checking channel: {e}")
    
    async def _process_message(self, message):
        try:
            payload = self.parser.parse_mention_format(message.content)
            
            if not payload:
                if DEBUG_MODE:
                    print(f"Invalid payload format in message: {message.content}")
                return
            
            device_id = payload['device_id']
            device_name = payload['device_name']
            action = payload['action']
            
            current_device_id = self.device_identity.get_device_id()
            current_device_name = self.device_identity.get_device_name()
            
            if device_id == current_device_id and device_name == current_device_name:
                if DEBUG_MODE:
                    print(f"Message for this device: device_id={device_id}, device_name={device_name}, action={action}")
                
                await self._execute_action(action, message)
            else:
                if DEBUG_MODE:
                    print(f"Message for different device: device_id={device_id}, device_name={device_name}")
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error processing message: {e}")
    
    async def _execute_action(self, action, message):
        if DEBUG_MODE:
            print(f"Executing action: {action}")
        
        await ActionLoader.execute_action(action, message, trigger_type='channel')
