import config
import discord
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from discord.ext import commands 

intents = discord.Intents.all()
client = discord.Client(intents=intents)

sever_msg_id = 	782664853784756234
wl_msg_id = 782665043845840996
vanity_msg_id = 795488467190153236
pronoun_msg_id = 795491652017979472

def get_server(name, guild):
	role = None
	if name == EMOJIS[':red_square:']:
		role = discord.utils.get(guild.roles,name="NA")
	elif name == EMOJIS[':blue_square:']:
		role = discord.utils.get(guild.roles,name="EU")
	elif name == EMOJIS[':yellow_square:']:
		role = discord.utils.get(guild.roles,name="Asia")
	elif name == EMOJIS[':green_square:']:
		role = discord.utils.get(guild.roles,name="TW/HK/MO")
	
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

def get_vanity(name, guild):
	role = None 
	if name == "warhams":
		role =  discord.utils.get(guild.roles,id = 795486023793639464)
	elif name == "kaching":
		role =  discord.utils.get(guild.roles,id = 795486061509345290)
	elif name == "toys":
		role =  discord.utils.get(guild.roles,id = 795486103905763328)
	elif name == "bennet":
		role =  discord.utils.get(guild.roles,id = 795486180166336542)
	elif name == "cocogoat":
		role =  discord.utils.get(guild.roles,id = 795492459051614240)
	elif name == "booze":
		role =  discord.utils.get(guild.roles,id = 795493682031493132)
	elif name == "allears":
		role = discord.utils.get(guild.roles, id = 795793991684587600)
	elif name == "thunk":
		role = discord.utils.get(guild.roles, id = 796365047604707388)

	return role

def get_pronoun(name, guild):
	role = None 
	if name == "venteee":
		role = discord.utils.get(guild.roles,id = 802947991253549167)
	if name == "effort":
		role = discord.utils.get(guild.roles,id = 802947995955757098)
	if name == "lumided":
		role = discord.utils.get(guild.roles,id = 802947992780800022)

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
		role = None 
		
		if message_id == sever_msg_id:	
			print(str(member) + " added server reaction")	
			role = get_server(payload.emoji.name, guild)
		if message_id == wl_msg_id:
			print(str(member) + " added WL reaction")
			role = get_WL(payload.emoji.name, guild)		
		if message_id == vanity_msg_id:
			print(str(member) + " added vanity reaction")
			role = get_vanity(payload.emoji.name, guild)
		if message_id == pronoun_msg_id:
			print(str(member) + " added pronoun reaction")
			role = get_pronoun(payload.emoji.name, guild)
		 
		if role is not None: 
			if member is not None:
				await member.add_roles(role)
				print(str(member) + " added " + str(role))
			else: 
				print("member not found")
			

		
@client.event 
async def on_raw_reaction_remove(payload): 
	message_id = payload.message_id
	if message_id == sever_msg_id or wl_msg_id:
		guild = await client.fetch_guild(payload.guild_id)
		member = await guild.fetch_member(payload.user_id)
		role = None 
		
		if message_id == sever_msg_id:	
			print(str(member) + " removed server reaction")	
			role = get_server(payload.emoji.name, guild)
		if message_id == wl_msg_id:
			print(str(member) + " removed WL reaction")
			role = get_WL(payload.emoji.name, guild)
		if message_id == vanity_msg_id:
			print(str(member) + " removed vanity reaction")
			role = get_vanity(payload.emoji.name, guild)
		if message_id == pronoun_msg_id:
			print(str(member) + " removed pronoun reaction")
			role = get_pronoun(payload.emoji.name, guild)
			
		if role is not None: 
			if member is not None:
				await member.remove_roles(role)
				print(str(member) + " removed " + str(role))
			else: 
				print("member not found")
		
client.run(config.bot_key)