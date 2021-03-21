# discord, asyncio, bs4
import tierimage
def play(bot):

    import discord
    import asyncio
    import random
    import time
    import urllib.request
    import youtube_dl
    import os
    from discord.utils import get   
    from youtube_dl import YoutubeDL
    from urllib.error import URLError, HTTPError
    from discord import FFmpegPCMAudio
    from bs4 import BeautifulSoup
    from discord.ext import commands

    @bot.command()
    async def 코포(ctx):
        try:
            newurl = ("http://codeforces.com/contests")
            newhtml = urllib.request.urlopen(newurl).read()

            bsObject = BeautifulSoup(newhtml, "html.parser")
        #502 bad gate 에러나 504 gateway time-out에러 잡기
        except HTTPError as e:
            if e.code == 502 or 504:
                await ctx.send("사용자문제 :)")

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

                await ctx.send(embed=embed)
    @bot.command()
    async def 코드포스(ctx):
        await 코포(ctx)
    @bot.command()
    async def ㅋㅍ(ctx):
        await 코포(ctx)

    @bot.command()
    async def 백준(ctx):
        await ctx.channel.send(embed=discord.Embed(title="ID를 입력하새오", color=discord.Color.blue()))
        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel
        # 15초안에 입력하지않으면 다시입력하게만듬
        try:
            msg = await bot.wait_for('message', check=pred, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.channel.send("시간초과ㅡㅡ")
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
                    await ctx.channel.send("solved.ac에 백준 아이디를 등록해주세요")
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
                    await ctx.send(embed=embed)

                #403, 502, 504 에러
            except HTTPError as e:
                if e.code == 502 or 504:
                    await ctx.send("ID를 확인해주세요")
                if e.code == 403:
                    await ctx.send("조금 기다렸다 시도해주새오")

    @bot.command()
    async def hellothisisverification(ctx):
        await ctx.send("민팡#2701")

    @bot.command()
    async def 버전(ctx):
        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name = "마법의 소라고동 v3.1입니다.")
        embed.add_field(name = "최종수정 21-03-21", value = "도와주신분 : 구글", inline=False)
        await ctx.send(embed=embed)

    @bot.command()
    async def version(ctx):
        await 버전(ctx)

    @bot.command()
    async def 명령어(ctx):
        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name = "마법의 소라고동 v3.1 메뉴얼")
        embed.add_field(name = "백준 티어 확인", value = "!백준", inline=False)
        embed.add_field(name = "코드포스 예정 대회 확인", value = "!코포 or !코드포스", inline=False)
        embed.add_field(name = "소라고동 버전 확인", value = "!버전 or !version", inline=False)
        embed.add_field(name = "소라고동 명령어 확인", value = "!명령어", inline=False)
        embed.set_footer(text="많이 애용해주새오")
        await ctx.send(embed=embed)

    @bot.command()
    async def 도움말(ctx):
        await 명령어(ctx)
    @bot.command()
    async def commands(ctx):
        await 명령어(ctx)


    @bot.command()
    async def play(ctx, *, url):
        print(ctx.message)
        print(ctx.message.author)
        print(ctx.message.author.voice)
        print(ctx.message.author.voice.channel)
        try:
            global vc
            vc = await ctx.message.author.voice.channel.connect()
        except:
            # try:
            await vc.move_to(ctx.message.author.voice.channel)
            # except:
            #     await ctx.send("Nobody in Channel!!")

        YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        if not vc.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        else:
            await ctx.send("Music is already running!")

    @bot.command()
    async def leave(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("konch is not connected to a voice channel!")

    @bot.command()
    async def pause(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing")

    @bot.command()
    async def resume(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused")

    @bot.command()
    async def stop(ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()

 