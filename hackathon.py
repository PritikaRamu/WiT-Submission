#application deployed in IBM Cloud Foundry


import json
import requests
import time
import urllib
from datetime import date
from datetime import datetime


#https://api.telegram.org/botTOKEN/getUpdates
TOKEN = #insert token ID of the chatbot
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
DATA=[]

#list of valid flat numbers
valid_address=['A201','A202','A203','A204','A301','A302','A303','A304','A401',
'A402','A403','A404','A501','A502','A503','A504','A601','A602','A603','A604',
'A701','A702','A703','A704','A801','A802','A803','A804','A901','A902','A903',
'A904','B001','B002','B003','B004','B101','B102','B103','B104','B201','B202',
'B203','B204','B301','B302','B303','B304','B401','B402','B403','B404','B501',
'B502','B503','B504','B601','B602','B603','B604','B701','B702','B703','B704',
'B801','B802','B803','B804','B901','B902','B903','B904','C001','C002','C101',
'C102','C201','C202','C301','C302','C401','C402','C501','C502','C601','C602',
'C701','C702','C801','C802','C901','C902','D001','D002','D003','D004','D005',
'D006','D101','D102','D103','D104','D105','D106','D201','D202','D203','D204',
'D205','D206','D301','D302','D303','D304','D305','D306','D401','D402','D403',
'D404','D405','D406','D501','D502','D503','D504','D505','D506','D601','D602',
'D603','D604','D605','D606','D701','D702','D703','D704','D705','D706','D801',
'D802','D803','D804','D805','D806','D901','D902','D903','D904','D905','D906',
'E101','E102','E103','E104','E201','E202','E203','E204','E301','E302','E303',
'E304','E401','E402','E403','E404','E501','E502','E503','E504','E601','E602',
'E603','E604','E701','E702','E703','E704','E801','E802','E803','E804','E901',
'E902','E903','E904','F401','F402','F403','F404','F501','F502','F503','F504',
'F601','F602','F603','F604','F701','F702','F703','F704','F801','F802','F803',
'F804','F901','F902','F903','F904']
TOKENS_COL=[]
ADMIN_ID=#insert chat id of admin group or individual (can be obtained from API)
RESIDENT_GROUP_ID=#insert chat id of resident group

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    try:
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = get_json_from_url(url)
        return js
    except Exception as e:
        print(e)

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#to check if entered flat number is valid
def validate_apt_no(apt_no):
    for va in valid_address:
        if(va==apt_no):
            return True
    return False

#to ensure no more than one token is given per flat
def unique_apt_no(apt_no):
    for token_res in DATA:
        if(token_res[1]==apt_no):
            return False
    return True

#to ensure no more than one token is given per user
def unique_chat_id(chat_id):
    for token_res in DATA:
        if(int(token_res[3])==chat_id):
            return False
    return True

def reset_last_update_id():
    try:
        h=open("last_update_id.txt",'r')
        last_update_id=int(h.read())
        h.close()
    except:
        last_update_id=None
    return last_update_id

def get_last_token():
    try:
        f=open('token_data.txt','r')
        content=f.read()
        f.close()
        content_list=content.split('\n')
        for i in content_list[:-1]:
            DATA.append(i.split('|'))
        token_id=len(content_list[:-1])
    except:
        token_id=0
    return token_id

def get_collected_tokens():
    try:
        f=open("collected_tokens.txt",'r')
        content=f.read()
        f.close()
        content_list=content.split('\n')
        for i in content_list[:-1]:
            TOKENS_COL.append(i)
        token_counter=len(content_list[:-1])
    except:
        token_counter=0
    return token_counter

def write_token(token_info):
    f=open('token_data.txt','a')
    string=''
    for info in token_info[:-1]:
        string+=str(info)+'|'
    string+=str(token_info[-1])+'\n'
    f.write(string)
    f.close()

#to give current status to resident
def current_status(chat_id,token_counter,last_token_id):
    int_tokens_col=[]
    for tok in TOKENS_COL:
        int_tokens_col.append(int(tok))
    int_tokens_col.sort()
    if(token_counter!=0):
        send_message("Total tokens issued: {} \nTokens Processed: {}\nMax Token Processed: {}".format(last_token_id,token_counter,int_tokens_col[-1]),chat_id)
    else:
        send_message("Total tokens issued: {} \nTokens Processed: {}".format(last_token_id,token_counter),chat_id)

#to give the complete list to resident
def list_all(chat_id):
    message='Issued Tokens List:\n'
    for info in DATA:
        message+=str(info[0]).rjust(3,'0')+" "+str(info[1])+" "+str(info[2])+'\n'
    message+="\nProcessed Token Numbers:\n"
    int_tokens_col=[]
    for tok in TOKENS_COL:
        int_tokens_col.append(int(tok))
    int_tokens_col.sort()
    for tok in int_tokens_col:
        message+=str(tok).rjust(3,' ')+", "
    if(len(int_tokens_col)==0):
        send_message(message,chat_id)
    else:
        send_message(message[:-2],chat_id)

#inform the admin as well as residents to request the next set of token holders to go
def inform_admin(token_counter):
    send_message("{} tokens have been processed. Please inform token holders {}-{}".format(token_counter,token_counter+6,token_counter+10),ADMIN_ID)
    send_message("{} tokens have been processed. Token holders {}-{}, please go down.".format(token_counter,token_counter+6,token_counter+10),RESIDENT_GROUP_ID)

#issue token after validating flat number and chat id
def issue_token(apt_no,chat_id,name,last_token_id):
    today = date.today()
    d = str(today.strftime("%d-%m-%Y"))
    if(validate_apt_no(apt_no)):
        if(unique_apt_no(apt_no)):
            if(unique_chat_id(chat_id)):
                last_token_id+=1
                DATA.append([last_token_id,apt_no,name,chat_id])
                write_token(DATA[last_token_id-1])
                send_message("Your token number is {} for the date {}.\nPlease maintain social distancing and wear a mask while shopping. Enter DONE after billing.".format(last_token_id,d),chat_id)
            else:
                send_message("Token has already been issued for you.",chat_id)
        else:
            send_message("Token has already been issued for this flat.",chat_id)
    else:
        send_message("Valid commands are:\n 1.Apt# (To Request Token e.g. D702)\n 2.Done (After Billing)\n 3.List All\n 4.Status",chat_id)
    return last_token_id

#increment the number of tokens collected i.e. when resident says "done"
def collect_token(chat_id,token_counter):
    if(unique_chat_id(chat_id)==False):
        token_no=str(get_index(chat_id))
        if(unique_token(token_no)):
            send_message("Thank you! Token number {} has been processed. Don't forget to wash your hands.".format(token_no),chat_id)
            f=open("collected_tokens.txt",'a')
            f.write(token_no+'\n')
            f.close()
            token_counter+=1
            TOKENS_COL.append(token_no)
        else:
            send_message('Token already processed',chat_id)
    else:
        send_message("Token not issued to this resident.",chat_id)
    return token_counter

def log_exception(function_name, e):
    f=open("Exception.txt",'a')
    f.write(function_name + ':' + str(e))
    f.close()

def unique_token(token):
    for tok in TOKENS_COL:
        if(tok==token):
            return False
    return True

def get_index(chat_id):
    for info in DATA:
        if(str(info[3])==str(chat_id)):
            return info[0]

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = reset_last_update_id()
    token_counter=get_collected_tokens()
    last_token_id=get_last_token()
    send_message("Server started",ADMIN_ID)
    updates=get_updates(last_update_id)
    flag=True
    today = date.today()
    e_bot_start_time = time.mktime(time.strptime(str(today.strftime("%d-%m-%Y")+"  08:00:00"), '%d-%m-%Y %H:%M:%S'))
    send_message("Server start time set as 8:00:00",ADMIN_ID)
    send_message("Token Issue start time set as 8:00:00. Use @*insert bot name* to request for token.",RESIDENT_GROUP_ID)
    while flag:
        updates = get_updates(last_update_id)
        if "result" in updates:
            if len(updates["result"]) > 0:
                for update in updates["result"]:
                    try:
                        chat = update["message"]["chat"]["id"]
                        epoch= update["message"]["date"]
                        if(epoch>=e_bot_start_time): #to ensure only requests after start time are processed
                            try:
                                type = update["message"]["chat"]["type"]
                                text = update["message"]["text"]
                            except:
                                continue
                            if(type=="private"):
                                name = update["message"]["chat"]["first_name"]
                                if(text.strip().upper()=='DONE'):
                                    token_counter_new=collect_token(chat,token_counter)
                                    if token_counter < token_counter_new:
                                        token_counter=token_counter_new
                                    if(token_counter==last_token_id):
                                        send_message("All tokens processed",ADMIN_ID)
                                elif((token_counter%5==0) and (token_counter!=0) and (token_counter+5<last_token_id)):
                                    inform_admin(token_counter)
                                elif(text=="/start"):
                                    send_message("Welcome to Token Management System\nValid commands are:\n 1.Apt# (To Request Token e.g. D702)\n 2.Done (After Billing)\n 3.List All\n 4.Status",chat)
                                elif(text.strip().upper()=='STATUS' or text.strip().upper()=='/STATUS'):
                                    current_status(chat,token_counter,last_token_id)
                                elif(text.strip().upper()=='LIST ALL' or text.strip().upper()=='/LIST ALL'):
                                    list_all(chat)
                                elif(text.strip().upper()=='/EXIT' and chat==ADMIN_ID):
                                    flag=False
                                    send_message("Thank you for using CCTMS",ADMIN_ID)
                                    break
                                elif(type=="private"):
                                    last_token_id=issue_token(text.strip().upper(),chat,name,last_token_id)
                                else:
                                    if(type!="supergroup"):
                                        send_message("Invalid Command",chat)
                                if((flag) or (text.strip().upper()=='/EXIT' and chat==ADMIN_ID)):
                                    if (flag):
                                        last_update_id = get_last_update_id(updates)+1
                        else:
                            send_message("Your request time is: {}\nPlease request for token after 8:00:00".format(time.strftime("%H:%M:%S ", time.localtime(epoch))),chat)
                    except Exception as e:
                        f=open("Exception.txt",'a')
                        f.write(str(e)+'\n')
                        f.close()
                        flag=False
                        break

                else:
                    last_update_id = update["update_id"]+1
                h=open("last_update_id.txt",'w')
                h.write(str(last_update_id))
                h.close()
        else:
            f=open("Exception.txt","a")
            f.write(str(updates)+'\n')
            f.close()
            time.sleep(90)
    time.sleep(1)

if __name__ == '__main__':
    main()
