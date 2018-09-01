from client import client
import discord


@client.message()
async def reeeePinged(message: discord.Message):
	if ("<@476143089598332929>" in message.content) and (not message.content.lower().startswith("<@476143089598332929>")):
		await message.add_reaction(discord.utils.find(lambda x: x.id == 476571656375238657, client.emojis))
		return