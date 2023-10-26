import token
import discord
import gspred
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
    print("프린트")
    # channel = bot.get_channel(1166986626568835102)
    member_info = bot.get_guild(1036292207491154041).members

    for info in member_info:
        print(info.nick)
    
    # await channel.send(new_msg) 

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

@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(1166986626568835102)
    await channel.send(member) 
    await channel.send(before) 
    await channel.send(after) 
    print(member)
    print(before)
    print(after)

            

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