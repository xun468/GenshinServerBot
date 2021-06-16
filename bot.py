import config
import discord
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from discord.ext import commands
from discord.ext.tasks import loop
from discord.utils import get
import gspread
import re 
from datetime import datetime, timedelta
import pickle

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!")
#SPREAADSHEETSS 
gc = gspread.service_account(filename="service_account.json")

#Fanart management stuff 
grandpapants = 487023958110109757
xun = 161536840002830336
seal = "bennet_thumbsup"
fanart_source = 764590126420459530
fanart_dest = 849138260374323210

#Role react stuff
sever_msg_id = 	782664853784756234
wl_msg_id = 782665043845840996
vanity_msg_id = 795488467190153236
pronoun_msg_id = 795491652017979472
command_msg_id = 807789677729808385
housing_msg_id = 802955738267385906

servers = {
	EMOJIS[':red_square:']    : "NA",
	EMOJIS[':blue_square:']   : "EU",
	EMOJIS[':yellow_square:'] : "Asia",
}

WL = {
	EMOJIS[':one:']   : "1-5",
	EMOJIS[':two:']   : "1-5",
	EMOJIS[':three:'] : "1-5",
	EMOJIS[':four:']  : "1-5",
	EMOJIS[':five:']  : "1-5",
	EMOJIS[':six:']   : "6",
	EMOJIS[':seven:'] : "7",
	EMOJIS[':eight:'] : "8"
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
	EMOJIS[':knife:']   : 806554181175214080,
	"broke"   : 802948687508668456	
}

pronouns = {
	"venteee" : 802947991253549167,
	"lazy"    : 802947995955757098,
	"lumided" : 802947992780800022

}

WLS = ["WL8", "WL7", "WL6", "WL5", "WL4", "WL3", "WL2", "WL1"]
server_names = ["NA", "EU", "Asia"]
WL_server = ["EU1-5", "EU6" ,"EU7",	"EU8",
			"NA1-5", "NA6", "NA7", "NA8",
			"Asia1-5", "Asia6", "Asia7", "Asia8"]

def get_server(name, guild):
	if name in servers.keys():
		return discord.utils.get(guild.roles,name=servers[name]), "server reaction" 	
	return None, "invalid server reaction" 

def get_WL(name, member, guild):
	if name in WL.keys():
		roles = [y.name for y in member.roles]
		for s in server_names: 
			if s in roles: 
				return discord.utils.get(guild.roles,name=s+WL[name]), "WL reaction"	
		for s in WL_server: 
			if s in roles:
				return discord.utils.get(guild.roles,name=s), "WL reaction"			
	return None, "invalid WL reaction"

def get_vanity(name, guild):
	if name in vanity.keys():
		return discord.utils.get(guild.roles,id=vanity[name]), "vanity reaction"
	return None, "invalid vanity reaction"

def get_pronoun(name, guild):
	if name in pronouns.keys():
		return discord.utils.get(guild.roles,id=pronouns[name]), "pronoun reaction"
	return None, "invalid pronoun reaction"

def get_housing(name, member, guild):
	if (name == EMOJIS[':house:']):
		roles = [y.name for y in member.roles]
		for s in server_names: 
			if s in roles: 
				return discord.utils.get(guild.roles,name="Housing-"+s), "Housing reaction"	
	return None, "invalid WL reaction"	
	
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
	#Role Reacts 
	message_id = payload.message_id
	if message_id == sever_msg_id or wl_msg_id:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
		member = payload.member
		role = None 
		member_str = str(member) + " added "
		category = "invalid post"
		
		if message_id == wl_msg_id: 
			role, category = get_WL(payload.emoji.name, member, guild)
			print(member_str + category)
		elif message_id == housing_msg_id: 
			role, category = get_housing(payload.emoji.name, member, guild)
			print(member_str + category)
		elif message_id in reaction_categories.keys():
			role, category = reaction_categories[message_id](payload.emoji.name, guild)	
			print(member_str + category)

		if role is not None: 
			if member is not None:
				await member.add_roles(role)
				print(str(member) + " added " + str(role))
			else: 
				print("member not found")

	#Fanart Curation 
	channel = payload.channel_id	
	if channel == fanart_source:
		message_id = payload.message_id
		msg = await client.get_channel(payload.channel_id).fetch_message(message_id)
		#grandpapants 
		if payload.member.id == grandpapants:
			print("Grandpapants has added an image to the museum") 			
			embed = msg.embeds[0]
			await client.get_channel(fanart_dest).send(embed=embed)
		#popular vote 
		else:
			seen = set()			
			for emote in msg.reactions:
				async for user in emote.users():
					seen.add(user)

			print(len(seen))		
			if len(seen) >= 4 and msg.embeds:
				print("in embeds")				
				with open('MuseumIDs.txt') as f:
						lines = [line.rstrip() for line in f]
				if str(message_id) not in lines:
					print("Image has been voted into the museum") 	
					embed = msg.embeds[0]
					await client.get_channel(fanart_dest).send(embed=embed)
					with open('MuseumIDs.txt', "a") as f:
						f.write(str(message_id)+"\n")
			elif len(seen) >= 4 and msg.attachments:	
				print("in attachments")			
				with open('MuseumIDs.txt') as f:
						lines = [line.rstrip() for line in f]
				if str(message_id) not in lines:
					print("Image has been voted into the museum") 	
					embed = msg.attachments[0].url
					await client.get_channel(fanart_dest).send(embed)
					with open('MuseumIDs.txt', "a") as f:
						f.write(str(message_id)+"\n")
			elif len(seen) >= 4 and "twitter.com" in msg.content:	
				print("in twitter")	
				with open('MuseumIDs.txt') as f:
						lines = [line.rstrip() for line in f]
				if str(message_id) not in lines:
					print("Image has been voted into the museum") 	
					embed = msg.attachments[0].url
					await client.get_channel(fanart_dest).send(embed)
					with open('MuseumIDs.txt', "a") as f:
						f.write(str(message_id)+"\n")
		
@client.event 
async def on_raw_reaction_remove(payload): 
	message_id = payload.message_id
	if message_id == sever_msg_id or wl_msg_id:
		guild = await client.fetch_guild(payload.guild_id)
		member = await guild.fetch_member(payload.user_id)
		role = None 
		member_str = str(member) + " removed "
		category = "invalid post"
		
		if message_id == wl_msg_id: 
			role, category = get_WL(payload.emoji.name, member, guild)
			print(member_str + category)
		elif message_id == housing_msg_id: 
			role, category = get_housing(payload.emoji.name, member, guild)
			print(member_str + category)
		elif message_id in reaction_categories.keys():
			role, category = reaction_categories[message_id](payload.emoji.name, guild)	
			print(member_str + category)
			
		if role is not None: 
			if member is not None:
				await member.remove_roles(role)
				print(str(member) + " removed " + str(role))
			else: 
				print("member not found")

@client.command()
async def register(ctx, uid = None, server = None, wl = None):
	sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	user = ctx.author  
	#automatic 
	if uid and len(uid) == 9 and uid.isnumeric(): 		
		#get roles 
		all_roles = set([i.name for i in user.roles])
		print(str(user) + " registering with " + str(all_roles))

		user_s = str(user).lower()
		nickname = user.display_name

		server = list(all_roles.intersection(server_names))
		if not server:
			server = "Not Given"
		else:
			server = server[0]

		wls = list(all_roles.intersection(WL_server))
		wl = '0'
		if not wls: 
			wl = "Not given"
		else: 
			for r in wls: 
				if(int(r[-1]) > int(wl)):
					wl = r[-1]
			if wl == '5': 
				wl = "1-5"
	
		#updating sheet
		cells = sheet.findall(user_s)
		values = [user_s, nickname, uid, server, wl]
		#new registration
		if len(cells) == 0: 
			sheet.append_row(values)
			await ctx.send("Goon registered!")
		#updating
		else:
			r = str(sheet.find(user_s).row)
			cell_list = sheet.range('A'+r+":E"+r)
			for i, v in enumerate(values):
				cell_list[i].value = v
			sheet.update_cells(cell_list)
			await ctx.send("Goon updated!")
	elif uid: 
		await ctx.send("Registration failed, UID is not 9 digits")
	else: 
		await ctx.send("Registration failed, did not get UID")
	# #manual 
	# elif uid and len(uid) == 9 and server: 
	# 	if not wl: 
	# 		wl = "Not Given"
	# 	cells = sheet.findall(str(uid))
	# 	values = [str(user), uid, server, wl]
	# 	if len(cells) == 0
	# 		sheet.append_row(values)
	# 	else: 
	# 		r = str(sheet.find(str(uid)).row)


@client.command()
async def goon(ctx, term = None):
	sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	#get self
	if term == None: 
		user = str(ctx.author).lower()
		values = sheet.findall(user)
		if len(values) > 0: 
			for r in values:   
				row_values = sheet.row_values(r.row)
				row_values[1] = "\"" + row_values[1] + "\""
				await ctx.send(', '.join(row_values))
		else: 
			await ctx.send("You have not registered yet, you can do so using !register <insert UID here>")
	#search
	else: 
		#if user
		if re.match(r"^.{3,32}#[0-9]{4}$", term):
			print("regex match " + term)
			values = sheet.findall(term.lower())	
		#if UID		
		elif len(term) == 9 and term.isnumeric():
			print("UID match " + term)
			values = sheet.findall(term)
		#nickname
		else: 
			print("nick search " + term)
			nick_column = sheet.range("B1:B{}".format(sheet.row_count))
			print(sheet.row_count)
			values = [found for found in nick_column if term.lower() in found.value.lower()]				

		if len(values) > 0: 
			print("goon found")
			for r in values:   
				row_values = sheet.row_values(r.row)
				row_values[1] ="\"" + row_values[1] + "\""
				await ctx.send(', '.join(row_values))
		else: 
			print("goon not found")
			await ctx.send("Goon not found")

@client.command()
async def unregister(ctx, uid = None):
	sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	# if uid: 
	# 	values = sheet.findall(uid)		
	# else: 
	user = str(ctx.author).lower()
	values = sheet.findall(user)
	for r in values: 
			sheet.delete_row(r.row)
	return 

@loop(seconds=1800)
async def countdown():
	print("Checking banned list")
	try:
		ban_list = pickle.load(open("ban_list", 'rb'))
		day_list = pickle.load(open("day_list", 'rb'))

		now = datetime.now()
		to_remove = [] 

		for i in range(len(ban_list)):
			if(now > day_list[i]):
				print(ban_list[i])

				guild = await client.fetch_guild(763498760537767956)
				member = await guild.fetch_member(ban_list[i])
				print(str(member))

				if member:
					print("checking " + str(member))
					await member.remove_roles(discord.utils.get(guild.roles,id=854734771321569290))
					channel = await client.fetch_channel(782784858471792641)
					to_remove.append(i)
					await channel.send("Unprobed " + str(member))

		for i in to_remove: 
			del ban_list[i]
			del day_list[i]

		pickle.dump(ban_list, open("ban_list", "wb"))
		pickle.dump(day_list, open("day_list", "wb"))

	except(OSError, IOError) as e:
		print("No ban list found")


@client.command(pass_context = True)
async def probe(ctx,member:discord.Member, days = 1, hours = 0):
	if ctx.message.author.id == grandpapants or ctx.message.author.id == xun:
		guild = ctx.guild
		await member.add_roles(discord.utils.get(guild.roles,id=854734771321569290))
		await ctx.send('User probed for **' + str(days) + ' day(s)** and **' + str(hours) + ' hour(s)**')
		print("probed " + str(member) + " for " + str(days) + " days and " + str(hours) + " hours")

		try: 
			ban_list = pickle.load(open("ban_list", 'rb'))
			day_list = pickle.load(open("day_list", 'rb'))
		except (OSError, IOError) as e:
			ban_list = []
			day_list = [] 

		ban_list.append(member.id)
		day_list.append(datetime.now() + timedelta(days=days, hours = hours))


		pickle.dump(ban_list, open("ban_list", "wb"))
		pickle.dump(day_list, open("day_list", "wb"))

	else: 
		await ctx.send("Thank you for volunteering for mod duty. Please report to Grandpapants as soon as possible")
countdown.start()
client.run(config.bot_key)
