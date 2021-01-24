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

servers = {
	EMOJIS[':red_square:']    : "NA",
	EMOJIS[':blue_square:']   : "EU",
	EMOJIS[':yellow_square:'] : "Asia",
	EMOJIS[':green_square:']  : "TW/HK/MO"
}

WL = {
	EMOJIS[':one:']   : "WL1",
	EMOJIS[':two:']   : "WL2",
	EMOJIS[':three:'] : "WL3",
	EMOJIS[':four:']  : "WL4",
	EMOJIS[':five:']  : "WL5",
	EMOJIS[':six:']   : "WL6",
	EMOJIS[':seven:'] : "WL7",
	EMOJIS[':eight:'] : "WL8"
}

vanity = {
	"warhams" : 795486023793639464,
	"kaching" : 795486061509345290,
	"toys"    : 795486103905763328,
	"bennet"  : 795486180166336542,
	"cocogoat": 795492459051614240,
	"booze"   : 795493682031493132,
	"allears" : 795793991684587600,
	"thunk"   : 796365047604707388,
	"broke"   : 802948687508668456	
}

pronouns = {
	"venteee" : 802947991253549167,
	"lazy"    : 802947995955757098,
	"lumided" : 802947992780800022

}
def get_server(name, guild):
	if name in servers.keys():
		return discord.utils.get(guild.roles,name=servers[name]), "server reaction" 
	
	return None, "invalid server reaction" 

def get_WL(name, guild):
	if name in WL.keys():
		return discord.utils.get(guild.roles,name=WL[name]), "WL reaction"
		
	return None, "Invalid WL reaction"

def get_vanity(name, guild):
	if name in vanity.keys():
		return discord.utils.get(guild.roles,id=vanity[name]), "vanity reaction"

	return None, "invalid vanity reaction"

def get_pronoun(name, guild):
	if name in pronouns.keys():
		return discord.utils.get(guild.roles,id=pronouns[name]), "pronoun reaction"

	return None, "invalid pronoun reaction"
	
reaction_categories = {
	sever_msg_id : get_server,
	wl_msg_id : get_WL,
	vanity_msg_id : get_vanity,
	pronoun_msg_id : get_pronoun
}


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
		member_str = str(member) + " added "
		category = "invalid post"
		
		if message_id in reaction_categories.keys():
			role, category = reaction_categories[message_id](payload.emoji.name, guild)	
		
		print(member_str + category)
		 
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
		member_str = str(member) + " removed "
		category = "invalid post"
		
		if message_id in reaction_categories.keys():
			role, category = reaction_categories[message_id](payload.emoji.name, guild)	
		
		print(member_str + category)

			
		if role is not None: 
			if member is not None:
				await member.remove_roles(role)
				print(str(member) + " removed " + str(role))
			else: 
				print("member not found")
		
client.run(config.bot_key)