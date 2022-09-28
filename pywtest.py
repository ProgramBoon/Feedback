import os

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

import database



def ShowFiles(id):

    listOfFiles = database.Database.GetFiles(id)
    if listOfFiles !=[]:
        put_button("Просмотреть файлы",onclick=lambda: Show2Files(id))


def Show2Files(id):
    listOfFiles = database.Database.GetFiles(id)

    with popup('Файлы', implicit_close=True) as s:
        for file in listOfFiles:
            content = open(file[0], 'rb').read()
            x = file[0].split("/")[-1]
            # print(x[-1])
            put_file(file[0].split("/")[-1], content)



def check_num(p):  # return None when the check passes, otherwise return the error message

    nummerList = []
    numbers = database.Database.GetTreadNumbers()
    for num in numbers:
        nummerList.append(num[0])

    if nummerList.count(p) == 0:
        return 'Диалога с таким номером не существует'

def Responce(numberOfTread):
    info = input_group("Ответ", [
        input('Тема', name='theme',required=True),
        input('Сообщение', name='message',required=True),
        file_upload(label="Файлы", placeholder="Добавьте файлы", multiple=True, name='files')
    ])
    try:
        # database.Database.PutReply(numberOfTread,info['theme'],info['message'],info['files'])
        database.Database.Put(info['theme'], info['message'], info['files'],numberOfTread)

    except Exception as e:
        print(e)


    # print(info['theme'], info['message'],info['files'])



def check():
    numberGet = input("Введите номер диалога", type=NUMBER, required=True, validate=check_num)

    Messages = database.Database.GetTreadMessages(numberGet)

    tmplist = []
    t = 0
    for message in Messages:
        tmplist.append(message[0])


        put_collapse((message[1].strftime("%m/%d/%Y, %H:%M:%S")+" "+message[3]), put_table([
            ["Тема","Дата","Сообщение","Файлы"],
            [(message[3]),message[1].strftime("%Y-%m-%d"),message[4], ShowFiles(message[0])]]))
        t+=1

    put_button("Добавить ответ",onclick=lambda : Responce(numberGet))


def send():
    info = input_group("Сообщение", [
        input('Тема', name='theme', required=True),
        input('Сообщение', name='message', required=True),
        file_upload(label="Файлы", placeholder="Добавьте файлы", multiple=True, name='files')
    ])
    try:
        treadid = database.Database.Put(info['theme'], info['message'], info['files'])
        # treadid = database.Database.PutFirstMessage(info['theme'], info['message'], info['files'])
        popup("Номер диалога", str(treadid))
        send()
    except Exception as e:
        print(e)


def index():
    put_link('Отправить отзыв', app='send')  # Use `app` parameter to specify the task name
    put_text(" ")

    put_link('Просмотреть отзывы', app='check')



start_server([index,send,check], port=8080, debug=True)




# for mes in Messages:
#     print(mes)







