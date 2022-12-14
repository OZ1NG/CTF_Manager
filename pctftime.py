#!/usr/bin/python3.11
# ctftime RSS parsing module
import requests
import xml.etree.ElementTree as ET
import datetime

class Pctftime:
    def __init__(self, max_parse_days=7):
        self.max_parse_days = max_parse_days # 파싱할 최대 일 수
        self.url = 'https://ctftime.org/'
        self.__headers = { # user-agent가 필수
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46"
        }
        self.upcoming_events_data = None 
        self.now_running_data = None     
        self.past_events_data = None     

    def get_img(self, img_url:str):
        url = self.url + img_url
        print(url)
        img_data = requests.get(url, headers=self.__headers).content
        return img_data

    def __parse_XML(self, xml_str:str):
        element = ET.fromstring(xml_str)
        channel = element.find("channel")
        if(channel == None):
            return -1 # parse error
        data = []
        for ctf in channel.findall("item"): # findall은 list 리턴
            if(abs(self.__checknow(ctf.find("start_date").text)[1]) > self.max_parse_days):
                continue
            tmp = {
                'ctf_title': ctf.find("title").text,
                'start_date': ctf.find("start_date").text,
                'finish_date': ctf.find("finish_date").text,
                'format_text': ctf.find("format_text").text,
                'ctf_url': ctf.find("url").text,
                'ctf_weight': ctf.find("weight").text
            }
            if(ctf.find("logo_url").text == None):
                tmp['logo_url'] = self.url + "static/images/ctftime-logo-avatar.png" 
            else:
                tmp['logo_url'] = self.url + ctf.find("logo_url").text 
            data.append(tmp)
        return data

    def parseRSS(self, url:str)->list:
        xml_str = requests.get(url, headers=self.__headers).content
        pdata = self.__parse_XML(xml_str)
        if(pdata == -1):
            print("[!] Parse Error!")
            return []
        return pdata
    
    # 현재시간과 남은 시간을 비교
    def __checknow(self, date)->datetime.timedelta:
        t = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S') - datetime.datetime.now()
        return str(t).split('.')[0], t.days

    # return format : [upcoming_events_data, past_events_data, now_running_data]
    def run(self): 
        now_running = self.url+"event/list/running/rss/"
        upcoming_events = self.url+"event/list/upcoming/rss/"
        past_events = self.url+"event/list/archive/rss/"
        self.now_running_data     = self.parseRSS(now_running)
        self.upcoming_events_data = self.parseRSS(upcoming_events) 
        self.past_events_data     = self.parseRSS(past_events) 
        return self.now_running_data, self.upcoming_events_data, self.past_events_data

# test
if __name__ == '__main__':
    print(f'[+] Start parsing RSS at CTFtime.org')
    pctf = Pctftime()
    res = pctf.run()[0]
    for r in res:
        print(r)
    #print(pctf.checknow('20221212T000000'))

