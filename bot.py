import config
import discord
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from discord.ext import commands 

intents = discord.Intents.all()
client = discord.Client(intents=intents)

sever_msg_id = 	782664853784756234
wl_msg_id = 782665043845840996

def get_server(name, guild):
	role = None
	if name == EMOJIS[':red_square:']:
		role = discord.utils.get(guild.roles,name="NA")
	elif name == EMOJIS[':blue_square:']:
		role = discord.utils.get(guild.roles,name="EU")
	elif name == EMOJIS[':yellow_square:']:
		role = discord.utils.get(guild.roles,name="Asia")
	elif name == EMOJIS[':green_square:']:
		role = discord.utils.get(guild.roles,name="SAR")
	
	return role 
def get_WL(name, guild):
	role = None
	if name == EMOJIS[':one:']:
		role = discord.utils.get(guild.roles,name="WL1")
	elif name == EMOJIS[':two:']:
		role = discord.utils.get(guild.roles,name="WL2")
	elif name == EMOJIS[':three:']:
		role = discord.utils.get(guild.roles,name="WL3")
	elif name == EMOJIS[':four:']:
		role = discord.utils.get(guild.roles,name="WL4")
	elif name == EMOJIS[':five:']:
		role = discord.utils.get(guild.roles,name="WL5")
	elif name == EMOJIS[':six:']:
		role = discord.utils.get(guild.roles,name="WL6")
	elif name == EMOJIS[':seven:']:
		role = discord.utils.get(guild.roles,name="WL7")
	elif name == EMOJIS[':eight:']:
		role = discord.utils.get(guild.roles,name="WL8")
		
	return role
	
@client.event
async def on_ready():
	print("Katheryne Online") 

@client.event 
async def on_raw_reaction_add(payload): 
	message_id = payload.message_id
	if message_id == sever_msg_id or wl_msg_id:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
		member = payload.member
		
		if message_id == sever_msg_id:	
			print(str(member) + " added server reaction")	
			role = get_server(payload.emoji.name, guild)
		if message_id == wl_msg_id:
			print(str(member) + " added WL reaction")
			role = get_WL(payload.emoji.name, guild)
			
		if role is not None: 
			if member is not None:
				await member.add_roles(role)
				print("added " + str(role) + " to " + str(member))
			else: 
				print("member not found")
			

		
@client.event 
async def on_raw_reaction_remove(payload): 
	message_id = payload.message_id
	if message_id == sever_msg_id or wl_msg_id:
		guild = await client.fetch_guild(payload.guild_id)
		member = await guild.fetch_member(payload.user_id)
		
		if message_id == sever_msg_id:	
			print(str(member) + " removed server reaction")	
			role = get_server(payload.emoji.name, guild)
		if message_id == wl_msg_id:
			print(str(member) + " removed WL reaction")
			role = get_WL(payload.emoji.name, guild)
			
		if role is not None: 
			if member is not None:
				await member.remove_roles(role)
				print("removed " + str(role) + " from " + str(member))
			else: 
				print("member not found")
		
client.run(config.bot_key)