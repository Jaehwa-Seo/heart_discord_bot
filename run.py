from token_data import token
import discord
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = './google_sheet.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1HChfMTew04Quy0LuWRckUW9ovmto5uZQ0NAyKmGQKx0/edit#gid=0'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('Discord_user_data')
user_data = worksheet.get_all_values()

print(user_data)


from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

global immigration_message, immigration_user, immigration_count
immigration_count = 0;


@bot.event    
async def on_ready():
    print("라미 봇 ON")

@bot.command()
async def 자기소개끝(message):
    print("자기소개끝")
    print(discord.Team.members)
    channel = bot.get_channel(1166986626568835102)
    
    # embed = discord.Embed(title= message.author.name + "님의 입국 심사", color=discord.Color.green())
    # # channel = bot.get_channel(1041268462183534595)
    # channel = bot.get_channel(1125625298063462411)
    # global immigration_message, immigration_user, immigration_count
    # immigration_message = await channel.send(embed=embed)
    # immigration_user = message.author
    # immigration_count = 0

    # print(immigration_count)
    # await immigration_message.add_reaction("⭕")

@bot.command()
async def print_members(message):
    print("print_members")
    member_info = bot.get_guild(1036292207491154041).members

    # for info in member_info:
    #     index = 0
    #     for name in user_data:
    #         if name[1] == info.nick:
    #             break
    #         index += 1

    #     worksheet.update_cell(index+1, 1, str(info.id))
    #     worksheet.insert_row([info.id, info.nick, info.name, 0], 1)
    #     time.sleep(1)


# @bot.command()
# async def give_test(message):
#     print("give_test")
#     global immigration_user
#     # await message.author.add_roles(bot.get_guild(1041268462183534592).get_role(1126092766527619104)) 
#     # msg = immigration_user.name+"님 환영합니다. 🐻"
#     # channel = bot.get_channel(1041268462183534595)
#     # await channel.send(msg) 
#     await message.author.add_roles(bot.get_guild(1036292207491154041).get_role(1041002722029215846)) 
#     msg = immigration_user.name+"님 환영합니다. 🐻"
#     channel = bot.get_channel(1125625298063462411)
#     await channel.send(msg) 

@bot.event
async def on_message(message):
    print("on_message")
    
    # message_content = message.content
    # introduce = message_content.find("자기소개끝")

    # if introduce >= 0:
    #     await message.delete()
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
   
    if user.bot == 1:
        return None
    if str(reaction.emoji) == "⭕":
        global immigration_user

        if user.name == immigration_user.name:
            return None
        
        global immigration_count
        immigration_count += 1
        print(immigration_count)
        if immigration_count == 10:
            await immigration_user.add_roles(bot.get_guild(1036292207491154041).get_role(1041002722029215846)) 
            await immigration_message.delete()
            msg = immigration_user.name+"님 환영합니다. 🐻"
            channel = bot.get_channel(1125625298063462411)
            await channel.send(msg) 

connect_data = []

@bot.event
async def on_voice_state_update(member, before, after):
    # channel = bot.get_channel(1166986626568835102)
    # await channel.send(member) 
    # await channel.send(before) 
    # await channel.send(after) 
    # print(member.id)
    # print(before.channel)
    # print(after)

    

    if before.channel == None and after.channel != None:
        user_info = {"id" : member.id, "start_time" : datetime.now()}
        connect_data.append(user_info)
    elif before.channel != None and after.channel == None:
        index = 0
        find_info = False

        for info in connect_data:
            if info["id"] == member.id:
                find_info = True
                break;
            index += 1

        if find_info:
            sheet_index = 0
            total_time = 0
            for user_id in user_data:
                if str(user_id[0]) == str(member.id):
                    total_time = user_id[3]
                    break
                sheet_index += 1
            now = datetime.now()
            connect_time = (now - connect_data[index]["start_time"]).seconds/60

            worksheet.update_cell(sheet_index+1, 4, float(total_time)+connect_time)
            del connect_data[index]

            

@bot.event
async def on_reaction_remove(reaction, user):
    print("on_reaction_remove")
    if user.bot == 1:
        return None
    if str(reaction.emoji) == "⭕":
        global immigration_user

        if user.name == immigration_user.name:
            return None

        global immigration_count
        immigration_count -= 1
        
@bot.event
async def on_member_join(member):
    print("member_join")
    msg = member.name+"님, 동그라미 나라에 오신 것을 환영합니다. 💕\n\n간단하게 자기소개 부탁드립니다. 😎\n입국하기 위해서는 10명의 동의가 필요하니 천천히 심사를 기다려 주세요. 🥰"
    channel = bot.get_channel(1125625298063462411)
    await channel.send(msg)
     

bot.run(token)