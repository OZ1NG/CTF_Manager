#!/usr/bin/python3.11
# ctf manager utils
import datetime

# 1초마다 현재 시간 체크
# min:int : 0~59
def checkminute(now:datetime.datetime, min:int=5)->bool: # min : 체크할 시간 값
    if((now.minute % min == 0) and now.second == 0):     # 0분 0초면 참 리턴
        return True
    return False

# 오전 9시인지 체크
def check9o(now:datetime.datetime):
    if(now.hour == 9):
        return True
    return False

def __str2date(date:str):        
    date_time_obj = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S') + datetime.timedelta(hours=9)
    return date_time_obj.strftime("%Y/%m/%d, %H:%M:%S")

# 현재시간과 남은 시간을 비교
# type: start=시작시간, finish=종료시간
def checknow(date:str)->datetime.timedelta:
    t = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S') - datetime.datetime.now()
    if(t.days < 0):
        return None
    return str(t).split('.')[0]

def create_desciprtion(parse_data:dict, remain_flag=True):
    desc = ''                                       
    desc += "[CTF Title]    : " + parse_data['ctf_title']                   + '\n'        # ctf 제목
    desc += "[URL]          : " + parse_data['ctf_url']                     + '\n'        # ctf url
    desc += "[Form]         : " + parse_data['format_text']                 + '\n'        # ctf 종류 ex)Jeopardy
    desc += "[Weight]       : " + parse_data['ctf_weight']                  + '\n'        # ctf weight
    desc += "[Start Date]   : " + __str2date(parse_data['start_date'])   + ' (KST) \n'    # 시작 시간
    desc += "[Finish Date]  : " + __str2date(parse_data['finish_date'])  + ' (KST) \n'    # 종료 시간
    if(remain_flag==True):
        sd_chk = checknow(parse_data['start_date'])
        if(sd_chk == None):
            desc += "[Start Remaining]   : " + "Already Started"   + ' \n' # 시작까지 남은 시간
        else:
            desc += "[Start Remaining]   : " + sd_chk   + ' \n' # 이미 시작함

        fd_chk = checknow(parse_data['finish_date'])
        if(fd_chk == None):
            desc += "[Finish Remaining]  : " + "Already Ended"  + ' \n' # 종료까지 남은 시간
        else:
            desc += "[Finish Remaining]  : " + fd_chk  + ' \n' # 이미 끝남
    return desc

