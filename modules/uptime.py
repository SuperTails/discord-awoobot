from client import client
import discord
import time

cmd_name = "uptime"

client.basic_help(title=cmd_name, desc="Returns the current uptime of Awoobot, in seconds, hours, and days.")


@client.command(trigger=cmd_name, aliases=[])
async def uptime_cmd(command: str, message: discord.Message):
	await message.channel.send(f"**__Uptime:__**\n{time.perf_counter()-client.first_execution:.2f} seconds, or \n{(time.perf_counter()-client.first_execution)/3600:.3f} hours, or \n{(time.perf_counter()-client.first_execution)/86400:.4f} days")
	return
