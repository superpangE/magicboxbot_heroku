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
                    
                    clock = clockdata.split(' ')[0]
                    clocktemp = int(clock.split(':')[0]) + 1
                    clockhour = str(clocktemp)
                    clockminutemp = clock.split(':')[1]
                    clockminu = clockminutemp.split(' ')[0]
                    #clock = str(clockdata.split('.')[1])[0:3] + " " + str(clockdata.split('.')[0])
                    #clock = " " + str(clockdata.split('.')[0])
                    resclock = "오후 " + clockhour + ":" + clockminu
                    realdate = str(date.split(' ')[0]) + " " + resclock

                    embed = discord.Embed(color = discord.Color.blue())
                    embed.set_author(name = probname)
                    embed.add_field(name = "시간제한 : " + time, value = realdate, inline=False)

                    await message.channel.send(embed=embed)

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
                    check_src = levelcheck["src"]

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
                        await message.channel.send("사용자문제 :)")
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

