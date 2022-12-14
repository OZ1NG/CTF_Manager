#!/usr/bin/python3.11
import discord
from discord.ext import commands
from discord.ext import tasks
import pctftime
import datetime
import util
import database
import asyncio

TOKEN = <Your Token>

intents = discord.Intents.default()

# !로 시작하면 명령어로 인식
bot = commands.Bot(command_prefix='!', intents=intents)

PCTF = pctftime.Pctftime()

DB = database.DBManager()

CC_LIST:list[discord.channel.TextChannel] = [] # connect channel list

# TODO: 기존에 없는 데이터가 존재하면 해당 데이터 send
def add_new_data(channel_id:int ,msg:discord.Message, newdata:dict):
    print(f"{msg.content}:{msg.channel}:{msg.id}")
    # TODO: 추가된 데이터 데이터베이스에 추가
    DB.add_data(channel_id, msg.id, newdata['ctf_title'], newdata['ctf_url'], newdata['format_text'], newdata['ctf_weight'], newdata['start_date'], newdata['finish_date'])

# 1분 마다 새로운 데이터 파싱 후 전송
@tasks.loop(minutes=1)
async def run():
    global CC_LIST

    for ch in CC_LIST:
        # 기존 메시지 수정 (시간 정보)
        msg_id_list = DB.get_msg_id(ch.id)
        for id in msg_id_list:
            try:
                msg = await ch.fetch_message(id)
            except discord.errors.NotFound:
                continue
            data = DB.search_data(id)
            if(len(data) > 0):
                #print(data)
                tmp = {
                    'ctf_title':   data[0][0],
                    'ctf_url':     data[0][1],
                    'format_text': data[0][2],
                    'ctf_weight':  data[0][3],
                    'start_date':  data[0][4],
                    'finish_date': data[0][5]
                }
                await msg.edit(content=util.create_desciprtion(tmp)) # 메세지 수정
                # 모든게 끝난 대회인지 체크
                if(util.checknow(tmp['finish_date']) == None):
                    DB.delete_data(id)

        now_running, upcoming, past = PCTF.run()
        # 새로운 데이터가 있는지 확인 (CTF 이름으로 비교)
        # 해당 채널에서 새로운 데이터인지를 판별 후 전송
        for nd in now_running:
            if(not DB.is_ctf_title(ch.id, nd['ctf_title'])): # False면 새로운 데이터
                # 기존에 없는 데이터가 존재하면 해당 데이터 send
                if(nd['logo_url'] != None):
                    await ch.send(nd['logo_url'])
                msg = await ch.send(util.create_desciprtion(nd))
                add_new_data(ch.id, msg, nd)
        for nd in upcoming:
            if(not DB.is_ctf_title(ch.id, nd['ctf_title'])): # False면 새로운 데이터
                # 기존에 없는 데이터가 존재하면 해당 데이터 send
                if(nd['logo_url'] != None):
                    await ch.send(nd['logo_url'])
                msg = await ch.send(util.create_desciprtion(nd))
                add_new_data(ch.id, msg, nd)

# 5분 마다 새롭게 채널 리스트를 받아옴
@tasks.loop(minutes=5)
async def get_channel_list():
    global CC_LIST
    # 모든 채널리스트를 가져온 후 특정 토픽이 설정된 채널만 골라냄
    print(f'[+] Get Channel List...')
    tmp:list[discord.channel.TextChannel] = [] 
    chs = bot.get_all_channels()
    for ch in chs:
        if((ch.type.name == 'text') and (ch.topic != None) and ("#ctftime_P" in ch.topic)): # 텍스트 채널 구분
            #print(f"{ch.name}:{ch.topic}:{ch.id}") # test
            cc = bot.get_channel(ch.id) # connect channel 
            tmp.append(cc)
    CC_LIST = tmp

@bot.event
async def on_ready(): # 봇이 처음 시작할 때 실행되는 함수
    global CC_LIST

    print(f'[+] logged in as {bot.user}')

    get_channel_list.start()
    await asyncio.sleep(3) # 동기 문제가 발생할 수 있기 때문에 3초 후 진행

    print(f'[+] Parse Start!')
    run.start()

# !hello 명령어 처리 - DM
@bot.command()
async def hello(ctx:discord.Message):
    await ctx.reply('Hi, there!')

# TODO: !help 명령어 처리 - DM

bot.run(TOKEN)
