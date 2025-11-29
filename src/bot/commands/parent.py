import discord
from discord import app_commands
from src.bot.device_identity import DeviceIdentity


class ParentBotCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="parent", description="Parent bot commands")
    
    @app_commands.command(name="help", description="Show help information")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Help", color=discord.Color.blue())
        embed.add_field(name="/login [device_name]", value="Login to a specific device", inline=False)
        embed.add_field(name="/whoami", value="Show current device info", inline=False)
        embed.add_field(name="/logout", value="Logout from device", inline=False)
        embed.add_field(name="/devices", value="List all available devices", inline=False)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="devices", description="List all available devices")
    async def list_devices(self, interaction: discord.Interaction):
        device_identity = DeviceIdentity()
        device_name = device_identity.get_device_name()
        embed = discord.Embed(title="Available Devices", color=discord.Color.green())
        embed.add_field(name="Device", value=device_name, inline=False)
        await interaction.response.send_message(embed=embed)
