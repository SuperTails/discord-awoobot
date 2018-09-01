from typing import Tuple, Union
from collections import Counter
from modules import _common
from client import client
import datetime
import discord
import log
import key

accepted_phrases = [
	"hail awoobis",
	"hail awoobis!",
	"hail lord awoobis",
	"hail lord awoobis!",
]

help_count = {
	"Usage": f"{client.default_prefix}count",
	"Arguments": "None",
	"Description": "Shows the number of hails you have made to Awoobis.",
}
client.long_help("count", help_count)
help_reps = {
	"Usage": f"{client.default_prefix}reps <int>",
	"Arguments": "`<int>` - number of top reputation members to show. Negative values can be entered to see worst reputation people.",
	"Description": "Shows the reputation scoreboard of people in the server, including top and bottom reputation members.",
}
client.long_help("reps", help_reps)
help_top = {
	"Usage": f"{client.default_prefix}top <int>",
	"Arguments": "`<int>` - number of top hailers to show.",
	"Description": "Shows the scoreboard of who has Hailed Awoobis the most times in the server. ",
}
client.long_help("top", help_top)

other_roles = []
record = Counter()
reputation = Counter()
last_count = {}
last_rep = {}


def get_rep(message: str, source: int) -> Union[Tuple[int, int], Tuple[None, None]]:
	if message.lower().startswith("-rep "):
		# decrement rep count
		target = _common.stripMentionsToID(message.lower().split(" ")[1])
		if target == source:
			return target, 0
		return target, -1

	if message.lower().startswith("+rep "):
		# increment rep count
		target = _common.stripMentionsToID(message.lower().split(" ")[1])
		if target == source:
			return target, 0
		return target, +1

	# if all else fails...
	return None, None


@client.ready()
async def ready_get_count():
	global other_roles, record, reputation, last_count, last_rep
	other_roles = [x.id for x in client.get_guild(key.awoobis_guild).roles if x.id != key.awoobis_worshiper_role]
	every_msg_ever = []
	for ch in client.get_guild(key.awoobis_guild).text_channels:
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
		try:
			target, drep = get_rep(msg.content, msg.author.id)  # "drep" = delta rep
		except:  # it's probably just some random text and not an id or mention
			continue
		if (target is None) or (drep is 0):
			pass
		else:
			if msg.created_at - last_rep.get(msg.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(seconds=key.rep_cooldown):
				if target not in [key.awoobis_id, key.awoobot_id]:
					reputation[target] += drep
					last_rep[msg.author.id] = msg.created_at
				if target in [key.awoobis_id, key.awoobot_id]:
					if drep == -1:
						continue
					reputation[target] += drep
					last_rep[msg.author.id] = msg.created_at

		if msg.created_at-last_count.get(msg.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(seconds=key.hail_cooldown):
			if msg.content.lower() in accepted_phrases:
				last_count[msg.author.id] = msg.created_at
				record[msg.author.id] += 1
		else:
			continue


@client.message()
async def hail_awoobis(message: discord.Message):
	if message.author.bot:
		return
	if message.content.lower() in accepted_phrases:
		if not [x for x in message.author.roles if not x.id == key.awoobis_worshiper_role]:
			await message.author.add_roles([x for x in message.guild.roles if x.id == key.awoobis_worshiper_role][0])
			await message.channel.send("Hail Awoobis! (You've been added to the `worshipers` role)")
			record[message.author.id] += 1
		else:
			if message.created_at-last_count.get(message.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(seconds=key.hail_cooldown):
				record[message.author.id] += 1
				last_count[message.author.id] = message.created_at
			await message.channel.send(f"Hail Awoobis!")

	try:
		target, drep = get_rep(message.content, message.author.id)  # "drep" = delta rep
	except:  # it's probably just some random text and not an id or mention
		return

	if target is None:
		pass
	else:
		if target not in [key.awoobis_id, key.awoobot_id]:
			if message.created_at - last_rep.get(message.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(seconds=key.rep_cooldown):
				reputation[target] += drep
				last_rep[message.author.id] = message.created_at
				try:
					await message.add_reaction("☑")
				except:  # if it doesn't work that's ok
					pass
		if target in [key.awoobis_id, key.awoobot_id]:
			if drep == -1:
				await message.add_reaction("❌")
				return
			if message.created_at - last_rep.get(message.author.id, datetime.datetime(2015, 5, 15, 0, 0, 0)) > datetime.timedelta(seconds=key.rep_cooldown):
				reputation[target] += drep
				last_rep[message.author.id] = message.created_at
			try:
				await message.add_reaction("☑")
			except:  # if it doesn't work that's ok
				pass
		if drep is 0:
			await message.channel.send(f"{message.author.mention}'s reputation: `{'+' if reputation[target] >= 0 else ''}{'-' if reputation[target] < 0 else ''}{abs(reputation[target]):03d} rep`")

	if message.content.startswith("<@476143089598332929> reps"):
		parts = message.content.split(" ")
		count = 10 if len(parts) < 3 else int(parts[2])

		if count >= 0:
			# top rep branch
			out = f"__Top {count} Reputation Members:__\n"
			for u, c in reputation.most_common(count):
				m = message.guild.get_member(u)
				if m is not None:
					out += f"`{'+' if c >= 0 else ''}{'-' if c < 0 else ''}{abs(c):03d} rep`: {m.display_name}\n"
				if m is None:
					out += f"`{'+' if c >= 0 else ''}{'-' if c < 0 else ''}{abs(c):03d} rep`: (user no longer in server)\n"
			await message.channel.send(out)

		if count < 0:
			count = abs(count)
			# bottom rep branch
			out = f"__Bottom {count} Reputation Members:__\n"
			for u, c in reputation.most_common()[::-1][:count]:
				m = message.guild.get_member(u)
				if m is not None:
					out += f"`{'+' if c >= 0 else ''}{'-' if c < 0 else ''}{abs(c):03d} rep`: {m.display_name}\n"
				if m is None:
					out += f"`{'+' if c >= 0 else ''}{'-' if c < 0 else ''}{abs(c):03d} rep`: (user no longer in server)\n"
			await message.channel.send(out)

	if message.content == "<@476143089598332929>":
		await message.channel.send(f"Hey there! I'm Awoobot, a bot created by ntoskrnl and written in Python to help people become followers of Awoobis.\nTo get the Worshipers role, all you have to do is say \"Hail Awoobis!\" and if you don't already have the role I'll give it to you.\nFor help on some of the commands within me, run `{client.default_prefix}help`.")
		return

	if message.content == "<@476143089598332929> count":
		await message.channel.send(f"You have hailed Awoobis {record[message.author.id]} times.")
		return

	if message.content == "<@476143089598332929> last_rec":
		await message.channel.send(last_count[message.author.id].__str__())
		return

	if message.content.startswith("<@476143089598332929> top"):
		parts = message.content.split(" ")
		out = f"__Top {int(parts[2])} Hailers:__\n"
		for u, c in record.most_common(int(parts[2])):
			m = message.guild.get_member(u)
			if m is not None:
				out += f"{c} hails: {m.display_name}\n"
			if m is None:
				out += f"{c} hails: (user no longer in server)\n"
		await message.channel.send(out)
		return

