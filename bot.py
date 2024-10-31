import config
import discord
from emoji.unicode_codes import EMOJI_ALIAS_UNICODE_ENGLISH as EMOJIS 
from discord.ext import commands
from discord.ext.tasks import loop
from discord.utils import get
import gspread
import re 
from datetime import datetime, timedelta
from pathlib import Path
import pickle
import markovify 
import spacy
from datetime import datetime, timezone
from dateutil import tz
from dicts import character_mats, vanity

#DALLE
from Classes import Dalle
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Union
from discord import Embed
from discord.ext import commands
import random

nlp = spacy.load("en_core_web_sm")
def is_image_url(url):
	parsed = url.split(".")
	ending = parsed[-1].lower()

	return True if ending == "jpg" or ending == "jpeg" or ending == "png" or ending == "gif" else False

class POSifiedText(markovify.NewlineText):
	def word_split(self, sentence):
		return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

	def word_join(self, words):
		sentence = " ".join(word.split("::")[0] for word in words)
		return sentence

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

#leaks channels 
leaks_channel = 913137663400374312
leaks_discussion = 777083973984976946

sr_leaks_channel = 1209886429296201738
sr_leaks_discussion = 1120836976283766801

#Other channels 
general = 763500030928879666
news = 763499148867403816
test_channel = 851544672672677958
art_club = 1006585412246057141
sr_news = 1116323672941137980

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
	EMOJIS[':eight:'] : "8",
	EMOJIS[':nine:'] : "9",
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


fanart_contest = {
	"paimoncoinbobross" : 922678865707565086,
	"paimoncoincute" : 909272962119651378,
	"paimoncoincool" : 909273025361371157, 
	"paimoncoinfancy" : 909273086354935820,
}


from collections import Counter

talent_costs = [
Counter({"Mora":0, "T1 books": 0, "T2 books": 0, "T3 books": 0, "T1 drops": 0, "T2 drops": 0,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":12500, "T1 books": 3, "T2 books": 0, "T3 books": 0, "T1 drops": 6, "T2 drops": 0,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":17500, "T1 books": 0, "T2 books": 2, "T3 books": 0, "T1 drops": 0, "T2 drops": 3,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":25000, "T1 books": 0, "T2 books": 4, "T3 books": 0, "T1 drops": 0, "T2 drops": 4,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":30000, "T1 books": 0, "T2 books": 6, "T3 books": 0, "T1 drops": 0, "T2 drops": 6,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":37500, "T1 books": 0, "T2 books": 9, "T3 books": 0, "T1 drops": 0, "T2 drops": 9,"T3 drops": 0, "Boss drops": 0}),
Counter({"Mora":120000, "T1 books": 0, "T2 books": 0, "T3 books": 4, "T1 drops": 0, "T2 drops": 0,"T3 drops": 4, "Boss drops": 1}),
Counter({"Mora":260000, "T1 books": 0, "T2 books": 0, "T3 books": 6, "T1 drops": 0, "T2 drops": 0,"T3 drops": 6, "Boss drops": 1}),
Counter({"Mora":450000, "T1 books": 0, "T2 books": 0, "T3 books": 12, "T1 drops": 0, "T2 drops": 0,"T3 drops": 9, "Boss drops": 2}),
Counter({"Mora":700000, "T1 books": 0, "T2 books": 0, "T3 books": 16, "T1 drops": 0, "T2 drops": 0,"T3 drops": 12, "Boss drops": 2}),
]

with open('json_model.json', 'r') as outfile:
	model_json = outfile.read()
text_model = POSifiedText.from_json(model_json)
# text_model = markovify.Text.from_json(model_json)
chat_count = 0 

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
		member_id = payload.member.id
		msg = await client.get_channel(payload.channel_id).fetch_message(message_id)

		seen = set()			
		for emote in msg.reactions:
			async for user in emote.users():
				seen.add(user)

		print(len(seen))
		if len(seen) >= 4 or member_id == grandpapants:
			with open('MuseumIDs.txt') as f:
				lines = [line.rstrip() for line in f]

			if str(message_id) not in lines:	
				print("Image has been voted into the museum")

				if "twitter.com" in msg.content:	
					print("in twitter")									
					embed = msg.content
					await client.get_channel(fanart_dest).send(embed)
					
				elif is_image_url(msg.content):
					print("is image link")
					await client.get_channel(fanart_dest).send(msg.content)

				elif msg.embeds:
					print("in embeds")	
					for embed in msg.embeds:
						await client.get_channel(fanart_dest).send(embed=embed)
					
				elif msg.attachments:	
					print("in attachments")
					for embed in msg.attachments:
						await client.get_channel(fanart_dest).send(embed)					

				with open('MuseumIDs.txt', "a") as f:
						f.write(str(message_id)+"\n")


		#fanart contest		
		if payload.emoji.name in fanart_contest.keys():
			coin_name = payload.emoji.name
			target_channel = fanart_contest[coin_name]

			filename = Path(coin_name + "-ImageIDs.txt")
			filename.touch(exist_ok=True)

			filename = Path(coin_name + "-MemberIDs.txt")
			filename.touch(exist_ok=True)
			

			with open(coin_name + "-ImageIDs.txt") as f:
				image_ids = [line.rstrip() for line in f]
			with open(coin_name + "-MemberIDs.txt") as f:
				user_ids = [line.rstrip() for line in f]

			if str(message_id) not in image_ids and str(member_id) not in user_ids:
				print(coin_name + " nomination has been made")
				if "twitter.com" in msg.content:	
					print("in twitter")									
					embed = msg.content
					new = await client.get_channel(target_channel).send(embed)
					
				elif is_image_url(msg.content):
					print("is image link")
					new = await client.get_channel(target_channel).send(msg.content)

				elif msg.embeds:
					print("in embeds")			
					new = await client.get_channel(target_channel).send(embed=msg.embeds[0])
					
				elif msg.attachments:	
					print("in attachments")
					new = await client.get_channel(target_channel).send(msg.attachments[0])	

				await new.add_reaction("<:paimoncoin:922681177071034368>")				

				with open(coin_name + "-ImageIDs.txt", "a") as f:
					f.write(str(message_id)+"\n")
				with open(coin_name + "-MemberIDs.txt","a") as f:
					f.write(str(member_id)+"\n")
				

				



		
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


@client.event
async def on_message(message):
	channel = message.channel
	await client.process_commands(message)
	global chat_count

	if channel.id == leaks_channel:
		print("leak detected")
		await client.get_channel(leaks_discussion).send(message.content, tts=message.tts, files=[await attch.to_file() for attch in message.attachments])
	if channel.id == sr_leaks_channel:
		print("sr leak detected")
		await client.get_channel(sr_leaks_discussion).send(message.content, tts=message.tts, files=[await attch.to_file() for attch in message.attachments])
		
	if channel.id == general: 
		chat_count = chat_count + 1 
		if chat_count > 200: 
			query = text_model.make_sentence()
			if random.randint(1,10) == 11:
				ctx = client.get_channel(general)
				await draw(ctx, query = query, override = True)
			else:
				await client.get_channel(general).send(query)
			chat_count = 0
	if channel.id == news: 
		if len(message.content) == 12: 
			await client.get_channel(news).send("<https://genshin.hoyoverse.com/en/gift?code=" + message.content+">")	
	if channel.id == sr_news: 
		if len(message.content) == 12: 
			await client.get_channel(sr_news).send("<https://hsr.hoyoverse.com/gift?code=" + message.content+">")	
	if channel.id == test_channel:
		pass

@client.command(aliases=["register"])
async def genshin(ctx, uid = None):
	try:
		sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	except :
		await ctx.send("Connection to sheet lost, try again")
		return 

	user = ctx.author  
	#automatic 
	if uid and len(uid) == 9 and uid.isnumeric(): 		
		#get roles 
		print(str(user) + " registering with " + str(uid))

		user_s = str(user).lower()
		nickname = user.nick	
		discord_id = str(user.id)	
	
		#updating sheet
		cells = sheet.findall(discord_id)
		values = [user_s, nickname, uid]
		#new registration
		if len(cells) == 0: 
			values.append("")
			values.append(discord_id)
			sheet.append_row(values)
			await ctx.send("Goon registered!")
		#updating
		else:
			r = str(sheet.find(discord_id).row)			
			cell_list = sheet.range('A'+r+":C"+r)
			for i, v in enumerate(values):
				cell_list[i].value = v
			sheet.update_cells(cell_list)
			await ctx.send("Goon updated!")
	elif uid: 
		await ctx.send("Registration failed, UID is not 9 digits")
	else: 
		await ctx.send("Registration failed, did not get UID")

@client.command()
async def starrail(ctx, uid = None):
	try:
		sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	except :
		await ctx.send("Connection to sheet lost, try again")
		return 

	user = ctx.author  
	#automatic 
	if uid and len(uid) == 9 and uid.isnumeric(): 		
		#get roles 
		print(str(user) + " registering with " + str(uid))

		user_s = str(user).lower()
		nickname = user.nick
		discord_id = str(user.id)		
	
		#updating sheet
		cells = sheet.findall(discord_id)
		values = [user_s, nickname]
		#new registration
		if len(cells) == 0: 
			values.append("")
			values.append(uid)
			values.append(discord_id)
			sheet.append_row(values)
			await ctx.send("Goon registered!")
		#updating
		else:
			r = str(sheet.find(discord_id).row)
			cell_list = sheet.range('A'+r+":D"+r)
			for i, v in enumerate(values):
				cell_list[i].value = v

			cell_list[0].value = user_s
			cell_list[1].value = nickname
			cell_list[3].value = uid
			sheet.update_cells(cell_list)
			await ctx.send("Goon updated!")
	elif uid: 
		await ctx.send("Registration failed, UID is not 9 digits")
	else: 
		await ctx.send("Registration failed, did not get UID")

game_list = ["Genshin: ", "Star Rail: "]
@client.command()
async def goon(ctx, term = None):
	print("goon")
	try:
		sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	except :
		await ctx.send("Connection to sheet lost, try again")
		return 

	#get self
	if term == None: 
		user = str(ctx.author.id)
		values = sheet.findall(user)
		if len(values) == 0:
			await ctx.send("You have not registered yet, you can do so using !register <insert UID here>")
	#search
	else: 
		#if UID		
		if len(term) == 9 and term.isnumeric():
			print("UID match " + term)
			values = sheet.findall(term)
		#nickname
		else: 
			print("nick search " + term)
			values = sheet.findall(term)

	if len(values) > 0: 
		print("goon found")
		to_print = []
		for r in values:   
			row_values = sheet.row_values(r.row)
			if term != None:
				to_print = [row_values[0]]
			row_values = row_values[2:]
			for i, v in enumerate(row_values[:-1]):
				if v.strip():
					to_print.append(game_list[i] + v)

			await ctx.send(', '.join(to_print))
	else: 
		print("goon not found")
		await ctx.send("Goon not found")

@client.command()
async def unregister(ctx, uid = None):
	try:
		sheet = gc.open_by_key('1E9KJhGEjgST2KdPBDy0UcO2KvYRq4YXjtTJmctCGvwQ').sheet1
	except :
		await ctx.send("Connection to sheet lost, try again later")
		return 

	# if uid: 
	# 	values = sheet.findall(uid)		
	# else: 
	user = str(ctx.author).lower()
	values = sheet.findall(user)
	for r in values: 
			sheet.delete_row(r.row)
	return 

@client.command()
async def aprilfools(ctx, term = None):
	if ctx.channel.id == 851544672672677958:
		if term:
			try: 
				msg = text_model.make_sentence_with_start(term)
			except markovify.text.ParamError:
				msg = text_model.make_sentence()
			await client.get_channel(general).send(msg)
		else: 
			await client.get_channel(general).send(text_model.make_sentence())	

@client.command()
async def generate(ctx, *, term = None):
	if ctx.channel.id == 851544672672677958:
		ctx = client.get_channel(general)		
		if term:
			query = term
		else: 
			query = random.choice(characters) + " from genshin impact"
		await draw(ctx, query = query, override = True)

def parse_date(date, hour):
	now = datetime.now(timezone.utc)
	combined = date + " " + hour
	try:
		return datetime.strptime(combined, '%Y/%m/%d %I%p')
	except ValueError:
		pass
	try: 
		return datetime.strptime(combined, '%Y/%m/%d %H:%M')
	except ValueError: 
		pass
	try:
		return datetime.strptime(str(now.year) + "/"  + combined, '%Y/%m/%d %I%p')
	except ValueError:
		return 0

@client.command()
async def time(ctx, date = None, hour = None):
	message = ""
	from_zone = tz.gettz("UTC+8")

	if date == None:
		message = "No date entered. Find out how long until a specific UTC+8 time! Available formats are YYYY/MM/DD 06:00, YYYY/MM/DD 6AM, MM/DD 6AM (Copied from news posts)"
	else:			
		target_date = parse_date(date, hour)
		if target_date != 0:
			target_date = target_date.replace(tzinfo=from_zone)			
			message = date + " " + hour + " UTC+8 is <t:"+str(int(target_date.timestamp()))+":R>"
		else: 
			message = "Invalid date, available formats are YYYY/MM/DD 06:00, YYYY/MM/DD 6AM, MM/DD 6AM. Bother Xun for more formats if you want"
			

	await ctx.send(message)

@client.command()
async def shop(ctx):
	await ctx.send("https://cdn.discordapp.com/attachments/763499290914979871/1013892054788608010/unknown.png")

@client.command()
async def srshop(ctx):
	await ctx.send("https://cdn.discordapp.com/attachments/1099727180747001886/1155155520043356230/image.png")

@client.command()
async def books(ctx):
	await ctx.send("https://cdn.discordapp.com/attachments/851544672672677958/1301488444501000234/g3.png")

@client.command()
async def talents(ctx, start = None, end = None):
	if start == None:
		await ctx.send("https://i.imgur.com/He8yLVY.png")
	else:
		print_order = ["Mora", "T1 books", "T2 books", "T3 books", "T1 drops", "T2 drops","T3 drops", "Boss drops"]

		try:
			start = int(start)
			end = int(end)
		except:
			await ctx.send("Input incorrectly formatted! Format should be !talents start end (eg. !talents 1 10)")
			return

		if start < 1 or end > 10: 
			await ctx.send("Talent levels out of bounds")
			return

		final = talent_costs[0]
		if start < end:
			for i in range(start, end):
				final = final + talent_costs[i]

		output = "" 
		for key in print_order:
			if final[key] != 0: 
				output = output + f'{final[key]:,}' + " " + key + " | "

		if output == "":
			await ctx.send("No mats needed")
			return

		await ctx.send(output[:len(output)-2])


drawing_messages = [
"Drawing...",
"Hold on...",
"Wait a moment..."
]

finished_messages = [
"Behold!",
"I have drawn", 
"Here is"
]

#DALLE STUFF 
@client.command()
async def draw(ctx, *, query =  None, override = False):
	print(query)
	print(override)
	if override or ctx.channel.id == art_club:
		# Check if query is empty
		if not query:
			query = random.choice(characters) + " genshin impact"

		# Check if query is too long
		if len(query) > 100:
			await ctx.send("Invalid query\nQuery is too long.")
			return

		print(f"[-] dalle was called with {query}")

		message = await ctx.send(random.choice(drawing_messages))

		try:
			dall_e = await Dalle.DallE(prompt=f"{query}", author=f"Katheryne")
			generated = await dall_e.generate()

			if len(generated) > 0:			
				first_image = Image.open(random.choice(generated).path)

				i = 0
				while os.path.exists("./generated/art%s.png" % i):
				    i += 1

				artname = "art" + str(i) + ".png"
				first_image.save(f"./generated/" + artname)		

				# Prepare the attachment
				file = discord.File(f"./generated/" + artname, filename=artname)
				message = await ctx.send(random.choice(finished_messages) + " " + query)
				await ctx.send(file=file)
				os.remove(f"./generated/" + artname)


		except Dalle.DallENoImagesReturned:
			await ctx.send(f"Unable to draw {query}.")
		except Dalle.DallENotJson:
			await ctx.send("Serialization Error, please try again later.")
		except Dalle.DallEParsingFailed:
			await ctx.send("Parsing Error, please try again later.")
		except Dalle.DallESiteUnavailable:
			await ctx.message.send("Lost my pen, please try again later.")
		except Exception as e:
			await ctx.send("Nevermind, please try again later.")
			print(repr(e))

@client.command()
async def mats(ctx, search):
	print("search for " + search)
	search = search.lower()
	if search in character_mats.keys():
		await ctx.send(character_mats[search])
	else:
		await ctx.send(search + " not found")

# @loop(minutes=60.0)
# async def countdown():
# 	print("Checking banned list")
# 	try:
# 		ban_list = pickle.load(open("ban_list", 'rb'))
# 		day_list = pickle.load(open("day_list", 'rb'))

# 		now = datetime.now()
# 		to_remove = [] 

# 		for i in range(len(ban_list)):
# 			if(now > day_list[i]):
# 				guild = await client.fetch_guild(763498760537767956)

# 				try: 
# 					member = await guild.fetch_member(ban_list[i])
# 				except: 
# 					member = False 

# 				if member:
# 					print("checking " + str(member))
# 					await member.remove_roles(discord.utils.get(guild.roles,id=854734771321569290))
# 					channel = await client.fetch_channel(782784858471792641)
# 					to_remove.append(i)
# 					await channel.send("Unprobed " + str(member))

# 		for i in to_remove: 
# 			del ban_list[i]
# 			del day_list[i]

# 		pickle.dump(ban_list, open("ban_list", "wb"))
# 		pickle.dump(day_list, open("day_list", "wb"))

# 	except(OSError, IOError) as e:
# 		print("No ban list found")


# @client.command(pass_context = True)
# async def probe(ctx,member:discord.Member, days = 1, hours = 0):
# 	if ctx.message.author.id == grandpapants or ctx.message.author.id == xun:
# 		guild = ctx.guild
# 		await member.add_roles(discord.utils.get(guild.roles,id=854734771321569290))
# 		await ctx.send('User probed for **' + str(days) + ' day(s)** and **' + str(hours) + ' hour(s)**')
# 		print("probed " + str(member) + " for " + str(days) + " days and " + str(hours) + " hours")

# 		try: 
# 			ban_list = pickle.load(open("ban_list", 'rb'))
# 			day_list = pickle.load(open("day_list", 'rb'))
# 		except (OSError, IOError) as e:
# 			ban_list = []
# 			day_list = [] 

# 		ban_list.append(member.id)
# 		day_list.append(datetime.now() + timedelta(days=days, hours = hours))


# 		pickle.dump(ban_list, open("ban_list", "wb"))
# 		pickle.dump(day_list, open("day_list", "wb"))

# 	else: 
# 		await ctx.send("Thank you for volunteering for mod duty. Please report to Grandpapants as soon as possible")
# countdown.start()
client.run(config.bot_key)
