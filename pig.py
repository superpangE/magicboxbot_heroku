# discord, asyncio, bs4
import tierimage
def play(client):

    import discord
    import asyncio
    import random
    from discord.ext import commands
    import time
    import urllib.request
    from urllib.error import URLError, HTTPError
    from bs4 import BeautifulSoup
    import youtube_dl
    import re

    que = {}
    playerlist = {}
    playlist = list() #재생목록 리스트

    def queue(id): #음악 재생용 큐
        if que[id] != []:
            player = que[id].pop(0)
            playerlist[id] = player
            del playlist[0]
            player.start()

    @client.event
    async def on_ready():
        print("login")
        print(client.user.name)
        print(client.user.id)
        print("-----------------")
        await client.change_presence(status=discord.Status.online, activity=discord.Game('!명령어 설명'))

    @client.event
    async def on_message(message):

        #코드포스 대회 시간 보여줌
        if message.content == '!코포' or message.content == '!코드포스':
            try:
                newurl = ("http://codeforces.com/contests")
                newhtml = urllib.request.urlopen(newurl).read()

                bsObject = BeautifulSoup(newhtml, "html.parser")
            #502 bad gate 에러나 504 gateway time-out에러 잡기
            except HTTPError as e:
                if e.code == 502 or 504:
                    await message.channel.send("사용자문제 :)")

            #table이 하나밖에없어서 첫번째 table을 찾음
            table = bsObject.find("table")

            #table에서 'tr'태그를 모두 찾음
            tableprob = table.find_all('tr')

            #문제수 만큼 for문으로 반복 - 출력
            for idx, tr in enumerate(tableprob):
                if idx > 0 and idx < 4:
                    tds = tr.find_all('td')

                    #문제 이름의 텍스트만 probname에 담음
                    probname = tds[0].text.strip()

                    #시험 날짜 date에 담음
                    date = tds[2].text.strip()

                    #시험 시간 time에 담음
                    time = tds[3].text.strip()

                    #date 바꿔서 집어넣는 작업
                    utc = date.split(' ')[1]

                    #시간 변환
                    utch = int(utc.split(':')[0])
                    utcm = int(utc.split(':')[1])

                    dateurl = ("https://www.timeanddate.com/worldclock/fixedtime.html?day=12&month=5&year=2020&hour="+str(utch)+"&min="+str(utcm)+"&sec=0&p1=166")
                    datehtml = urllib.request.urlopen(dateurl).read()

                    dateObject = BeautifulSoup(datehtml, "html.parser")
                    newdate = dateObject.find_all("div", {"class": "evt-time"})[1]

                    clockdata = newdate.text
                    #heroku가 미국 서버라 한국에서 약간의 코드 변경
                    clock = clockdata.split(' ')[0]
                    clocktemp = int(clock.split(':')[0]) + 1
                    clockhour = str(clocktemp)
                    clockminutemp = clock.split(':')[1]
                    clockminu = clockminutemp[0:3]
                    resclock = "오후 " + clockhour + ":" + clockminu
                    realdate = str(date.split(' ')[0]) + " " + resclock
                    
                    embed = discord.Embed(color = discord.Color.blue())
                    embed.set_author(name = probname)
                    embed.add_field(name = "시간제한 : " + time, value = realdate, inline=False)

                    await message.channel.send(embed=embed)

        if message.content.startswith("!음악"): #음성채널에 봇을 추가 및 음악 재생
            msg = message.content.split(" ")
            try:
                url = msg[1]
                url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url) #정규 표현식을 사용해 url 검사
                if url1 == None:
                    await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: url을 제대로 입력해주세요.",colour = 0x2EFEF7))
                    return
            except IndexError:
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: url을 입력해주세요.",colour = 0x2EFEF7))
                return

            channel = message.author.voice.channel 
            server = message.guild
            voice_client = client.voice_client_in(server)

            if client.is_voice_connected(server) and not playerlist[server.id].is_playing(): #봇이 음성채널에 접속해있으나 음악을 재생하지 않을 때
                await voice_client.disconnect()
            elif client.is_voice_connected(server) and playerlist[server.id].is_playing(): #봇이 음성채널에 접속해있고 음악을 재생할 때
                player = await voice_client.create_ytdl_player(url,after=lambda:queue(server.id),before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                if server.id in que: #큐에 값이 들어있을 때
                    que[server.id].append(player)
                else: #큐에 값이 없을 때
                    que[server.id] = [player]
                await client.send_message(message.channel, embed=discord.Embed(title=":white_check_mark: 추가 완료!",colour = 0x2EFEF7))
                playlist.append(player.title) #재생목록에 제목 추가
                return

            try:
                voice_client = await client.join_voice_channel(channel)
            except discord.errors.InvalidArgument: #유저가 음성채널에 접속해있지 않을 때
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: 음성채널에 접속하고 사용해주세요.",colour = 0x2EFEF7))
                return

            try:
                player = await voice_client.create_ytdl_player(url,after=lambda:queue(server.id),before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                playerlist[server.id] = player
                playlist.append(player.title)
            except youtube_dl.utils.DownloadError: #유저가 제대로 된 유튜브 경로를 입력하지 않았을 때
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: 존재하지 않는 경로입니다.",colour = 0x2EFEF7))
                await voice_client.disconnect()
                return
            player.start()

        if message.content == "!종료": #음성채널에서 봇을 나가게 하기
            server = message.server
            voice_client = client.voice_client_in(server)

            if voice_client == None: #봇이 음성채널에 접속해있지 않았을 때
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: 봇이 음성채널에 없어요.",colour = 0x2EFEF7))
                return
            
            await client.send_message(message.channel, embed=discord.Embed(title=":mute: 채널에서 나갑니다.",colour = 0x2EFEF7)) #봇이 음성채널에 접속해있을 때
            await voice_client.disconnect()

        if message.content == "!스킵":
            id = message.server.id
            if not playerlist[id].is_playing(): #재생 중인 음악이 없을 때
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: 스킵할 음악이 없어요.",colour = 0x2EFEF7))
                return
            await client.send_message(message.channel, embed=discord.Embed(title=":mute: 스킵했어요.",colour = 0x2EFEF7))
            playerlist[id].stop()
        
        if message.content == "!목록":

            if playlist == []:
                await client.send_message(message.channel, embed=discord.Embed(title=":no_entry_sign: 재생목록이 없습니다.",colour = 0x2EFEF7))
                return

            playstr = "```css\n[재생목록]\n\n"
            for i in range(0, len(playlist)):
                playstr += str(i+1)+" : "+playlist[i]+"\n"
            await client.send_message(message.channel, playstr+"```")

        #백준 명령어를 통한 백준 티어 출력
        if message.content == '!백준':
            await message.channel.send(embed=discord.Embed(title="ID를 입력하새오", color=discord.Color.blue()))
            def pred(m):
                return m.author == message.author and m.channel == message.channel
            # 15초안에 입력하지않으면 다시입력하게만듬
            try:
                msg = await client.wait_for('message', check=pred, timeout=15.0)
            except asyncio.TimeoutError:
                await message.channel.send("시간초과ㅡㅡ")
            else:
                # discord에서 메시지를 파이썬에서 text만 받아오게함
                plus = ('{0.content}'.format(msg))
                
                # 입력에는 어짜피 영문밖에안들어가서 간단하게했는데, 한글로하면 다른작업 필요
                url = ("https://www.acmicpc.net/user/" + str(plus))
                try:
                    html = urllib.request.urlopen(url).read()
                    bsObject = BeautifulSoup(html, "html.parser")

                    #백준 홈페이지의 solvedac-tier 클래스를 가진 img의 src 정보를 가져옴
                    levelcheck = bsObject.find("img", {"class": "solvedac-tier"})
                    if levelcheck is None:
                        await message.channel.send("solved.ac에 백준 아이디를 등록해주세요")
                    else:
                        check_src = levelcheck["src"]
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/-1.svg":
                            level = "unranked"  
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/1.svg":
                            level = "bronze5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/2.svg":
                            level = "bronze4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/3.svg":
                            level = "bronze3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/4.svg":
                            level = "bronze2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/5.svg":
                            level = "bronze1"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/6.svg":
                            level = "silver5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/7.svg":
                            level = "silver4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/8.svg":
                            level = "silver3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/9.svg":
                            level = "silver2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/10.svg":
                            level = "silver1"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/11.svg":
                            level = "gold5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/12.svg":
                            level = "gold4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/13.svg":
                            level = "gold3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/14.svg":
                            level = "gold2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/15.svg":
                            level = "gold1"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/16.svg":
                            level = "platinum5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/17.svg":
                            level = "platinum4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/18.svg":
                            level = "platinum3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/19.svg":
                            level = "platinum2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/20.svg":
                            level = "platinum1"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/21.svg":
                            level = "diamond5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/22.svg":
                            level = "diamond4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/23.svg":
                            level = "diamond3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/24.svg":
                            level = "diamond2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/25.svg":
                            level = "diamond1"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/26.svg":
                            level = "ruby5"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/27.svg":
                            level = "ruby4"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/28.svg":
                            level = "ruby3"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/29.svg":
                            level = "ruby2"
                        if check_src == "https://d2gd6pc034wcta.cloudfront.net/tier/30.svg":
                            level = "ruby1"
                        
                        #tierimage.py에서 level에 맞는 이미지 가져오기
                        url1 = tierimage.tier(level)
                        #티어값 출력
                        embed = discord.Embed(color=discord.Color.blue())
                        embed.set_author(name=plus + "님의 티어는?")
                        embed.set_thumbnail(url=url1)
                        embed.add_field(
                            name=level, value="소라고동이 인증합니다🙂", inline=False)
                        await message.channel.send(embed=embed)

                    #403, 502, 504 에러
                except HTTPError as e:
                    if e.code == 502 or 504:
                        await message.channel.send("ID를 확인해주세요")
                    if e.code == 403:
                        await message.channel.send("조금 기다렸다 시도해주새오")

        #단순 응답 핑퐁
        if message.content.startswith('팡이'):
            await message.channel.send("멋쟁이")
        if message.content.startswith('!hellothisisverification'):
            await message.channel.send("민팡#2701")

        #소라고동에게 랜덤한 대답 기대
        if message.content.startswith('소라고동') or message.content.startswith('마법의'):

            randomNum = random.randrange(1, 4)
            if randomNum == 1:
                await message.channel.send(embed=discord.Embed(title="그래.", color=discord.Color.blue()))
            elif randomNum == 2:
                await message.channel.send(embed=discord.Embed(title="몰라.", color=discord.Color.green()))
            else:
                await message.channel.send(embed=discord.Embed(title="아니.", color=discord.Color.red()))

        #버전 / version 확인 가능
        if message.content == '!버전' or message.content == '!version':

            embed = discord.Embed(color = discord.Color.blue())
            embed.set_author(name = "마법의 소라고동 v3.0입니다.")
            embed.add_field(name = "최종수정 21-02-23", value = "도와주신분 : 구글", inline=False)
            await message.channel.send(embed=embed)

        #명령어 확인
        if message.content == '!명령어' or message.content == '!도움' or message.content == '!도움말' or message.content == '!help' or message.content == '!commands':

            embed = discord.Embed(color = discord.Color.blue())
            embed.set_author(name = "마법의 소라고동 v3.0 메뉴얼")
            embed.add_field(name = "백준 티어 확인", value = "!백준", inline=False)
            embed.add_field(name = "코드포스 예정 대회 확인", value = "!코포 or !코드포스", inline=False)
            embed.add_field(name = "소라고동 버전 확인", value = "!버전 or !version", inline=False)
            embed.add_field(name = "소라고동 명령어 확인", value = "!명령어", inline=False)
            embed.set_footer(text="많이 애용해주새오")
            await message.channel.send(embed=embed)

