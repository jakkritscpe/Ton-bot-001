from flask import Flask, request, abort
import requests
import json
from Project.Config import *
from pprint import pprint

app = Flask(__name__)

API_HOST = 'https://api.bitkub.com'

@app.route('/')
def hello():
    return 'hello world ton',200

def getPriceCrypto(sym):
    res = requests.get(API_HOST + '/api/market/ticker')
    result = res.json()
    rs = result[sym]
    data = rs['last']  
    if data < 1000:
        txt = "ราคา {} ล่าสุด : {:,.3f} บาท".format(sym,data)
    else:
        txt = "ราคา {} ล่าสุด : {:,.0f} บาท".format(sym,data)
    return  txt

def getPriceCryptoAll(sym_all):
    res = requests.get(API_HOST + '/api/market/ticker')
    result = res.json()
    txt = ""
    num = 0 
    for sym in sym_all:
        rs = result[sym]
        data = rs['last'] 
        t = ""
        if data < 1000: 
            t += "{} : {:,.3f} Baht".format(sym,data)
        else:
            t += "{} : {:,.0f} Baht".format(sym,data)

        if num > 0 :
            txt += "\n" + t
        else:
            txt += t
        num += 1

    return  txt

def getPriceCryptoAllSort(sym_all):
    res = requests.get(API_HOST + '/api/market/ticker')
    result = res.json()
    d = {}
    for sym in sym_all:
        rs = result[sym]
        data = rs['last'] 
        d[sym] = data
    
    txt = ""
    num = 0 
    sorted_d = sorted(d.items(), key=lambda x: x[1])
    for i in sorted_d:
        t = ""
        if i[1] < 1000: 
            t += "{} : {:,.3f} Baht".format(i[0],i[1])
        else:
            t += "{} : {:,.0f} Baht".format(i[0],i[1])

        if num > 0 :
            txt += "\n" + t
        else:
            txt += t
        num += 1

    return  txt

def symCoineCrypto():
    res = requests.get(API_HOST + '/api/market/ticker')
    result = res.json()
    symCoinAll = []
    for name , _ in result.items():
        symCoinAll.append(name)
    return symCoinAll

def chekCoinList(allcoine,message):
    rs = False
    for c in allcoine:
        coine_name = c.split("_")
        if coine_name[1] in message:
            rs = True
    return rs


@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)

        all_coine = symCoineCrypto()
        
        if "ALL" == message.upper():
            Reply_messasge = getPriceCryptoAll(all_coine)
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif chekCoinList(all_coine,message.upper()):
            Reply_messasge = getPriceCrypto("THB_"+message.upper())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "ALLSORT" == message.upper():
            Reply_messasge = getPriceCryptoAllSort(all_coine)
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif "TIP" == message.upper():
            Reply_messasge = "น่าร๊าก <3"
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        else:
            Reply_messasge = "------- Help List Command -------"
            Reply_messasge +="\nชื่อเหรียญ : แสดงราคา เหรียญ หน่วย(Baht) "
            Reply_messasge +="\nAll : แสดงราคา Crypto ทั้งหมด หน่วย(Baht)"
            Reply_messasge +="\nAllSORT : แสดงราคา Crypto ทั้งหมด หน่วย(Baht) จากน้อยไปมาก"
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)

        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

# Use for fuction Send Message to Line Bot
# Reply_token : Token from User for Answer.
# TextMessage : Massage your want send to Line bot 
# Line_Acees_Token : Token from Line
def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken": Reply_token,
        "messages":[{
            "type":"text",
            "text": TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200