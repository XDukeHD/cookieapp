import discord
from discord import app_commands
from discord.ext import commands
from src.bot.device_identity import DeviceIdentity
from src.bot.managers import SessionManager
from src.bot.authentication import AuthenticationManager
from src.config import APP_VERSION, DEBUG_MODE
from src.actions import ActionLoader


class ChildBotCommands:
    def __init__(self, bot):
        self.bot = bot
        self.device_identity = DeviceIdentity()
        self.session = SessionManager()
        self.auth = AuthenticationManager()
        ActionLoader.load_actions()
    
    async def register_commands(self):
        @self.bot.tree.command(name="help", description="Show available commands")
        async def slash_help(interaction: discord.Interaction):
            await self._handle_help(interaction)
        
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
        
        @self.bot.tree.command(name="screenshot", description="Capture a screenshot")
        async def slash_screenshot(interaction: discord.Interaction):
            await self._handle_screenshot(interaction)
        
        @self.bot.command(name="help")
        async def prefix_help(ctx):
            await self._handle_help(ctx)
        
        @self.bot.command(name="login")
        async def prefix_login(ctx, device_name: str):
            await self._handle_login(ctx, device_name)
        
        @self.bot.command(name="whoami")
        async def prefix_whoami(ctx):
            await self._handle_whoami(ctx)
        
        @self.bot.command(name="logout")
        async def prefix_logout(ctx):
            await self._handle_logout(ctx)
        
        @self.bot.command(name="screenshot")
        async def prefix_screenshot(ctx):
            await self._handle_screenshot(ctx)
    
    async def _handle_help(self, context):
        if not await self.auth.enforce_authentication(context, 'help'):
            return
        
        device_name = self.device_identity.get_device_name()
        
        embed = discord.Embed(
            title="Available Commands",
            description=f"Device: **{device_name}**",
            color=discord.Color.blurple()
        )
        
        commands_list = [
            ("help", "Show this help message"),
            ("login [device_name]", "Login to this device"),
            ("whoami", "Show current session info"),
            ("logout", "Logout from this device"),
            ("screenshot", "Capture a screenshot")
        ]
        
        slash_commands = "\n".join([f"• `/{cmd}` - {desc}" for cmd, desc in commands_list])
        prefix_commands = "\n".join([f"• `c!{cmd}` - {desc}" for cmd, desc in commands_list])
        
        embed.add_field(name="Slash Commands", value=slash_commands, inline=False)
        embed.add_field(name="Prefix Commands (c!)", value=prefix_commands, inline=False)
        embed.set_footer(text=f"Version {APP_VERSION}")
        
        if isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    async def _handle_login(self, context, device_name: str):
        current_device = self.device_identity.get_device_name()
        
        if DEBUG_MODE:
            print(f"Login attempt: requested_device='{device_name}', current_device='{current_device}'")
        
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
        
        if DEBUG_MODE:
            print(f"User {user_name} logged in to device {device_name}")
        
        embed = discord.Embed(title="Login Successful", color=discord.Color.green())
        embed.add_field(name="Device", value=device_name, inline=False)
        embed.add_field(name="User", value=user_name, inline=False)
        
        if isinstance(context, discord.Interaction):
            await context.response.send_message(embed=embed, ephemeral=True)
        else:
            await context.send(embed=embed)
    
    async def _handle_screenshot(self, context):
        if not await self.auth.enforce_authentication(context, 'screenshot'):
            return
        
        await ActionLoader.execute_action('screenshot', context, trigger_type='command')
    
    async def _handle_whoami(self, context):
        if not await self.auth.enforce_authentication(context, 'whoami'):
            return
        
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
        if not await self.auth.enforce_authentication(context, 'logout'):
            return
        
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
