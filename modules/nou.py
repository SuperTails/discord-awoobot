from client import client
import discord


@client.message()
async def shutdown_nou(message: discord.Message):
	if message.content.lower().endswith("awoobot shut down"):
		await message.channel.send("no u")
	if message.content.lower() == "no u":
		await message.channel.send(f"this is so sad {message.author.mention} shut down")
	return
