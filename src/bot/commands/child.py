import discord
from discord import app_commands
from discord.ext import commands
from src.bot.device_identity import DeviceIdentity
from src.bot.managers import SessionManager


class ChildBotCommands:
    def __init__(self, bot):
        self.bot = bot
        self.device_identity = DeviceIdentity()
        self.session = SessionManager()
    
    async def register_commands(self):
        @self.bot.tree.command(name="login", description="Login to this device")
        @app_commands.describe(device_name="The device name to login to")
        async def slash_login(interaction: discord.Interaction, device_name: str):
            await self._handle_login(interaction, device_name)
        
        @self.bot.tree.command(name="whoami", description="Show current session info")
        async def slash_whoami(interaction: discord.Interaction):
            await self._handle_whoami(interaction)
        
        @self.bot.tree.command(name="logout", description="Logout from this device")
        async def slash_logout(interaction: discord.Interaction):
            await self._handle_logout(interaction)
        
        @self.bot.command(name="login")
        async def prefix_login(ctx, device_name: str):
            await self._handle_login(ctx, device_name)
        
        @self.bot.command(name="whoami")
        async def prefix_whoami(ctx):
            await self._handle_whoami(ctx)
        
        @self.bot.command(name="logout")
        async def prefix_logout(ctx):
            await self._handle_logout(ctx)
    
    async def _handle_login(self, context, device_name: str):
        current_device = self.device_identity.get_device_name()
        
        if device_name != current_device:
            message = f"This device is '{current_device}'. Cannot login to '{device_name}'."
            
            if isinstance(context, discord.Interaction):
                await context.response.send_message(message, ephemeral=True)
            else:
                await context.send(message)
            return
        
        if self.session.get_current_device() and self.session.get_current_device() != device_name:
            self.session.logout()
        
        user_id = context.user.id if isinstance(context, discord.Interaction) else context.author.id
        user_name = context.user.name if isinstance(context, discord.Interaction) else context.author.name
        
        self.session.login(device_name, user_id)
        embed = discord.Embed(title="Login Successful", color=discord.Color.green())
        embed.add_field(name="Device", value=device_name, inline=False)
        embed.add_field(name="User", value=user_name, inline=False)
        
        if isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    async def _handle_whoami(self, context):
        if not self.session.is_logged_in():
            message = "You are not logged in. Use /login or c!login to login to this device."
            
            if isinstance(context, discord.Interaction):
                await context.response.send_message(message, ephemeral=True)
            else:
                await context.send(message)
            return
        
        current_device = self.session.get_current_device()
        user_name = context.user.name if isinstance(context, discord.Interaction) else context.author.name
        
        embed = discord.Embed(title="Current Session", color=discord.Color.blue())
        embed.add_field(name="Device", value=current_device, inline=False)
        embed.add_field(name="User", value=user_name, inline=False)
        
        if isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    async def _handle_logout(self, context):
        if not self.session.is_logged_in():
            message = "You are not logged in."
            
            if isinstance(context, discord.Interaction):
                await context.response.send_message(message, ephemeral=True)
            else:
                await context.send(message)
            return
        
        previous_device = self.session.get_current_device()
        self.session.logout()
        embed = discord.Embed(title="Logout Successful", color=discord.Color.orange())
        embed.add_field(name="Device", value=previous_device, inline=False)
        
        if isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
