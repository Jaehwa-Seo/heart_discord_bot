from token_data import token
import discord
import time
import youtube_dl
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
async def check_daily_connect(message):
    channel = bot.get_channel(1036293472774279369)
    messages = [message async for message in channel.history(limit=1000)]
    
    tmp = []

    for info in messages:
        index = 0
        flag = False
        for id in user_data:
            if id[0] == str(info.author.id):
                flag = True
                break
            index += 1
        if flag:        
            user_data[index][5] = str(int(user_data[index][5]) + 1)
            if index not in tmp:
                print(str(info.author.name))
                tmp.append(index)
        else:
            print(str(info.author.name))
        
    print("write finish")
    print(tmp)

    for i in tmp:
        worksheet.update_cell(i+1, 6, user_data[i][5])
        time.sleep(1)

    print("finish")
 
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
# async def test(message):

play_list = []

@bot.command()
async def calculate_score(message):
    index = 0
    for data in user_data:
        if index != 0:
            total_score = int(float(data[6])) + (int(data[5]) * 30) 
            worksheet.update_cell(index+1, 9, total_score)
            time.sleep(1)
        index += 1

@bot.command()
async def play_music(message, *vars):
    print(vars)
    if len(bot.voice_clients) == 0:
        channel = message.author.voice.channel
        await channel.connect()

    voice = bot.voice_clients[0]

    if len(vars) == 0:
        # if len(play_list) <= play_number:
        # elif voice.is_playing():
        if voice.is_paused():
            await voice.resume()
        else:
            await play_music_in_list(voice)
    elif len(vars) == 1 and vars[0][0:23] == "https://www.youtube.com":
        play_list.append(vars[0])
        
        if voice.is_playing() == False:
            await play_music_in_list(voice)

ydl_opts = {
    'quiet': False,
    'default_search': 'ytsearch',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'youtube_include_dash_manifest': False,
}
FFMPEG_OPTIONS = {
    'executable': 'C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

async def play_music_in_list(voice):
    global playNumber
    global messageChannel
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(play_list[0], download = False)
            url = info['formats'][0]['url']
        playNumber = playNumber + 1
        voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),after = my_after)
    except Exception as e:
        print(e)

    
@bot.command()
async def stop_music(message):
    await bot.voice_clients[0].disconnect()



@bot.event
async def on_message(message):
    print("on_message")

    if str(message.channel.id) == "1036293472774279369":
        Daily_check_connect(message)
    else:
        await bot.process_commands(message)

    # message_content = message.content
    # introduce = message_content.find("자기소개끝")

    # if introduce >= 0:
    #     await message.delete()

connect_data = []

@bot.event
async def on_voice_state_update(member, before, after):
    print(member)
    print(before)
    print(after)
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
            month_connect_time = 0
            total_connect_time = 0
            for user_id in user_data:
                if str(user_id[0]) == str(member.id):
                    month_connect_time = user_id[3]
                    total_connect_time = user_id[6]
                    break
                sheet_index += 1

            now = datetime.now()
            connect_time = (now - connect_data[index]["start_time"]).seconds/60

            month_connect_time = float(month_connect_time)+connect_time
            total_connect_time = float(total_connect_time)+connect_time
            print(float(month_connect_time)+connect_time)
            print(user_data[sheet_index][1])
            print(month_connect_time)
            print(total_connect_time)
            user_data[sheet_index][3] = month_connect_time
            user_data[sheet_index][6] = total_connect_time

            print(user_data[sheet_index])
            print(float(month_connect_time)+connect_time)

            worksheet.update_cell(sheet_index+1, 4, month_connect_time)
            worksheet.update_cell(sheet_index+1, 7, total_connect_time)
            del connect_data[index]

@bot.event
async def on_member_join(member):
    print("member_join")
    
    msg = member.name+"님, 동그라미 나라에 오신 것을 환영합니다. 💕"
    
    channel = bot.get_channel(1125625298063462411)
    
    await channel.send(msg)



async def Monthly_discord_connect_time():
    role_foreign = bot.get_guild(1036292207491154041).get_role(1041280525094109205)
    role_people = bot.get_guild(1036292207491154041).get_role(1041002722029215846)
    index = 0
    for user_id in user_data:
        if user_id[0] != "id-code":
            if float(user_id[3]) > 600:
                user_id[3] = 0
                if user_id[4] == "외국인":
                    user_id[4] = "국민"
                    member_data = bot.get_guild(1036292207491154041).get_member(int(user_id[0]))
                    await member_data.add_roles(role_people)
                    await member_data.remove_roles(role_foreign) 

                    worksheet.update_cell(index+1, 5, "국민")
            else:
                user_id[3] = 0
                if user_id[4] == "국민":
                    user_id[4] = "외국인"
                    member_data = bot.get_guild(1036292207491154041).get_member(int(user_id[0]))
                    await member_data.add_roles(role_people)
                    await member_data.remove_roles(role_foreign) 

                    worksheet.update_cell(index+1, 5, "외국인")
        index += 1

def Daily_check_connect(message):
    user_id = message.author.id
    index = 0
    for user_info in user_data:
        if user_info[0] == str(user_id):
            today_date = datetime.today().strftime("%Y%m%d")
            if str(today_date) != user_info[7]:
                total_daily_check_count = user_info[5] 
                user_data[index][5] = str(int(user_data[index][5]) + 1)
                user_data[index][7] = str(today_date)
                worksheet.update_cell(index+1, 6, int(total_daily_check_count) + 1)
                worksheet.update_cell(index+1, 8, str(today_date))
        index += 1


     

bot.run(token)
            

# @bot.event
# async def on_reaction_remove(reaction, user):
#     print("on_reaction_remove")
#     if user.bot == 1:
#         return None
#     if str(reaction.emoji) == "⭕":
#         global immigration_user

#         if user.name == immigration_user.name:
#             return None

#         global immigration_count
#         immigration_count -= 1

# @bot.event
# async def on_reaction_add(reaction, user):
   
#     if user.bot == 1:
#         return None
#     if str(reaction.emoji) == "⭕":
#         global immigration_user

#         if user.name == immigration_user.name:
#             return None
        
#         global immigration_count
#         immigration_count += 1
#         print(immigration_count)
#         if immigration_count == 10:
#             await immigration_user.add_roles(bot.get_guild(1036292207491154041).get_role(1041002722029215846)) 
#             await immigration_message.delete()
#             msg = immigration_user.name+"님 환영합니다. 🐻"
#             channel = bot.get_channel(1125625298063462411)
#             await channel.send(msg) 
        
