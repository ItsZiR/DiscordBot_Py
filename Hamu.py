import discord, random, asyncio, datetime, json, requests
class MyClient(discord.Client):
    async def on_ready(self):#Log in
        print(f'{self.user}已上線, {datetime.datetime.now()}')#在Console印出上線訊息
        print('------')
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name='期末作業'))#更改狀態
        
    async def on_raw_reaction_add(self, reaction):#給身分組
        if reaction.message_id == 936461401453641769:#用id指定訊息
            if reaction.emoji.name == 'despise':#用名字指定表情符號
                guild = discord.utils.find(lambda g : g.id == reaction.guild_id, client.guilds)#找伺服器
                role = discord.utils.get(guild.roles, name='成員')#找伺服器中的身分組
                member = discord.utils.find(lambda m : m.id == reaction.user_id, guild.members)#找到按下表情符號的用戶
                await member.add_roles(role)#給身分組
    async def on_raw_reaction_remove(self, reaction):#移除身分組, 步驟同上
        if reaction.message_id == 936461401453641769:
            if reaction.emoji.name == 'despise':
                guild = discord.utils.find(lambda g : g.id == reaction.guild_id, client.guilds)
                role = discord.utils.get(guild.roles, name='成員')
                member = discord.utils.find(lambda m : m.id == reaction.user_id, guild.members)
                await member.remove_roles(role)
    
    async def on_voice_state_update(self, member, before, after):#創建臨時語音頻道
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

    async def on_message(self, msg):#監聽文字
        if msg.author.bot: return #無視bot發的內容
        async def sine(x):#勞改系統
            try:
                target = msg.mentions[0] #只選被tag到的第一個
            except:
                return
            jail = discord.utils.get(msg.guild.roles, name = '勞改營') #用身分組名字找該伺服器裡面的勞改營身分組
            LaogaiEmbed = discord.Embed(color=discord.Color.red()) #嵌入內容
            if not target or not jail:
                return
            elif jail in target.roles: 
                #如果已經被勞改的人再被勞改則無效
                LaogaiEmbed.set_author(name='正在勞改當中')
                await msg.channel.send(embed=LaogaiEmbed)
            else:
                ReleaseEmbed = discord.Embed(color=discord.Color.green())
                if target.id == 970910347223523348 or target.id == 503484838029033483: #機器人或自己被勞改則反彈回去
                    reflectEmbed = discord.Embed(title='你竟敢用我的魔法對付我，波特?', colour=discord.Color.red())
                    await msg.channel.send(embed=reflectEmbed)
                    await asyncio.sleep(2)
                    await msg.author.add_roles(jail)
                    target = msg.author
                    LaogaiEmbed.add_field(name=f'{target.name}#{target.discriminator}已被勞改', value=datetime.datetime.now(), inline=False)
                    await msg.channel.send(embed=LaogaiEmbed)
                else: #一般勞改
                    await target.add_roles(jail)
                    LaogaiEmbed.add_field(name=f'{msg.author.name}#{msg.author.discriminator}使用勞改系統, {target.name}#{target.discriminator}已被勞改, 持續 {x} 秒', value=datetime.datetime.now(), inline=False)
                    await msg.channel.send(embed=LaogaiEmbed)
                
                await asyncio.sleep(x) #數字代表勞改時間，以秒為單位
                await target.remove_roles(jail)
                ReleaseEmbed.add_field(name=f'{target.name}#{target.discriminator}已被解除勞改', value=datetime.datetime.now(), inline=False)
                await msg.channel.send(embed=ReleaseEmbed)
        
        async def manual():#產生說明書
            Manual = discord.Embed(color=discord.Color.green(), title='說明書/Manual/お手引き', url="https://youtu.be/dQw4w9WgXcQ", timestamp=datetime.datetime.now())
            Manual.set_author(name=client.get_user(503484838029033483), url="https://twitter.com/Zir_aguduzhe")
            Manual.set_thumbnail(url=self.user.avatar.url)
            Manual.add_field(name='文字、表情互動', value='偵測你發出的特定文字或表情後做回應', inline=True)
            Manual.add_field(name='給機率', value='訊息包含\'機率\'兩字就會隨機給1~100%', inline=True)
            Manual.add_field(name='隨機選擇', value='以\'隨機\'開頭,隨機抽出一個選擇\n格式: "隨機 選項一 選項二 ..."', inline=False)
            Manual.add_field(name='身分組管理', value='按下表情就能自動新增or移除身分組\n需手動先設定好指定使用的:伺服器,身分組,訊息,表情', inline=False)
            Manual.add_field(name='~ref', value='用此指令更新目前顯示的一般成員數量', inline=False)
            Manual.add_field(name='天氣播報', value='輸入~天氣\n播報今日氣象', inline=True)
            Manual.add_field(name='創建臨時語音頻道', value='自動新增、刪除臨時頻道', inline=True)
            Manual.add_field(name='勞改系統', value='~sine @勞改對象\n自動掛一個伺服器內的禁言身分組', inline=False)
            Manual.set_footer(text='Python期末作業，此機器人是由Discord.py所開發', icon_url=self.get_emoji(936249833143033946).url)
            await msg.channel.send(embed=Manual)
        
        async def weather():#天氣播報
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
            reportEmbed.set_author(name=self.user.name).set_thumbnail(url=self.user.avatar.url)
            reportEmbed.add_field(name='你好, 我是你的天氣播報機器人, 以下將為您報告天氣狀況', value='今天的天氣狀況是------' + weatherEmoji, inline=False)
            
            for x in sets['parameterSet']['parameter']:
                reportEmbed.add_field(name='.', value=x['parameterValue'], inline=False)
            reportEmbed.set_footer(text='以上資訊由政府資料開放平台所提供')
            await msg.channel.send(embed=reportEmbed, mention_author=False)
        
        #純文字互動
        if msg.content == '1':
            await msg.add_reaction('<:wtm:1058317486803652660>')
        if '我婆' in msg.content:
            await msg.reply('醒')
        if 'despise' in msg.content:
            await msg.add_reaction('<:despise:936249833143033946>')
        if 'naruto' in msg.content.lower():
            await msg.reply(str(self.get_emoji(918640300610682890)) + str(self.get_emoji(918640300614889512)), mention_author=False)       
        
        if '機率' in msg.content:#隨機給機率
            x = random.randint(1, 100)
            await msg.reply('機率為%d%%' % x, mention_author=False)
        
        if msg.content.startswith('隨機'):#隨機從選項抽出
            ctx = msg.content[3:].split(' ')
            if len(ctx) < 2:
                return
            else:
                random.shuffle(ctx)
                numx = random.randint(0, len(ctx)-1)
                await msg.channel.send(f'隨機 [ {msg.content[3:]} ]\n=> {ctx[numx]}')
        
        #特製指令集
        if msg.content.startswith('~'):
            cmd = msg.content[1:].split(' ')
            if cmd[0] == 'utils':
                await manual()
                await msg.delete()
            elif cmd[0] == 'sine':
                try:
                    if len(cmd) == 1:
                        return
                    elif not cmd[len(cmd)-1].isnumeric():
                        await msg.reply('失敗, 請確定是否有輸入持續時間', mention_author=False)
                    else:
                        await sine(int(cmd[len(cmd)-1]))
                        await msg.delete()
                except:
                    return
            elif cmd[0] == 'ref':
                role = discord.utils.get(msg.guild.roles, name='成員')
                await self.get_channel(936908251520466984).edit(name=f'目前成員人數 : {len(role.members)}')
                await msg.delete()
            elif cmd[0] == '天氣':
                await weather()
                await msg.delete()
                 
client = MyClient(intents=discord.Intents.all())
client.run(json.load(open('hamToken.json', 'r'))['tokenPy'])