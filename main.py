import asyncio
import discord
import datetime
import time
import log
from collections import Counter
from typing import List
from key import token

client = discord.Client(status=discord.Status.dnd)

awoobis_role: int = 0  # actual ID removed
awoobis_server: int = 0  # actual ID removed
reeeeePinged_emoji: int = 0  # actual ID removed

accepted_phrases: List[str] = [
	"hail awoobis",
	"hail awoobis!",
]

other_roles = []
record = Counter()
last_count = {}
booted = False


@client.event
async def on_ready():
	global other_roles, record, last_count, booted
	other_roles = [x.id for x in client.get_guild(awoobis_server).roles if x.id != awoobis_role]
	every_msg_ever = []
	for ch in client.get_guild(awoobis_server).text_channels:
		every_msg_ever.extend(await ch.history(limit=None, reverse=True).flatten())
	every_msg_ever = sorted(every_msg_ever, key=lambda x: x.created_at)
	i = 0
	log.info(f"Now processing {len(every_msg_ever)} messages in the entire server...")
	for msg in every_msg_ever:
		i += 1
		if i % 5000 == 0:
			log.info(f"Processed {i} messages...")
		if msg.author.bot:
			continue
		if msg.created_at-last_count.get(msg.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(hours=6):
			if msg.content.lower() in accepted_phrases:
				last_count[msg.author.id] = msg.created_at
				record[msg.author.id] += 1
		else:
			continue
	booted = True
	await client.change_presence(status=discord.Status.online, activity=discord.Game(name="Hail Awoobis!"))
	log.info(f"Logged in as {client.user.name}#{client.user.discriminator} ({client.user.id})")


@client.event
async def on_message(message: discord.Message):
	# just log the message
	if not message.attachments:  # no attachments
		try:
			log.msg(f"[{message.guild.name} - {message.guild.id}] [#{message.channel.name} - {message.channel.id}] [message id: {message.id}] [{message.author.name}#{message.author.discriminator} - {message.author.id}] {message.author.display_name}: {message.system_content}")
		except AttributeError:
			log.msg(f"[DM] [message id: {message.id}] [{message.author.name}#{message.author.discriminator} - {message.author.id}] {message.system_content}")
	else:
		try:
			log.msg(f"[{message.guild.name} - {message.guild.id}] [#{message.channel.name} - {message.channel.id}] [message id: {message.id}] [{message.author.name}#{message.author.discriminator} - {message.author.id}] {message.author.display_name}: {message.system_content} {' '.join([x.url for x in message.attachments])}")
		except AttributeError:
			log.msg(f"[DM] [message id: {message.id}] [{message.author.name}#{message.author.discriminator} - {message.author.id}] {message.system_content} {' '.join([x.url for x in message.attachments])}")

	global record, last_count
	if message.author.bot or (not booted):
		return
	if message.content.lower() in accepted_phrases:
		if not [x for x in message.author.roles if not x.id == awoobis_server]:
			await message.author.add_roles(discord.utils.find(lambda x: x.id == awoobis_role, message.author.roles))
			await message.channel.send("Hail Awoobis! (You've been added to the `worshipers` role)")
			record[message.author.id] += 1
		else:
			if message.created_at-last_count.get(message.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(hours=6):
				record[message.author.id] += 1
				last_count[message.author.id] = message.created_at
			await message.channel.send(f"Hail Awoobis!")

	if message.content == f"<@{client.user.id}> uptime":
		await message.channel.send(f"**__Uptime:__**\n{time.perf_counter()-start_time:.2f} seconds,\nor {(time.perf_counter()-start_time)/3600:.3f} hours, \nor {(time.perf_counter()-start_time)/86400:.4f} days")
		return
	if message.content == f"<@{client.user.id}> count":
		await message.channel.send(f"You have hailed Awoobis {record[message.author.id]} times.")
		return
	if message.content == f"<@{client.user.id}> last_rec":
		await message.channel.send(last_count[message.author.id].__str__())
		return
	if message.content.startswith(f"<@{client.user.id}> top"):
		parts = message.content.split(" ")
		out = f"__Top {int(parts[2])} Hailers:__\n"
		for u, c in record.most_common(int(parts[2])):
			m = message.guild.get_member(u)
			if m is not None:
				out += f"{m.display_name}: {c} hails\n"
			if m is None:
				out += f"(user no longer in server): {c} hails\n"
		await message.channel.send(out)
		return
	if message.content.lower().endswith("awoobot shut down"):
		await message.channel.send("no u")
	if message.content.lower() == "no u":
		await message.channel.send(f"this is so sad {message.author.mention} shut down")
	if f"<@{client.user.id}>" in message.content:
		await message.add_reaction(discord.utils.find(lambda x: x.id == reeeeePinged_emoji, client.emojis))
		return

start_time = time.perf_counter()
client.run(token)
