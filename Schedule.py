import discord
from discord.ext import commands
from discord import app_commands
import json, openpyxl as exl, datetime, random, asyncio, requests

scheduleList = exl.load_workbook('C:/Users/user/Desktop/SummerSchedule.xlsx')
now = datetime.datetime.now()
to_do_List = {}

def find_the_schedule():
    my_schedule = '' #messege to be sent finally
    try:
        for sheet in scheduleList.worksheets: #check each of the worksheet
            for i in range(3,34): #started at C2
                dayOnSchedule = sheet.cell(2,i).value #find today's schedule
                if dayOnSchedule == None:
                    break
                #verify by month & day
                if now.strftime("%m") == dayOnSchedule.strftime("%m") and now.strftime("%d") == dayOnSchedule.strftime("%d"):
                    #found today's schedule, then check each to-do item
                    #the subjects are placed in the grid that are multiples of 3, and the last one is No.39(B39)
                    for item in range(3, 45, 3):
                        if sheet.cell(item, i).fill.start_color.index == 'FFFFC000': #if orange cell was found
                            subject = sheet[f'B{item}'].value #find the name of each thing to do
                            #check if the date is out of range
                            if sheet.cell(item, i).value != None:
                                to_do_List[subject] = f'{sheet.cell(item, i).value}, {sheet.cell(item+1, i).value}hr' #the detail and time to execute
                            else:
                                to_do_List[subject] = f'{sheet.cell(item+1, i).value}hr'
                            my_schedule += f'{subject} : {to_do_List[subject]}\n'
                    break
            if to_do_List: #end the entire loop if schedule was found
                break
    except Exception as e:
        my_schedule = e

    return my_schedule

bot = commands.Bot(command_prefix='~', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is ready, {now}.')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='Slash commands'))
    except Exception as e:
        print(e)

@bot.event
async def on_raw_reaction_add(reaction):#給身分組
        if reaction.message_id == 936461401453641769:#用id指定訊息
            if reaction.emoji.name == 'despise':#用名字指定表情符號
                guild = discord.utils.find(lambda g : g.id == reaction.guild_id, bot.guilds)#找伺服器
                role = discord.utils.get(guild.roles, name='成員')#找伺服器中的身分組
                member = discord.utils.find(lambda m : m.id == reaction.user_id, guild.members)#找到按下表情符號的用戶
                await member.add_roles(role)#給身分組
@bot.event
async def on_raw_reaction_remove(reaction):#移除身分組, 步驟同上
    if reaction.message_id == 936461401453641769:
        if reaction.emoji.name == 'despise':
            guild = discord.utils.find(lambda g : g.id == reaction.guild_id, bot.guilds)
            role = discord.utils.get(guild.roles, name='成員')
            member = discord.utils.find(lambda m : m.id == reaction.user_id, guild.members)
            await member.remove_roles(role)

@bot.event
async def on_voice_state_update(member, before, after):#創建臨時語音頻道
    if before.channel is None and after.channel is not None:#如果空頻道有人進入
        if after.channel.id == 1052053922275151953:#指定初始頻道
            guild = after.channel.guild #guild(群組)為當前伺服器
            cat = discord.utils.get(guild.categories, name='語音聊天密道') #該群組中的頻道類別
            tempCh = await guild.create_voice_channel(f'{member.name}のチャンネル', category=cat, user_limit=None) #新增臨時頻道
            await member.move_to(tempCh) #把初始頻道裡的用戶拉到臨時頻道
    if before.channel is not None and after.channel is None:#如果有人離開語音頻道
        guild = before.channel.guild
        cat = discord.utils.get(guild.categories, name='語音聊天密道')
        if before.channel.category == cat:#如果是某特定類別的頻道
            if len(before.channel.members) == 0:#當人數為0
                await before.channel.delete() #刪除頻道

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

@bot.tree.command(name='greeting') #The name of the shown command
async def greet(interaction : discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.name}.', ephemeral=False)
#If ephemeral = True, that means only you can see the reply.

@bot.tree.command(name='speak')
@app_commands.describe(ctx = '114514')
async def speak(interaction: discord.Interaction, ctx: str):
    await interaction.response.send_message(f'{interaction.user.name} said : `{ctx}`.')

@bot.tree.command(name='schedule')
async def schedule(interaction: discord.Interaction):
    await interaction.response.send_message('Today, your schedule is :\n' + find_the_schedule(), ephemeral=False)

@bot.tree.command(name='weather')
async def weather(interaction: discord.interactions):
    sauceUrl = requests.get('https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-009?Authorization=rdec-key-123-45678-011121314&format=JSON')
    sauce = sauceUrl.text
    data = json.loads(sauce)
    sets = data['cwbopendata']['dataset']
    w = sets['parameterSet']['parameter'][0]['parameterValue']
    weatherEmoji = ''
    
    if '晴' in w:
        weatherEmoji += ':sunny: '
    if '寒流' in w:
        weatherEmoji += ':snowflake: '
    if '雲' in w or '陰' in w:
        if '晴' in w:
            if '雨' in w:
                weatherEmoji += ':white_sun_rain_cloud: '
            else:
                weatherEmoji += ':partly_sunny: '
        else:
            weatherEmoji += ':cloud: '
    if '寒冷' in w:
        weatherEmoji += ':cold_face: '
    if '保暖' in w:
        weatherEmoji += ':coat: '
    if '季風' in w or '涼' in w:
        weatherEmoji += ':wind_blowing_face: '
    if '有雨' in w:
        weatherEmoji += ':cloud_rain: '
    if '雨具' in w:
        weatherEmoji += ':umbrella: '
    
    reportEmbed = discord.Embed(color=discord.Color.blue(), title='本日天氣預報, ' + sets['datasetInfo']['issueTime'][:10] + sets['location']['locationName'], timestamp=datetime.datetime.now())
    reportEmbed.set_author(name=interaction.user.name).set_thumbnail(url=interaction.user.avatar.url)
    reportEmbed.add_field(name='你好, 我是你的天氣播報機器人, 以下將為您報告天氣狀況', value='今天的天氣狀況是------' + weatherEmoji, inline=False)
    
    for x in sets['parameterSet']['parameter']:
        reportEmbed.add_field(name='.', value=x['parameterValue'], inline=False)
    reportEmbed.set_footer(text='以上資訊由政府資料開放平台所提供')

    await interaction.response.send_message(embed=reportEmbed)

bot.run(json.load(open('hamToken.json', 'r'))['tokenPy'])