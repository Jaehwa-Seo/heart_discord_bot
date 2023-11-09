from token_data import token
import discord
import time
import youtube_dl
from datetime import datetime
import gspread
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from youtube_search import YoutubeSearch

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

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

global immigration_message, immigration_user, immigration_count
immigration_count = 0;


@bot.event    
async def on_ready():
    print("라미 봇 ON")
    global musicChannel
    musicChannel = bot.get_channel(1171707718688575558)

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



@bot.command()
async def calculate_score(message):
    index = 0
    for data in user_data:
        if index != 0:
            total_score = int(float(data[6])) + (int(data[5]) * 30) 
            worksheet.update_cell(index+1, 9, total_score)
            time.sleep(1)
        index += 1

global musicChannel
playList = []

play_list = []
playNumber = 0

# @bot.command()
# async def play_music(message, *vars):
#     print(vars)
#     if len(bot.voice_clients) == 0:
#         channel = message.author.voice.channel
#         await channel.connect()

#     voice = bot.voice_clients[0]

#     if len(vars) == 0:
#         # if len(play_list) <= play_number:
#         # elif voice.is_playing():
#         if voice.is_paused():
#             await voice.resume()
#         else:
#             await play_music_in_list(voice)
#     elif len(vars) == 1 and vars[0][0:23] == "https://www.youtube.com":
#         play_list.append(vars[0])
        
#         if voice.is_playing() == False:
#             await play_music_in_list(voice)



# async def play_music_in_list(voice):
#     global playNumber
#     messageChannel = bot.get_channel(1166986626568835102)
    
#     try:
#         str = " ".join(vars)
#         print(str)
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             if str[0:23] == "https://www.youtube.com" or str[0:16] == "https://youtu.be":
#                 print("playmusic")
#                 info = ydl.extract_info(play_list[0], download = False)
#                 url = info['formats'][0]['url']
#             else:
#                 info = ydl.extract_info(f"ytsearch:{str}", download = False)['entries'][0]
#                 print("end")
#                 await messageChannel.send(info)

#         playNumber = playNumber + 1
#         voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),after = my_after)
#     except Exception as e:
#         print(e)



# @bot.command()
# async def play_music(message, *vars):
#     print(vars)
    

#     voice = bot.voice_clients[0]

#     if len(vars) == 0:
#         # if len(play_list) <= play_number:
#         # elif voice.is_playing():
#         if voice.is_paused():
#             await voice.resume()
#         else:
#             await play_music_in_list(voice)
#     elif len(vars) == 1 and vars[0][0:23] == "https://www.youtube.com":
#         play_list.append(vars[0])
        
#         if voice.is_playing() == False:
#             await play_music_in_list(voice)

        
async def music_bot_play(message=None):
    global musicChannel
    global playNumber
    global playList
    
    if len(bot.voice_clients) == 0 and message != None:
        channel = message.author.voice.channel
        await channel.connect()

    voice = bot.voice_clients[0]

    if not voice.is_playing():
        if voice.is_paused():
            voice.resume()
        else:
            try:
                if len(playList) == 0:
                    await musicChannel.send("리스트에 음악이 없습니다. /노래 추가 음악제목 명령어를 이용해 음악을 추가해주세요.")
                elif playNumber >= len(playList) :
                    playNumber = 0
                if playNumber < len(playList):
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(playList[playNumber]["url"], download = False)
                        url = info['formats'][0]['url']
                
                    playNumber = playNumber + 1
                    voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),after = my_after)
            except Exception as e:
                print(e)

def my_after(error):
    global playNumber
    global playList

    try:
        fut = None
        if playNumber >= len(playList):
            playNumber = 0

        fut = asyncio.run_coroutine_threadsafe(music_bot_play(), bot.loop)
        fut.result()
    except Exception as e:
        print(e)

async def music_bot_stop():
    global musicChannel
    await bot.voice_clients[0].disconnect()
    await musicChannel.send("노래를 멈췄습니다.")

async def music_bot_leave():
    global musicChannel
    await bot.voice_clients[0].disconnect()
    await musicChannel.send("퇴장하겠습니다...")

async def music_bot_reset():
    bot.voice_clients[0].stop()

    global playNumber
    playNumber = 0
    playList.clear()

    global musicChannel
    await musicChannel.send("리스트를 초기화했습니다. 노래를 추가해주세요.")

async def music_bot_pause():
    bot.voice_clients[0].pause()
    global musicChannel
    await musicChannel.send("노래를 일시정지했습니다.")

async def music_bot_resume():
    bot.voice_clients[0].resume()
    global musicChannel
    await musicChannel.send("노래를 다시 재생했습니다.")

async def music_bot_skip(message):
    bot.voice_clients[0].stop()
    await music_bot_play(message)

async def music_bot_delete(message):
    global playNumber
    global playList

    del playList[playNumber-1]

    bot.voice_clients[0].stop()
    await music_bot_play(message)

async def music_bot_print_list():
    global playList
    global playNumber
    
    text = ""
    num = 1

    for music in playList:
        
        text += str(num) + ". " + music["title"]
        if playNumber == num:
            text += "  ★"

        text += "\n"

        num += 1

    embed = discord.Embed(title="노래 리스트", description=text)
    
    embedMessage = await musicChannel.send(embed=embed)


async def music_bot_add(message,vars):
    global musicChannel
    global playList

    try:
        musicName = " ".join(vars[1:])

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if musicName[0:23] == "https://www.youtube.com" or musicName[0:16] == "https://youtu.be":
                playList.append(musicName)
                await musicChannel.send("음악을 추가했습니다.")
                await music_bot_play(message)
            else:
                results = YoutubeSearch(musicName, max_results=10).to_dict()

                text = ""
                num = 1
                for music in results:
                    text += str(num) + ". " + music["title"] + "\n"
                    num += 1

                embed = discord.Embed(title="원하는 노래의 번호를 입력해주세요", description=text)
                
                embedMessage = await musicChannel.send(embed=embed)

                def check(m):
                    return m.author == message.author and m.channel == message.channel

                try:
                    msg = await bot.wait_for('message',check=check, timeout = 60)
                except asyncio.TimeoutError: 
                    await musicChannel.send("입력 시간을 초과하였습니다. 다시 음악을 추가해주세요.")
                else:
                    try: 
                        selectNumber = int(msg.content) - 1
                        playList.append({"title" : results[selectNumber]["title"],"url" : "https://www.youtube.com" + results[selectNumber]["url_suffix"] })

                        await musicChannel.send("음악을 추가했습니다.")
                        await music_bot_play(message)
                    except:
                        await musicChannel.send("번호를 잘못 입력하였습니다. 다시 음악을 추가해주세요.")

            
    except Exception as e:
        print(e)
        await musicChannel.send("음악을 추가를 실패하였습니다.")


# @bot.command()
# async def queue(message):
#     await message.channel.send(f'{playNumber} / {len(playList)}')



@bot.command()
async def 노래(message,*vars):
    print(vars)
    if vars[0] == "추가":
        await music_bot_add(message,vars)
    elif vars[0] == "재생":
        await music_bot_play(message)
    elif vars[0] == "멈춤":
        await music_bot_stop()
    elif vars[0] == "일시정지":
        await music_bot_pause()
    elif vars[0] == "퇴장":
        await music_bot_leave()
    elif vars[0] == "초기화":
        await music_bot_reset()
    elif vars[0] == "스킵":
        await music_bot_skip(message)
    elif vars[0] == "리스트":  
        await music_bot_print_list()
    elif vars[0] == "삭제":
        await music_bot_delete(message)  





@bot.event
async def on_message(message):
    print("on_message")

    if str(message.channel.id) == "1036293472774279369":
        Daily_check_connect(message)
    else:
        await bot.process_commands(message)

connect_data = []

@bot.event
async def on_voice_state_update(member, before, after):
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

            user_data[sheet_index][3] = month_connect_time
            user_data[sheet_index][6] = total_connect_time

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
        
