import sqlite3
import os

class DBManager():
    def __init__(self, dbpath='./db', dbname="ctfmanager.db") -> None:
        self.__create_directory(dbpath)
        self.dbpath = f"{dbpath}/{dbname}"
        self.DB = sqlite3.connect(self.dbpath)
        self.cursor = self.DB.cursor()
        self.db_init()

    def __create_directory(self, dbpath):
      if not os.path.exists(dbpath):
        os.makedirs(dbpath)

    def db_init(self):
        try:
            self.cursor.execute("CREATE TABLE msg_info(channel_id, msg_id, ctf_title, ctf_url, format_text, ctf_weight, start_date, finish_date)") # info table
        except sqlite3.OperationalError: # table already exists
            pass

    # 채널 id 추가
    def add_data(self, channel_id:int, msg_id:int, ctf_title:str, ctf_url:str, format_text:str, ctf_weight:str, start_date:str, finish_date:str):
        if(self.__chk_overlap(msg_id)): 
            return False 
        self.cursor.execute(f"INSERT INTO msg_info(channel_id, msg_id, ctf_title, ctf_url, format_text, ctf_weight, start_date, finish_date) VALUES ('{channel_id}', '{msg_id}', '{ctf_title}', '{ctf_url}', '{format_text}', '{ctf_weight}', '{start_date}', '{finish_date}')")
        self.DB.commit()
        return True

    def update_data(self, msg_id:int, src:str, dest:str):
        # 메시지 정보가 있는지 확인
        if(not self.__chk_overlap(msg_id)):
            return False 
        self.cursor.execute(f"UPDATE msg_info SET {src}='{dest}' WHERE msg_id='{msg_id}'")
        self.DB.commit()
        return True

    def delete_data(self, msg_id:int):
        self.cursor.execute(f"DELETE FROM msg_info WHERE msg_id='{msg_id}'")
        self.DB.commit()
        # 제대로 제거 되었는지 체크
        if(self.__chk_overlap(msg_id)):
            return False # 모종의 이유로 제거 실패
        return True

    def delete_channel_data(self, channel_id:int):
        self.cursor.execute(f"DELETE FROM msg_info WHERE channel_id='{channel_id}'")
        self.DB.commit()
        # 제대로 제거 되었는지 체크
        if(self.__chk_overlap_channel_id(channel_id)):
            return False # 모종의 이유로 제거 실패
        return True

    def search_data(self, msg_id:int):
        res = self.cursor.execute(f"SELECT ctf_title,ctf_url,format_text,ctf_weight,start_date,finish_date FROM msg_info WHERE msg_id='{msg_id}'")
        find = res.fetchall()
        return find

    # 모든 채널에 대한 msg id를 전부 가져옴
    def get_all_msg_id(self):
        res = self.cursor.execute(f"SELECT msg_id FROM msg_info")
        find = res.fetchall()
        result:list[int] = [int(f[0]) for f in find]
        return result

    # 모든 채널 id를 전부 가져옴
    def get_all_channel_id(self):
        res = self.cursor.execute(f"SELECT channel_id FROM msg_info")
        find = res.fetchall()
        result:list[int] = [int(f[0]) for f in find]
        return list(set(result)) # 중복 제거

    # 채널 id에 대한 msg id를 전부 가져옴
    def get_msg_id(self, channel_id:int):
        res = self.cursor.execute(f"SELECT msg_id FROM msg_info WHERE channel_id='{channel_id}'")
        find = res.fetchall()
        result:list[int] = [int(f[0]) for f in find]
        return result

    # db msg_id 중복 체크 # private
    # 리턴 : 값이 있으면 참, 없으면 거짓
    def __chk_overlap(self, msg_id:int):
        res = self.cursor.execute(f"SELECT msg_id FROM msg_info WHERE msg_id='{msg_id}'")
        find = res.fetchall()
        if(len(find) == 0):
            return False
        return True

    # db channel_id 중복 체크 # private
    # 리턴 : 값이 있으면 참, 없으면 거짓
    def __chk_overlap_channel_id(self, channel_id:int):
        res = self.cursor.execute(f"SELECT channel_id FROM msg_info WHERE channel_id='{channel_id}'")
        find = res.fetchall()
        if(len(find) == 0):
            return False
        return True

    # 리턴 : 값이 있으면 참, 없으면 거짓
    def is_ctf_title(self, channel_id:int, ctf_title:str):
        res = self.cursor.execute(f"SELECT ctf_title FROM msg_info WHERE channel_id='{channel_id}' AND ctf_title='{ctf_title}'")
        find = res.fetchall()
        if(len(find) == 0):
            return False
        return True

    def close(self):
        self.DB.close()

# test
if __name__ == "__main__":
    dbm = DBManager(dbname="test.db")
    #dbm = DBManager()

    # # add test : OK
    res = dbm.add_data(1111, 1111, "test1", "3333", "4444" , "5555", "6666", "7777")
    res = dbm.add_data(1111, 2222, "test1", "3333", "4444" , "5555", "6666", "7777")
    res = dbm.add_data(2222, 3333, "test2", "3333", "4444" , "5555", "6666", "7777")
    #print(res)

    # search test : OK
    # print(dbm.search_data(2222))

    # update test : OK
    ## change : OK
    # print(dbm.update_data(5678, 'ctf_title', 'test2'))
    # print(dbm.search_data(5678))

    # delete test : OK
    # dbm.delete_data(5678)
    # print(dbm.search_data(5678))

    # get_all_msg_id test : OK
    # print(dbm.get_all_msg_id())

    # get_all_id test : OK
    # print(dbm.get_msg_id(1111))

    # is_ctf_title test : OK
    # print(dbm.is_ctf_title(1111, 'test2'))

    #dbm.delete_channel_data(1111)

    print(dbm.get_all_channel_id())

