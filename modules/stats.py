from client import client
import datetime
import discord
import time
import os

try:
	import psutil
except ModuleNotFoundError:
	has_psutil = False
else:
	has_psutil = True

cmd_name = "stats"

client.basic_help(title=cmd_name, desc=f"shows various running statistics of {client.bot_name}")

detailed_help = {
	"Usage": f"{client.default_prefix}{cmd_name}",
	"Arguments": "None",
	"Description": f"This command shows different available statistics of {client.bot_name}, including servers, uptime, and commands run.",
}

client.long_help(cmd=cmd_name, mapping=detailed_help)


@client.command(trigger=cmd_name,
				aliases=["statistics"])
async def stats(command: str, message: discord.Message):
	async with message.channel.typing():

		if has_psutil:
			self = psutil.Process()
			cpu_self = self.cpu_percent(interval=1)
			self_m_used = self.memory_info().rss
			m_raw = psutil.virtual_memory()
			m_total = m_raw.total
			m_available = m_raw.available
			m_used = m_total - m_available
			cpu = psutil.cpu_percent(interval=1, percpu=True)
			index = 0
			cpu_text = ""
			for v in cpu:
				cpu_text += f"**CPU {index}:** {v}%\n"
				index += 1

		embed = discord.Embed(title=f"{client.bot_name} stats", description=discord.Embed.Empty, color=0x404040)
		up = time.perf_counter()-client.first_execution
		embed = embed.add_field(name="Uptime", value=f"{up:.6f} seconds")
		embed = embed.add_field(name="Servers", value=len(client.guilds))
		embed = embed.add_field(name="Total commands run in all servers since last reboot", value=client.command_count, inline=False)
		mps = client.message_count/up
		msg_freq = up/client.message_count
		embed = embed.add_field(name="Total messages sent in all servers since last reboot", value=f"{client.message_count} ({mps:.4f}/sec)    ({msg_freq:.4f} sec/message)", inline=False)
		embed = embed.add_field(name="Messages in cache", value=f"{len(client._connection._messages)} ({client._connection.max_messages} max)")
		n_connected = len(client.voice_clients)
		n_playing = len([x for x in client.voice_clients if x.is_playing()])
		embed = embed.add_field(name="Connected voice chats", value=f"{n_connected} ({n_playing} playing)")
		embed = embed.add_field(name="Bot Process ID", value=os.getpid())
		if has_psutil:
			embed = embed.add_field(name="Process Memory Usage", value=f"{self_m_used/(1024*1024):.3f} MiB")
			embed = embed.add_field(name="Process CPU Usage (rel. to one core)", value=f"{cpu_self:.1f}%")
			embed = embed.add_field(name="System RAM Usage", value=f"{m_used/(1024*1024):.1f}/{m_total/(1024*1024):.1f} MiB ({(m_used/m_total)*100:.2f}%)")
			embed = embed.add_field(name="System CPU Usage", value=cpu_text, inline=False)

		embed = embed.set_footer(text=str(datetime.datetime.utcnow()))
	await message.channel.send(embed=embed)
	return
