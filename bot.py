import config
import discord
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from discord.ext import commands 

intents = discord.Intents.all()
client = discord.Client(intents=intents)
 
async def server_roles_add(payload):
	guild_id = payload.guild_id
	guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
	role = None
	
	if payload.emoji.name == EMOJIS[':red_square:']:
		role = discord.utils.get(guild.roles,name="US")
	elif payload.emoji.name == EMOJIS[':blue_square:']:
		role = discord.utils.get(guild.roles,name="EU")
	elif payload.emoji.name == EMOJIS[':yellow_square:']:
		role = discord.utils.get(guild.roles,name="Asia")
	elif payload.emoji.name == EMOJIS[':purple_square:']:
		role = discord.utils.get(guild.roles,name="SAR")
		
	if role is not None: 
		member = payload.member
		print(member)
		if member is not None:
			print("added " + str(role) + " to " + str(member))
			await member.add_roles(role)
		else: 
			print("member not found")


async def server_roles_remove(payload):
	guild_id = payload.guild_id
	guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
	role = None
	
	if payload.emoji.name == EMOJIS[':red_square:']:
		role = discord.utils.get(guild.roles,name="US")
	elif payload.emoji.name == EMOJIS[':blue_square:']:
		role = discord.utils.get(guild.roles,name="EU")
	elif payload.emoji.name == EMOJIS[':yellow_square:']:
		role = discord.utils.get(guild.roles,name="Asia")
	elif payload.emoji.name == EMOJIS[':purple_square:']:
		role = discord.utils.get(guild.roles,name="SAR")
		
	if role is not None: 
		member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
		print(member)
		if member is not None:
			print("removed " + str(role) + " to " + str(member))
			await member.remove_roles(role)
		else: 
			print("member not found")
			

async def wl_roles_add(payload):
	guild_id = payload.guild_id
	guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
	role = None
	
	if payload.emoji.name == EMOJIS[':zero:']:
		role = discord.utils.get(guild.roles,name="WL0")
	elif payload.emoji.name == EMOJIS[':one:']:
		role = discord.utils.get(guild.roles,name="WL1")
	elif payload.emoji.name == EMOJIS[':two:']:
		role = discord.utils.get(guild.roles,name="WL2")
	elif payload.emoji.name == EMOJIS[':three:']:
		role = discord.utils.get(guild.roles,name="WL3")
	elif payload.emoji.name == EMOJIS[':four:']:
		role = discord.utils.get(guild.roles,name="WL4")
	elif payload.emoji.name == EMOJIS[':five:']:
		role = discord.utils.get(guild.roles,name="WL5")
	elif payload.emoji.name == EMOJIS[':six:']:
		role = discord.utils.get(guild.roles,name="WL6")
	elif payload.emoji.name == EMOJIS[':seven:']:
		role = discord.utils.get(guild.roles,name="WL7")
	elif payload.emoji.name == EMOJIS[':eight:']:
		role = discord.utils.get(guild.roles,name="WL8")

	if role is not None: 
		member = payload.member
		if member is not None:
			print("added " + str(role) + " to " + str(member))
			await member.add_roles(role)
		else: 
			print("member not found")
			
async def wl_roles_remove(payload):
	guild_id = payload.guild_id
	guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
	role = None
	
	if payload.emoji.name == EMOJIS[':one:']:
		role = discord.utils.get(guild.roles,name="WL1")
	elif payload.emoji.name == EMOJIS[':two:']:
		role = discord.utils.get(guild.roles,name="WL2")
	elif payload.emoji.name == EMOJIS[':three:']:
		role = discord.utils.get(guild.roles,name="WL3")
	elif payload.emoji.name == EMOJIS[':four:']:
		role = discord.utils.get(guild.roles,name="WL4")
	elif payload.emoji.name == EMOJIS[':five:']:
		role = discord.utils.get(guild.roles,name="WL5")
	elif payload.emoji.name == EMOJIS[':six:']:
		role = discord.utils.get(guild.roles,name="WL6")
	elif payload.emoji.name == EMOJIS[':seven:']:
		role = discord.utils.get(guild.roles,name="WL7")
	elif payload.emoji.name == EMOJIS[':eight:']:
		role = discord.utils.get(guild.roles,name="WL8")

	if role is not None: 
		member = payload.member
		if member is not None:
			print("removed " + str(role) + " from " + str(member))
			await member.remove_roles(role)
		else: 
			print("member not found")


@client.event
async def on_ready():
	print("Katheryne Online") 
	
@client.event 
async def on_raw_reaction_add(payload): 
	message_id = payload.message_id
	print("hello")
	if message_id == 782592330300915712:
		await server_roles_add(payload) 
	if message_id == 782592919021682708:
		await wl_roles_add(payload)
		
@client.event 
async def on_raw_reaction_remove(payload): 
	message_id = payload.message_id
	print("hello")
	if message_id == 782592330300915712:
		await server_roles_remove(payload) 
	if message_id == 782592919021682708:
		await wl_roles_remove(payload)
		
client.run(config.bot_key)