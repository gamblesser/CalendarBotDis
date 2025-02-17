import discord
from discord.ext import commands, tasks
import datetime
from googleapiclient.discovery import build
import itertools
import locale
import os
import collections
from threading import Thread
import asyncio
from flask import Flask, render_template
import collections
from typing import Optional
import copy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey,JSON,BigInteger
from sqlalchemy.orm import relationship
import json
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from json import JSONEncoder
from json import JSONDecoder
import random
from discord import app_commands
from dotenv import load_dotenv

import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)


@app.route("/")
def index():
    return """<body style="margin: 0; padding: 0;">
       
  </body>"""







load_dotenv() 
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
URL0=os.getenv("URL0")
URL1 = os.getenv("URL1")
URL2 = os.getenv("URL2")
URL3 = os.getenv("URL3")
url = 'mysql://{0}:{1}@{2}:{3}'.format(URL0,URL1, URL2, URL3)
engine = sqlalchemy.create_engine(url)
Session = sessionmaker(bind=engine)

Base = declarative_base()








bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


   
class DecodeDateTime(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    
    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d

class TextChannels(Base):
    __tablename__ = 'textChannels'

    id = Column(String(255), primary_key=True)
    relation = relationship("DataFor_TextChannels",cascade='all, delete-orphan', uselist=False, back_populates="person")


class Names(Base):
    __tablename__ = 'names'

    id = Column(String(255), primary_key=True)
    relation = relationship("DataFor_Names",cascade='all, delete-orphan', uselist=False, back_populates="person")



class DataFor_TextChannels(Base):
    __tablename__ = 'dataTextChannels'

    id = Column(Integer, primary_key=True)
    relationID= Column(String(255), ForeignKey('textChannels.id'))
    person = relationship("TextChannels", back_populates="relation")
    guild = Column(String(255))
    role = Column(String(255))
    channel = Column(String(255))
    GOOGLE_API_KEY = Column(String(255))
    GOOGLE_CALENDAR_ID = Column(String(255))
    NAMES = Column(String(255))
    cache = Column(JSON)
    lenUsers = Column(String(255))
    language = Column(String(255))
    
    def __init__(self, guild, role,channel,GOOGLE_API_KEY,GOOGLE_CALENDAR_ID,NAMES,cache,lenUsers,language):
        self.guild = guild
        self.role = role
        self.channel = channel
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.GOOGLE_CALENDAR_ID = GOOGLE_CALENDAR_ID
        self.NAMES = NAMES
        self.cache = cache
        self.lenUsers = lenUsers
        self.language = language

class DataFor_Names(Base):
    __tablename__ = 'dataNames'

    id = Column(Integer, primary_key=True)
    relationID= Column(String(255), ForeignKey('names.id'))
    person = relationship("Names", back_populates="relation")
    GOOGLE_API_KEY = Column(String(255))
    GOOGLE_CALENDAR_ID = Column(String(255))
    NAMES = Column(String(255))
    language = Column(String(255))
    def __init__(self,GOOGLE_API_KEY,GOOGLE_CALENDAR_ID,NAMES,language):

        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.GOOGLE_CALENDAR_ID = GOOGLE_CALENDAR_ID
        self.NAMES = NAMES
        self.language = language


languages = {"rus":{"month_declensions":{
    "january": "января",
    "february": "февраля",
    "march": "марта",
    "april": "апреля",
    "may": "мая",
    "june": "июня",
    "july": "июля",
    "august": "августа",
    "september": "сентября",
    "october": "октября",
    "november": "ноября",
    "december": "декабря",
},"weekday_declensions":{
    "monday": "понедельника",
    "tuesday": "вторника",
    "wednesday": "среды",
    "thursday": "четверга",
    "friday": "пятницы",
    "saturday": "субботы",
    "sunday": "воскресенья",
},"labelbtn1":"Буду!","labelbtn2":"Уведомляю за другого!","labelbtn3":"Участник не может","titleCalReg":"Регистрация календаря","titleCalEdit":"Редактирование конфигурации","modalLab1":"Введите Апи ключ Гула","modalPh1":"Введите ваш Гугл апи ключ","modalLab2":"Айди календаря","modalPh2":"Введите айди календаря","modalLab3":"Почта:Ник ваших пользователей","modalPh3":"Введите Почта:Ник ваших пользователей","modalLab4":"Количество участников календаря","modalPh4":"Введите количество участников календаря","modalLab5":"Роль для рассылки уведомлений","modalPh5":"Введите Роль","noneOfThem1":"Не у кого из","noneOfTheem2":"нет свободного времени на ролку или они забыли добавить в календарь","success":"Успех!","titleAddUserModal":"Ввидите пользователя,которого нужно добавить","modalLabAddUser":"Ник пользователя","modalPhAddUser":"Введите пользователя","notedUsers":"Отметившийся Участники","intervalsTimeCould":"Промежутки времени когда может","intervalsTimecouldnt":"Расписание когда не могут люди","allMay":"У всех все свободно","couldIn":"может в","timeing":"Время","from":"с","by":"по","to":"до","and":" и ","couldntIn":"не может в","uploadTimeCouldnt":"ОБНОВЛЕНИЕ В РАСПИСАНИИ КОГДА НЕ МОГУТ!","uploadTimeCould":"ОБНОВЛЕНИЕ В РАСПИСАНИИ","noActualDataTime":"Дата и время больше не актуальна","nothigNoted":"Никто не отметился","chooseCouldnt":"Выберите кто не может","allCould":"ВСЕ МОГУТ","deleted":"Удалено!",'oldBtn':"Кнопка устарела","uploadSuccesful":"Обновление прошло успешно!"
},"eng": {
        "month_declensions": {
            "january": "January",
            "february": "February",
            "march": "March",
            "april": "April",
            "may": "May",
            "june": "June",
            "july": "July",
            "august": "August",
            "september": "September",
            "october": "October",
            "november": "November",
            "december": "December",
        },
        "weekday_declensions": {
            "monday": "Monday",
            "tuesday": "Tuesday",
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday",
            "saturday": "Saturday",
            "sunday": "Sunday",
        },
        "labelbtn1": "I'll attend!",
        "labelbtn2": "Notify for another!",
        "labelbtn3": "Can't attend",
        "titleCalReg": "Calendar Registration",
        "titleCalEdit": "Configuration Editing",
        "modalLab1": "Enter Google API Key",
        "modalPh1": "Enter your Google API key",
        "modalLab2": "Calendar ID",
        "modalPh2": "Enter calendar ID",
        "modalLab3": "Email:Nickname of your users",
        "modalPh3": "Enter Email:Nickname of your users",
        "modalLab4": "Number of calendar participants",
        "modalPh4": "Enter number of participants",
        "modalLab5": "Role for notification distribution",
        "modalPh5": "Enter Role",
        "noneOfThem1": "None of them",
        "noneOfTheem2": "have free time or forgot to add it to the calendar",
        "success": "Success!",
        "titleAddUserModal": "Enter the user to add",
        "modalLabAddUser": "User Nickname",
        "modalPhAddUser": "Enter user nickname",
        "notedUsers": "Marked Participants",
        "intervalsTimeCould": "Time intervals when they can",
        "intervalsTimecouldnt": "Schedule when people cannot",
        "allMay": "All are free",
        "couldIn": "can in",
        "timeing": "Time",
        "from": "from",
        "by": "by",
        "to": "to",
        'oldBtn':"The button is obsolete",
        "and": " and ",
        "couldntIn": "can't in",
        "uploadTimeCouldnt": "UPDATE OF SCHEDULE WHEN CANNOT!",
        "uploadTimeCould": "SCHEDULE UPDATE",
        "noActualDataTime": "Date and time are no longer relevant",
        "nothigNoted": "No one has marked",
        "chooseCouldnt": "Choose who cannot",
        "allCould": "ALL CAN",
        "deleted": "Deleted!",
        "uploadSuccesful": "Update successful!"
    },"es": {
        "month_declensions": {
            "january": "Enero",
            "february": "Febrero",
            "march": "Marzo",
            "april": "Abril",
            "may": "Mayo",
            "june": "Junio",
            "july": "Julio",
            "august": "Agosto",
            "september": "Septiembre",
            "october": "Octubre",
            "november": "Noviembre",
            "december": "Diciembre",
        },
        "weekday_declensions": {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
        },
        "labelbtn1": "¡Asistiré!",
        "labelbtn2": "Notificar por otro",
        "labelbtn3": "No puedo asistir",
        "titleCalReg": "Registro de calendario",
        "titleCalEdit": "Edición de configuración",
        "modalLab1": "Ingrese Clave API de Google",
        "modalPh1": "Ingrese su clave API de Google",
        "modalLab2": "ID del calendario",
        'oldBtn':"El botón está obsoleto",
        "modalPh2": "Ingrese ID del calendario",
        "modalLab3": "Correo:Apodo de tus usuarios",
        "modalPh3": "Ingrese Correo:Apodo de tus usuarios",
        "modalLab4": "Número de participantes",
        "modalPh4": "Ingrese número de participantes",
        "modalLab5": "Rol para la notificación",
        "modalPh5": "Ingrese Rol",
        "noneOfThem1": "Ninguno de ellos",
        "noneOfTheem2": "tiene tiempo libre o se olvidó de agregarlo al calendario",
        "success": "¡Éxito!",
        "titleAddUserModal": "Ingrese el usuario a agregar",
        "modalLabAddUser": "Apodo del usuario",
        "modalPhAddUser": "Ingrese el apodo del usuario",
        "notedUsers": "Participantes marcados",
        "intervalsTimeCould": "Intervalos de tiempo cuando pueden",
        "intervalsTimecouldnt": "Horario cuando no pueden",
        "allMay": "Todos están libres",
        "couldIn": "puede en",
        "timeing": "Hora",
        "from": "de",
        "by": "por",
        "to": "a",
        "and": " y ",
        "couldntIn": "no puede en",
        "uploadTimeCouldnt": "¡ACTUALIZACIÓN DEL HORARIO CUANDO NO PUEDEN!",
        "uploadTimeCould": "ACTUALIZACIÓN DEL HORARIO",
        "noActualDataTime": "La fecha y hora ya no son relevantes",
        "nothigNoted": "Nadie ha marcado",
        "chooseCouldnt": "Elija quién no puede",
        "allCould": "TODOS PUEDEN",
        "deleted": "¡Eliminado!",
        "uploadSuccesful": "¡Actualización exitosa!"
    },"zh": {
        "month_declensions": {
            "january": "一月",
            "february": "二月",
            "march": "三月",
            "april": "四月",
            "may": "五月",
            "june": "六月",
            "july": "七月",
            "august": "八月",
            "september": "九月",
            "october": "十月",
            "november": "十一月",
            "december": "十二月",
        },
        "weekday_declensions": {
            "monday": "星期一",
            "tuesday": "星期二",
            "wednesday": "星期三",
            "thursday": "星期四",
            "friday": "星期五",
            "saturday": "星期六",
            "sunday": "星期日",
        },
        "labelbtn1": "我会参加!",
        "labelbtn2": "为他人通知!",
        "labelbtn3": "不能参加",
        "titleCalReg": "日历注册",
        "titleCalEdit": "配置编辑",
        "modalLab1": "输入 Google API 密钥",
        "modalPh1": "输入您的谷歌API密钥",
        "modalLab2": "日历ID",
        "modalPh2": "输入日历ID",
        "modalLab3": "用户邮箱:昵称",
        "modalPh3": "输入用户的邮箱:昵称",
        "modalLab4": "日历参与者数量",
        "modalPh4": "输入参与者数量",
        "modalLab5": "通知分发角色",
        "modalPh5": "输入角色",
        "noneOfThem1": "他们中没有人",
        "noneOfTheem2": "有空或忘记添加到日历",
        "success": "成功!",
        'oldBtn':"该按钮已过时",
        "titleAddUserModal": "输入要添加的用户",
        "modalLabAddUser": "用户昵称",
        "modalPhAddUser": "输入用户昵称",
        "notedUsers": "已标记的参与者",
        "intervalsTimeCould": "可以参加的时间段",
        "intervalsTimecouldnt": "不能参加的时间表",
        "allMay": "所有人都有空",
        "couldIn": "可以在",
        "timeing": "时间",
        "from": "从",
        "by": "通过",
        "to": "到",
        "and": " 和 ",
        "couldntIn": "不能在",
        "uploadTimeCouldnt": "无法参加的时间更新！",
        "uploadTimeCould": "时间更新",
        "noActualDataTime": "日期和时间不再有效",
        "nothigNoted": "没有人标记",
        "chooseCouldnt": "选择谁不能参加",
        "allCould": "所有人都可以",
        "deleted": "已删除!",
        "uploadSuccesful": "更新成功！"
    },"hi": {
        "month_declensions": {
            "january": "जनवरी",
            "february": "फरवरी",
            "march": "मार्च",
            "april": "अप्रैल",
            "may": "मई",
            "june": "जून",
            "july": "जुलाई",
            "august": "अगस्त",
            "september": "सितंबर",
            "october": "अक्टूबर",
            "november": "नवंबर",
            "december": "दिसंबर",
        },
        "weekday_declensions": {
            "monday": "सोमवार",
            "tuesday": "मंगलवार",
            "wednesday": "बुधवार",
            "thursday": "गुरुवार",
            "friday": "शुक्रवार",
            "saturday": "शनिवार",
            "sunday": "रविवार",
        },
        "labelbtn1": "मैं आऊंगा!",
        "labelbtn2": "दूसरे के लिए सूचित करें!",
        "labelbtn3": "नहीं आ सकता",
        "titleCalReg": "कैलेंडर पंजीकरण",
        "titleCalEdit": "कॉन्फ़िगरेशन संपादन",
        "modalLab1": "अपनी Google खाता कुंजी दर्ज करें",
        "modalPh1": "अपनी गूगल एपीआई कुंजी दर्ज करें",
        "modalLab2": "कैलेंडर आईडी",
        "modalPh2": "कैलेंडर आईडी दर्ज करें",
        "modalLab3": "ईमेल:आपके उपयोगकर्ताओं का उपनाम",
        "modalPh3": "अपने उपयोगकर्ताओं का ईमेल:उपनाम दर्ज करें",
        "modalLab4": "कैलेंडर प्रतिभागियों की संख्या",
        "modalPh4": "प्रतिभागियों की संख्या दर्ज करें",
        "modalLab5": "सूचनाओं के लिए भूमिका",
        "modalPh5": "भूमिका दर्ज करें",
        "noneOfThem1": "इनमें से कोई भी नहीं",
        "noneOfTheem2": "खाली समय है या कैलेंडर में जोड़ना भूल गए",
        "success": "सफलता!",
        'oldBtn':"बटन अप्रचलित है",
        "titleAddUserModal": "उपयोगकर्ता जोड़ें",
        "modalLabAddUser": "उपयोगकर्ता उपनाम",
        "modalPhAddUser": "उपयोगकर्ता उपनाम दर्ज करें",
        "notedUsers": "नोट किए गए प्रतिभागी",
        "intervalsTimeCould": "समय अंतराल जब वे आ सकते हैं",
        "intervalsTimecouldnt": "समय सारिणी जब लोग नहीं आ सकते",
        "allMay": "सभी खाली हैं",
        "couldIn": "आ सकता है",
        "timeing": "समय",
        "from": "से",
        "by": "तक",
        "to": "तक",
        "and": " और ",
        "couldntIn": "नहीं आ सकता",
        "uploadTimeCouldnt": "जब लोग नहीं आ सकते समय सारिणी अपडेट!",
        "uploadTimeCould": "समय सारिणी अपडेट",
        "noActualDataTime": "तिथि और समय अब प्रासंगिक नहीं हैं",
        "nothigNoted": "कोई नोट नहीं किया गया",
        "chooseCouldnt": "चुनें कौन नहीं आ सकता",
        "allCould": "सभी आ सकते हैं",
        "deleted": "हटा दिया गया!",
        "uploadSuccesful": "सफलतापूर्वक अपडेट किया गया!"
    }

}


class BtnView(discord.ui.View):
    def __init__(self,textChannel,index_,dateTime,language):
        super().__init__()
        # Создаем кнопку с переданным значением в custom_id
        self.custom_value = f"{textChannel}${index_}"
        self.dateTime = "@".join([singleDateTime.strftime('%Y-%m-%dT%H:%M:%S+03:00') for singleDateTime in dateTime])
        button = discord.ui.Button(label=languages[language]["labelbtn1"], style=discord.ButtonStyle.primary,custom_id=f"{self.custom_value}${self.dateTime}$User")
        button2 = discord.ui.Button(label=languages[language]["labelbtn2"], style=discord.ButtonStyle.primary,custom_id=f"{self.custom_value}${self.dateTime}$Admin")
        button3 = discord.ui.Button(label=languages[language]["labelbtn3"], style=discord.ButtonStyle.primary,custom_id=f"{self.custom_value}${self.dateTime}$Cancel")

        self.add_item(button)
        self.add_item(button2)
        self.add_item(button3)
        

class BtnViewCancel(discord.ui.View):
    def __init__(self,textChannel,index_,members):
        super().__init__()
        counter = {}
        for pos,member in enumerate(members):
            if not(member in list(counter.keys())):
                counter[member] = 0
            else:
                counter[member]+=1
            self.custom_value = f"{textChannel}${index_}~{member}^{counter[member]}"
            button = discord.ui.Button(label=f"{pos+1}.{member}", style=discord.ButtonStyle.primary,custom_id=f"{self.custom_value}${"None"}$DelUser")
            self.add_item(button)

            
                    


        
        
        

class MyModal(discord.ui.Modal):
    def __init__(self,required,language):
        if required :
            title = languages[language]["titleCalReg"]
        else:
            title = languages[language]["titleCalEdit"]
        super().__init__(title = title)
        self.required = required
        self.api_key = discord.ui.TextInput(
            label=languages[language]["modalLab1"],
            placeholder=languages[language]["modalPh1"],
            required=required,
        )
   

        self.calendar_id = discord.ui.TextInput(
            label=languages[language]["modalPh2"],
            placeholder=languages[language]["modalPh2"],
            required=required,
        )
      
    
        self.names = discord.ui.TextInput(
            label=languages[language]["modalPh3"],
            placeholder=languages[language]["modalPh3"],
            required=False,
        )
        self.amount = discord.ui.TextInput(
            label=languages[language]["modalPh4"],
            placeholder=languages[language]["modalPh4"],
            required=False,
        )

        self.roleField = discord.ui.TextInput(
            label=languages[language]["modalPh5"],
            placeholder=languages[language]["modalPh5"],
            required=False,
        )
        self.add_item(self.api_key)
        self.add_item(self.calendar_id)
        self.add_item(self.names)
        self.add_item(self.amount)
        self.add_item(self.roleField)


    async def on_submit(self, interaction: discord.Interaction):
        calendar_changed = False
        # Process the input here
        try:
            await interaction.response.defer()
        except:
            pass
        Base.metadata.create_all(engine)
        session = Session()

        if not self.required:
            if interaction.guild_id:
                guild = bot.get_guild(int(interaction.guild.id))
            channel = bot.get_channel(interaction.channel.id)

            existing_record = session.query(TextChannels).filter_by(id=channel.id).first()
            language = existing_record.relation.language       
            if (not self.api_key.value) or (self.api_key.value == existing_record.relation.GOOGLE_API_KEY):
                api_key = existing_record.relation.GOOGLE_API_KEY
            else:
                api_key = self.api_key.value 

            if (not self.calendar_id.value) or (self.calendar_id.value == existing_record.relation.GOOGLE_CALENDAR_ID):
                calendar_id = existing_record.relation.GOOGLE_CALENDAR_ID
            else:
                calendar_changed =True
                calendar_id = self.calendar_id.value

            if (not self.names.value) or (self.names.value == existing_record.relation.NAMES):
                names = existing_record.relation.NAMES
            else:
                try:
                    [[i for i in name.split(":")] for name in self.names.value.split(",")][0][0]
                    names = self.names.value
                except:
                    names = existing_record.relation.NAMES


            if (not self.amount.value) or (self.amount.value == existing_record.relation.lenUsers):
                amount = existing_record.relation.lenUsers
            else:
                try:
                    int(self.amount.value)
                    amount = self.amount.value 
                except:
                    amount = existing_record.relation.lenUsers

            if (not self.roleField.value) or (self.roleField.value == existing_record.relation.role):
                role_name = existing_record.relation.role
            else:
                role_name = self.roleField.value


        else:
            # тут мы берем каждое значение в таблицы и проверяем если пусто или равно
            # то мы оставляем,а если нет то меняем на новый
            #проверить так же language ,если нет,то "eng"
            language = "eng"
            api_key = self.api_key.value  
            calendar_id = self.calendar_id.value
            names = self.names.value
            amount = self.amount.value
            role_name = self.roleField.value 
            USER = interaction.user.id
        
        



        # Поиск текстового канала по названию
        
        if interaction.guild_id:
            guild = bot.get_guild(int(interaction.guild.id))

            if not role_name:
                role_name = "Schedule"
            role = discord.utils.get(guild.roles, name=role_name)

            channel = bot.get_channel(interaction.channel.id)
            
            events = get_calendar_events(api_key, calendar_id)
            howmuch = len(constructEmailDateTimesDict(events)[0])
            returnedData = returnDataTime(channel, howmuch, events,cashed=True)
            constructedData = constructEmailDateTimesDict(events)[1]
            
            existing_record = session.query(TextChannels).filter_by(id=channel.id).first()
            if not calendar_changed and existing_record:
                cashData = existing_record.relation.cache   # если рекваед и валью calendar id равны , иначе берем старый(как?берем из базы данных)

            else:
                cashData={
                "new_events":events,
                "old_events":events,
                "new_formatedData":returnedData,
                "old_formatedData":returnedData,
                "new_reversed_formatedData":constructedData,
                "old_reversed_formatedData":constructedData,
                }
                cashData = json.dumps(cashData,cls=DateTimeEncoder)
                 # берем кэш из базы данных и присваиваем cashData и не дампсием
                
            

            
            if existing_record:
                # Обновление существующей записи
                session.delete(existing_record)

            textChannels0 = TextChannels(id=str(channel.id))
            if not role:
                role = role_name
            else:
                role = role.id
            dataForTextChannels = DataFor_TextChannels(guild.id,role,channel.id,api_key,calendar_id,names,cashData,amount,language)
            textChannels0.relation = dataForTextChannels
            session.add(textChannels0)

        else:  
            existing_record = session.query(Names).filter_by(id=USER).first()
            if existing_record:
                
                session.delete(existing_record)

            user0 = Names(id=str(USER))
            dataForNames = DataFor_Names(api_key,calendar_id,names,language)
            user0.relation = dataForNames
            session.add(user0)
        
        
        
        session.commit()
        session.close()
            
           


        # Send a confirmation message
        
        await interaction.followup.send(languages[language]["success"]) 

class AddUserModal(discord.ui.Modal):
    def __init__(self,cache,index_,textChannel,session,language):
        super().__init__(title=languages[language]["titleAddUserModal"])
        self.cache = cache
        self.index_ = index_
        self.session = session
        self.textChannel = textChannel
        self.language = language
        # Добавляем текстовое поле
        self.input_field = discord.ui.TextInput(label=languages[language]["modalLabAddUser"], placeholder=languages[language]["modalPhAddUser"],required=True)
        self.add_item(self.input_field)
        
    # Этот метод вызывается при отправке модального окна
    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
        except:
            pass
        language =self.language 
        #await interaction.response.send_message(content="Пользователь добавлен!",ephemeral=True)
        # Получаем текст, введенный пользователем
        user_input = self.input_field.value
        if user_input in self.cache["old_formatedData"][list(self.cache["old_formatedData"].keys())[0]][self.index_][1]:
            message= discord.Embed(title=f'***{languages[language]["notedUsers"]}***',color=0x00FF7F)
            members = self.cache["old_formatedData"][list(self.cache["old_formatedData"].keys())[0]][self.index_][1]
            cancelView = BtnViewCancel(self.textChannel,self.index_,members)
            await interaction.followup.send(embed=message,view=cancelView,ephemeral=True) 
            return None
        self.cache["old_formatedData"][list(self.cache["old_formatedData"].keys())[0]][self.index_][1].append(user_input)
        cache1 = json.dumps(self.cache,cls=DateTimeEncoder)
        rowForUploadCache = self.session.query(DataFor_TextChannels).filter_by(relationID=self.textChannel).first()#Обновить кэш 
        rowForUploadCache.cache = cache1 
        self.session.commit()
        self.session.close()
        message= discord.Embed(title=f'***{languages[language]["notedUsers"]}***',color=0x00FF7F)
        members = self.cache["old_formatedData"][list(self.cache["old_formatedData"].keys())[0]][self.index_][1]
        cancelView = BtnViewCancel(self.textChannel,self.index_,members)
        await interaction.followup.send(embed=message,view=cancelView,ephemeral=True) 

async def send_with_timeout(interaction: discord.Interaction, message, timeout: int = 5,private=False,view=False):
    try:
        if type(message) ==str:
            if private:
                await asyncio.wait_for(interaction.followup.send(message,ephemeral=True), timeout)
            else:
                await asyncio.wait_for(interaction.followup.send(message), timeout)
        else:
            if private:
                if view:
                    await asyncio.wait_for(interaction.followup.send(embed=message,ephemeral=True,view=view), timeout)
                else:
                    await asyncio.wait_for(interaction.followup.send(embed=message), timeout)
            else:
                if view:
                    await asyncio.wait_for(interaction.followup.send(embed=message,view=view), timeout)
                else:
                    await asyncio.wait_for(interaction.followup.send(embed=message), timeout)
    except asyncio.TimeoutError:
        print("Sending message timed out")

def convertDBtodict(ctx,toMember=False):

    Base.metadata.create_all(engine)

    session = Session()



    if type(ctx) == discord.channel.TextChannel:
        existing_record = session.query(TextChannels).filter_by(id=str(ctx.id)).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_TextChannels).filter_by(relationID=existing_record).first()
        
     
    elif toMember:
        existing_record = session.query(TextChannels).filter_by(id=str(toMember)).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_TextChannels).filter_by(relationID=existing_record).first()
        
    elif getattr(ctx,"guild",False):
        existing_record = session.query(TextChannels).filter_by(id=str(ctx.channel.id)).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_TextChannels).filter_by(relationID=existing_record).first()
    
    elif type(ctx) == str:
        existing_record = session.query(TextChannels).filter_by(id=ctx).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_TextChannels).filter_by(relationID=existing_record).first()

    elif type(ctx) == discord.interactions.Interaction:
        existing_record = session.query(Names).filter_by(id=str(ctx.user.id)).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_Names).filter_by(relationID=existing_record).first()  
    
    else:
        existing_record = session.query(Names).filter_by(id=str(ctx.author.id)).first()
        existing_record = existing_record.id
        existing_record = session.query(DataFor_Names).filter_by(relationID=existing_record).first()  
    
    session.close()
    
    return {"guild":getattr(existing_record,"guild",""),"role":getattr(existing_record,"role",""),"channel":getattr(existing_record,"channel",""),"GOOGLE_API_KEY":existing_record.GOOGLE_API_KEY,"GOOGLE_CALENDAR_ID":existing_record.GOOGLE_CALENDAR_ID,"NAMES":existing_record.NAMES,"cache":getattr(existing_record,"cache",""),"lenUsers":getattr(existing_record,"lenUsers",""),"language":getattr(existing_record,"language","")}

        

    
def exeptBusyTime(ctx,dataTime,events):
    
    if not dataTime[list(dataTime.keys())[0]]:
        return dataTime
    dataTimeNew =collections.defaultdict(list)

    DataTimeExept=constructEmailDateTimesDict(events)[1]
    for users in DataTimeExept:
        for time in DataTimeExept[users]:
            time = time['dateTime']
            
            for users1 in dataTime:
                count = 0
                for time1 in dataTime[users1]:
                    count+=1

                    if time[0]<=time1[0] and time[1] >= time1[1]:
                        continue

                    if time[0]<=time1[0] and time[1]>=time1[0]:

                        dataTimeNew[users1].append([time[1],time1[1]]) #добавить промежуток времени
                        continue
                    
                    if time[0]<=time1[1] and time1[1]<=time[1]:
                        dataTimeNew[users1].append([time1[0],time[0]])
                        continue
                    

                    
                    if time[0]>=time1[0] and time[1]<=time1[1]:
                        dataTimeNew[users1].append([time1[0],time[0]])
                        dataTimeNew[users1].append([time[1],time1[1]])
                        continue

                    dataTimeNew[users1].append([time1[0],time1[1]])
            if not dataTimeNew:
                dataTimeNew[list(dataTime.keys())[0]] = []
                dataTime = dataTimeNew
                return dataTime
            dataTime = copy.deepcopy(dataTimeNew)
            dataTimeNew =collections.defaultdict(list)
            

    return dataTime



                    
            
                   
def remove_value_by_index(lst, value, target_index):
    # Найти все индексы элемента с заданным значением
    indices = [index for index, val in enumerate(lst) if val == value]

    if not indices:
        print(f"Элементы со значением {value} не найдены в списке.")
        return

    # Проверка, существует ли элемент с таким индексом
    if target_index < len(indices):
        # Если индекс существует, удаляем элемент по этому индексу
        index_to_remove = indices[target_index]
        lst.pop(index_to_remove)
    else:
        # Если индекс больше допустимого, удаляем крайний справа
        if target_index >= len(indices):
            lst.pop(indices[-1])
        # Если индекс меньше допустимого, удаляем крайний слева
        elif target_index < 0:
            lst.pop(indices[0])
        else:
            print(f"Невозможно выполнить удаление, так как указанный индекс {target_index} некорректен.")
               

def get_declension(date,language):
    weekday = date.strftime("%A")
    day = date.strftime("%d")
    month = date.strftime("%B")
    year = date.strftime("%Y")
    time = date.strftime("%H:%M")

    weekday_decl = languages[language]["weekday_declensions"].get(weekday.lower(), weekday)
    month_decl = languages[language]["month_declensions"].get(month.lower(), month)
    return [weekday_decl, month_decl]


def get_person_declension(number,lang='eng'):
    if lang == "rus":
        if 11 <= number % 100 <= 14:
            return f"{number} человек"
        if number % 10 == 1:
            return f"{number} человек"
        if 2 <= number % 10 <= 4:
            return f"{number} человека"
        return f"{number} человек"
    
    elif lang == "en":
        return f"{number} person{'s' if number != 1 else ''}"
    
    elif lang == "es":
        return f"{number} persona{'s' if number != 1 else ''}"
    
    elif lang == "zh":
        return f"{number} 人"  # В китайском языке форма не изменяется
    
    elif lang == "hi":
        return f"{number} व्यक्ति"  # В хинди форма не изменяется
    
    # Добавить другие языки по мере необходимости
    else:
        # По умолчанию, если язык не поддерживается, возвращаем без изменений
        return f"{number} человек"


# Функция для поиска пересечения временных интервалов
def get_overlap(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2

    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)

    if latest_start < earliest_end:
        return (latest_start, earliest_end)
    else:
        return None


# Функция для поиска пересечений для заданного количества людей
def find_overlaps(schedule, num_people):
    overlaps = {}
    keys = list(schedule.keys())

    for combo in itertools.combinations(keys, num_people):
        combo_name = "@".join(combo)
        overlaps[combo_name] = []

        # Пары всех возможных временных интервалов
        intervals = [schedule[person] for person in combo]
        for interval_set in itertools.product(*intervals):
            common_overlap = interval_set[0]
            for interval in interval_set[1:]:
                common_overlap = get_overlap(common_overlap, interval)
                if not common_overlap:
                    break
            if common_overlap:
                overlaps[combo_name].append(common_overlap)

    return overlaps


def get_calendar_events(api_key, calendar_id):
    """Получить события из Google Calendar."""
    service = build("calendar", "v3", developerKey=api_key)
    now = datetime.datetime.utcnow().isoformat() + "Z"
    #future = (datetime.datetime.utcnow() + datetime.timedelta(days=16)).isoformat() + 'Z'
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return events


def find_first_hash_word(text, symbol):
    words = text.split()
    for word in words:
        if word.startswith(symbol):
            return word
    return False


def constructEmailDateTimesDict(events):
    eventData = [eventDataFreeTime,eventDataBusyTime] = {},{}
    index = 0
    for event in events:
        if "summary" in event.keys():
            busy = find_first_hash_word(event["summary"], "$")
            selected_user = find_first_hash_word(event["summary"], "#")
            
            if busy:
                index = 1
            else:
                index = 0

            if selected_user:
                user = selected_user[1:]

            else:
                user = event["creator"]["email"].split("@")[0]
        else:
            user = event["creator"]["email"].split("@")[0]

        if not user in eventData[index]:
            eventData[index][user] = []
        
        if "dateTime" not in event['start'].keys():
            start = datetime.datetime.strptime(event['start']['date'],"%Y-%m-%d")
            end = datetime.datetime.strptime(event['end']['date'],"%Y-%m-%d")
            timezone_offset = datetime.timezone(datetime.timedelta(hours=3))
            end = end.replace(hour=0, tzinfo=timezone_offset)
            start = start.replace(hour=0, tzinfo=timezone_offset)
        else:
            start = datetime.datetime.fromisoformat(event['start']['dateTime'])
            end = datetime.datetime.fromisoformat(event['end']['dateTime'])
        
        if index ==0:
            
            eventData[index][user].append((start, end))
        else: 
            eventData[index][user].append({"dateTime":(start, end),"summary":event["summary"].replace("$","").replace("#","")})
    
    return eventData


def renaming(name,data):
    if not data['NAMES']:
        return name
    NAMES_NOT_STRUCT = data['NAMES']
    NAMES = dict([[i for i in name.split(":")] for name in NAMES_NOT_STRUCT.split(",")])
    
    if name in NAMES.keys():
        return NAMES[name]
    else:
        return name


def returnDataTime(ctx, howmuch, events,ex=True,cashed=False):

    user_Date_TimesData = constructEmailDateTimesDict(events)[0]

    if not howmuch:
        howmuch = len(user_Date_TimesData)

    if howmuch != 1:
        howmuch = int(howmuch)
        user_Date_TimesData = find_overlaps(user_Date_TimesData, howmuch)
    if ex:
        
        user_Date_TimesData=exeptBusyTime(ctx,user_Date_TimesData,events=events)

    if cashed:
        #if user_Date_TimesData:
        for ind,times in enumerate(user_Date_TimesData[list(user_Date_TimesData.keys())[0]]):
            user_Date_TimesData[list(user_Date_TimesData.keys())[0]][ind]= [times,[]]
        
    return user_Date_TimesData


async def printDataTime(ctx, howmuch,data,ex =True,withButton=False,language="eng"):
    howmuch0 = howmuch
    if type(ctx) == discord.Interaction:
        await ctx.response.defer()
        pass
    events = get_calendar_events( data['GOOGLE_API_KEY'],data['GOOGLE_CALENDAR_ID'])

    user_Date_TimesData = returnDataTime(ctx, howmuch, events,ex=ex)

    if not howmuch:
        howmuch = len(constructEmailDateTimesDict(events)[0])

    checking = list(user_Date_TimesData.values())
    if checking ==[[]]:
        checking = []
    if checking:
        if user_Date_TimesData[list(user_Date_TimesData.keys())[0]]:
            howmuch = int(howmuch)
        if type(ctx) == discord.Interaction:
            
            await send_with_timeout(ctx,
            message=discord.Embed(
                title=f"{languages[language]['intervalsTimeCould']} {get_person_declension(howmuch,language)}",
                color=0x0000FF,
            )
        )
        else:
            await ctx.send(
            embed=discord.Embed(
                title=f"{languages[language]['intervalsTimeCould']} {get_person_declension(howmuch,language)}",
                color=0x0000FF,
            )
        )
        await formatingData(ctx, user_Date_TimesData,data=data,withButton=withButton,howMuch=howmuch0,language=language)
    else:
        howmuch = int(howmuch)
        if type(ctx) == discord.Interaction:
            
            await send_with_timeout(ctx,
            message=discord.Embed(
                title=f"{languages[language]['noneOfThem1']} {get_person_declension(howmuch,language)} {languages[language]['noneOfTheem2']}",
                color=0xFF0000,
            )
        )
        else:
            
            await ctx.send(
            embed=discord.Embed(
                title=f"{languages[language]['noneOfThem1']} {get_person_declension(howmuch,language)} {languages[language]['noneOfTheem2']}",
                color=0xFF0000,
            )
        )



async def printDataTimeReversed(ctx,howmuch,data,language):
    if type(ctx) == discord.Interaction:
        await ctx.response.defer()
        pass

    events = get_calendar_events( data['GOOGLE_API_KEY'],data['GOOGLE_CALENDAR_ID'])
      
    user_Date_TimesData = constructEmailDateTimesDict(events)[1]

    if not howmuch:
        howmuch = len(constructEmailDateTimesDict(events)[0])
    if user_Date_TimesData:

        howmuch = int(howmuch)
        if type(ctx) == discord.Interaction:
            
            await send_with_timeout(ctx,message=discord.Embed(title=languages[language]['intervalsTimecouldnt'],color=0xDC143C,))
        else:
            await ctx.send(embed=discord.Embed(title=languages[language]['intervalsTimecouldnt'],color=0xDC143C,))
        await formatingDataReversed(ctx,user_Date_TimesData,data=data,language=language)

    else:
        if type(ctx) == discord.Interaction:
            
            await send_with_timeout(ctx,
        	message=discord.Embed(
            	title=languages[language]['allMay'],
            	color=0x6A5ACD,
        	)
        )
        else:
            await ctx.send(
        	embed=discord.Embed(
            	title=languages[language]['allMay'],
            	color=0x6A5ACD,
        	)
        )


        


async def formatingData(ctx, user_Date_TimesData,data,withButton=False,howMuch=False,language="eng"):
    


    for users in user_Date_TimesData:
        
        if user_Date_TimesData[users]:
            users0 = users.split('@')
            users0 = [renaming(user,data) for user in users0]
            users_len = len(users0)
            users0 = languages[language]['and'].join(users0)
            embed = discord.Embed(
                title=f"{str(users0)} {languages[language]['couldIn']}",
                color=0x4169E1,
            )
            if type(ctx) == discord.Interaction:
                
                await send_with_timeout(ctx,message=embed)
            else:
                await ctx.send(embed=embed)

            for index_,dateTimes in enumerate(user_Date_TimesData[users]):
                weeekandmonth0 = get_declension(dateTimes[0],language)
                weeekandmonth1 = get_declension(dateTimes[1],language)
                message =discord.Embed(title=languages[language]['timeing'],description=f"{languages[language]['from']} {dateTimes[0].strftime('%d')} {weeekandmonth0[1]} {weeekandmonth0[0]} {languages[language]['by']} {dateTimes[1].strftime('%d')} {weeekandmonth1[1]} {weeekandmonth1[0]}  \n {languages[language]['from']} { dateTimes[0].strftime('%H:%M')} {languages[language]['to']} { dateTimes[1].strftime('%H:%M')}",color=0x00BFFF)
                messageWithBold = discord.Embed(title=languages[language]['timeing'],description=f"****__{languages[language]['from']} {dateTimes[0].strftime('%d')} {weeekandmonth0[1]} {weeekandmonth0[0]} {languages[language]['by']} {dateTimes[1].strftime('%d')} {weeekandmonth1[1]} {weeekandmonth1[0]}  \n {languages[language]['from']} { dateTimes[0].strftime('%H:%M')} {languages[language]['to']} { dateTimes[1].strftime('%H:%M')}__****",color=0x00BFFF)
                if (dateTimes[1] - dateTimes[0]) >= datetime.timedelta(
                    hours=2, minutes=30
                ):

                    if type(ctx) == discord.Interaction:
                        if withButton or (not(howMuch) and ctx.guild):
                            if type(ctx) == discord.Interaction or type(ctx)== discord.channel.TextChannel:
                                await send_with_timeout(ctx,message=message,view=BtnView(ctx.id,index_,dateTimes,language))
                            else:
                                await send_with_timeout(ctx,message=message,view=BtnView(ctx.channel.id,index_,dateTimes,language))
                        else:
                            await send_with_timeout(ctx,message=message
                    )
                            await send_with_timeout(ctx,message=messageWithBold)
                    
                    else:
                        if withButton or (not(howMuch) and ctx.guild):
                            if type(ctx) == discord.Interaction or type(ctx)== discord.channel.TextChannel:

                                await ctx.send(embed=messageWithBold,view=BtnView(ctx.id,index_,dateTimes,language))
                           
                            else:
                                await ctx.send(embed=messageWithBold,view=BtnView(ctx.channel.id,index_,dateTimes,language))



                        else:
                            await ctx.send(embed=messageWithBold)
                else:
                    if type(ctx) == discord.Interaction:
                        
                        await send_with_timeout(ctx,message=message)
                    else:
                        if withButton or (not(howMuch) and ctx.guild):
                            if type(ctx) == discord.Interaction or type(ctx)== discord.channel.TextChannel:

                                await ctx.send(embed=message,view=BtnView(ctx.id,index_,dateTimes,language))

                            else:
                                await ctx.send(embed=message,view=BtnView(ctx.channel.id,index_,dateTimes,language))

                        else:
                            await ctx.send(embed=message)

async def formatingDataReversed(ctx, user_Date_TimesData,data,language):
    

    for users in user_Date_TimesData:
        

        if user_Date_TimesData[users]:
            users0 = users.split('@')
            users0 = [renaming(user,data) for user in users0]
            users0 = languages[language]["and"].join(users0)
            embed = discord.Embed(title=f"{users0} {languages[language]['couldntIn']}:",color=0xFF4500,)

			

            for dateTimes in user_Date_TimesData[users]:

                weeekandmonth0 = get_declension(dateTimes["dateTime"][0],language)
                weeekandmonth1 = get_declension(dateTimes["dateTime"][1],language)

                
                embed.add_field(
                    name=languages[language]["timeing"],
                    value=f"{languages[language]['from']} {dateTimes["dateTime"][0].strftime('%d')} {weeekandmonth0[1]} {weeekandmonth0[0]} {languages[language]['by']} {dateTimes["dateTime"][1].strftime('%d')} {weeekandmonth1[1]} {weeekandmonth1[0]}  \n {languages[language]['from']} { dateTimes["dateTime"][0].strftime('%H:%M')} {languages[language]['to']} { dateTimes["dateTime"][1].strftime('%H:%M')} \n {dateTimes['summary']}\n",
                    inline=False,
                )

            if type(ctx) == discord.Interaction:
                
                await send_with_timeout(ctx,message=embed)
            else:
                await ctx.send(embed=embed)

# Настройка Discord бота









@tasks.loop(minutes= 50)
async def ping_loop0():
    try:
        Base.metadata.create_all(engine)
        session = Session()
        txtChannels1 = session.query(TextChannels.id).all()

        for txtChannel in  txtChannels1:
            try:
                

                txtChannel = txtChannel[0]
                data=convertDBtodict(txtChannel) 
                a = data["cache"]
                cache = json.loads(data["cache"], cls=DecodeDateTime)
                events = get_calendar_events( data['GOOGLE_API_KEY'], data['GOOGLE_CALENDAR_ID'])
                guild = bot.get_guild(int(data['guild']))
                CHANNEL_ID =txtChannel
                #events = get_calendar_events( data['GOOGLE_API_KEY'], data['GOOGLE_CALENDAR_ID'])
                howmuch = len(
                    constructEmailDateTimesDict(events)[0]
            )
                channel = bot.get_channel(int(CHANNEL_ID))
                cache["new_events"] = constructEmailDateTimesDict(events)[0]
                cache["new_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
                cache["new_formatedData"] = returnDataTime(channel, howmuch, events,cashed=True)
                cache = json.dumps(cache,cls=DateTimeEncoder)
                rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=txtChannel).first()#Обновить кэш 
                rowForUploadCache.cache = cache
                session.commit()
                session.close()
                Base.metadata.create_all(engine)
                session = Session()
                txtChannels1 = session.query(TextChannels.id).all()  
                txtChannel = txtChannels1[0][0]
                data=convertDBtodict(txtChannel) 
                language = data['language']
                a = data["cache"]
                cache = json.loads(data["cache"], cls=DecodeDateTime)


                if cache["old_reversed_formatedData"] != cache["new_reversed_formatedData"]:
                    cache["old_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
                    if channel:
                        await channel.send("⠀⠀⠀⠀")
                        await channel.send(
                        embed=discord.Embed(
                            	title=f"{languages[language]['uploadTimeCouldnt']}!", color=0xFF00FF
                        	)
                    	)

                        await printDataTimeReversed(channel,howmuch,data=data,language=data['language'])

                if cache["old_events"] != cache["new_events"]:
                    
                    cache["old_events"] = constructEmailDateTimesDict(events)[0]
                    

                    try:
                        a = [zxc[0] for zxc in [*cache["new_formatedData"][list(cache["new_formatedData"].keys())[0]]]]

                    except:
                        a = []
                    try:
                        b =[zxc[0] for zxc in [*cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]]]
                    except:
                        b = []
                    if a == []:
                        a.append([])
                    if b ==[]:
                        b.append([])

                
                    if (a != b):
                        dataTimeForCache = returnDataTime(channel, howmuch, events,cashed=True)
                        users_len = len(list(cache["old_formatedData"].keys())[0].split('@'))
                        isContains = False
                        if howmuch!= users_len:
                            cache["old_formatedData"] = dataTimeForCache
                            users_len = len(list(cache["old_formatedData"].keys())[0].split('@'))
                        else:
                            new_dataTime = {}
                            new_dataTime[list(dataTimeForCache.keys())[0]] = []
                            for dataTime in dataTimeForCache[list(dataTimeForCache.keys())[0]]:
                                for cache_timeData in cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]:
                                    oldCacheTimeData = [[datetime.datetime.fromisoformat(dateTime_str) for dateTime_str in cache_timeData[0]],cache_timeData[1]]

                                    if list(dataTime[0]) == list(oldCacheTimeData[0]) :
                                        new_dataTime[list(dataTimeForCache.keys())[0]].append(oldCacheTimeData)
                                        isContains = True
                                        break
                                if not isContains:
                                    new_dataTime[list(dataTimeForCache.keys())[0]].append(dataTime)
                                isContains = False
                            cache["old_formatedData"] = new_dataTime

                            

                        if guild:
                            if channel:
                                print(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]])
                                # тут идет еще одна проверка,а именно,на то что равно ли кол-во людей кол-во в базе,если только оно не False,если False,то печатать
                                if (users_len == int(data['lenUsers'])) or not cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]:
                                    await channel.send("⠀⠀⠀⠀")
                                    await channel.send(
                                	    embed=discord.Embed(
                                    	title=f"{languages[language]['uploadTimeCould']}!", color=0xFF00FF
                                	    )
                            	    )
                                    await printDataTime(channel, howmuch,data=data,withButton=True,language=data['language'])
                


                cache["new_events"] = constructEmailDateTimesDict(events)[0]
                cache["new_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
                cache["new_formatedData"] = returnDataTime(channel, howmuch, events,cashed=True)
                cache = json.dumps(cache,cls=DateTimeEncoder)
                rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=txtChannel).first()#Обновить кэш 
                rowForUploadCache.cache = cache
                session.commit()
                session.close()
            except:
                continue
        print("Ping!")
    
    except Exception as e:
        print(e)


@bot.event
async def on_ready():
    #Обращение к базе данных
    print(f"Logged in as {bot.user}")
    ping_loop0.start()
    


@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        try:
            textChannel,index_,convertedDateTime,status = interaction.data["custom_id"].split("$")
        except:
            return None
        if "~" in index_:
            index_,memb = index_.split("~") 
            memb,position = memb.split("^")
            position = int(position)
        index_ = int(index_)
        user = interaction.user.display_name
    except:
        return None
    try:
        if not(status == "Admin"):
            await interaction.response.defer()
    except:
        pass

        
    Base.metadata.create_all(engine)
    session = Session()
        
        
    data=convertDBtodict(textChannel) 
    language = data['language']
    a = data["cache"]
    cache = json.loads(data["cache"], cls=DecodeDateTime)
    if not cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]:
            message= discord.Embed(title=f"***{languages[language]['noActualDataTime']}***",color=0xB22222)
            session.commit()
            session.close()
            await interaction.followup.send(embed=message,ephemeral=True)
            return None

    for k,v in enumerate(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]):
        convertedDateTime01 = "@".join([singleDateTime for singleDateTime in v[0]])
        if convertedDateTime01 == convertedDateTime:
            index_ = k
            break
        else:
            index_=False

    howmuch = len(list(cache["old_formatedData"].keys())[0].split('@'))
    if (index_!= 0 and (not index_)):
        convertedDateTime0 = False
    else:
        convertedDateTime0 = "@".join([str(single_dataTime) for single_dataTime in cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][0]])



    if status == "DelUser":
        
        remove_value_by_index(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1],memb,position)
        
        cache1 = json.dumps(cache,cls=DateTimeEncoder)
        rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=textChannel).first()#Обновить кэш 
        rowForUploadCache.cache = cache1
        session.commit()
        session.close()
        if not cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]:
            message= discord.Embed(title=f"***{languages[language]['nothigNoted']}***",color=0xB22222)
            await interaction.followup.send(embed=message,ephemeral=True)
            return None
        message= discord.Embed(title=f"***{languages[language]["notedUsers"]}***",color=0x00FF7F)
        membe = cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]
        cancelView = BtnViewCancel(textChannel,index_,membe)
        await interaction.followup.send(embed=message,view=cancelView,ephemeral=True)
        
        return None

    if not ( convertedDateTime0==convertedDateTime):
        message= discord.Embed(title=f"***{languages[language]['noActualDataTime']}***",color=0xB22222)
        session.commit()
        session.close()
        await interaction.followup.send(embed=message,ephemeral=True)
        return None
    
    if status == "Cancel":
        if not cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]:
            message= discord.Embed(title=f"***{languages[language]['nothigNoted']}***",color=0xB22222)
            session.commit()
            session.close()
            await interaction.followup.send(embed=message,ephemeral=True)
            return None
        message= discord.Embed(title=f"***{languages[language]['chooseCouldnt']}***",color=0x00FF7F)
        members = cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]
        cancelView = BtnViewCancel(textChannel,index_,members)
        session.commit()
        session.close()
        await interaction.followup.send(embed=message,view=cancelView,ephemeral=True)
        
        return None
    
    if howmuch == len(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]):
        message= discord.Embed(title=f"***{languages[language]['notedUsers']}***",color=0x00FF7F)
        members = cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]
        session.commit()
        session.close()
        cancelView = BtnViewCancel(textChannel,index_,members)
        await interaction.followup.send(embed=message,view=cancelView,ephemeral=True)  
        return None

    if status == "Admin":
        
        modal = AddUserModal(cache,index_,textChannel,session,language)
        session.commit()
        session.close()
        await interaction.response.send_modal(modal)
        return None
    elif not (user in cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]):
        cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1].append(user)

        
            
        
    if howmuch == len(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]):
        guild = bot.get_guild(int(data['guild']))
        role = guild.get_role(int(data['role']))
            
        if role:
            for member in role.members:
                try:
                    await member.send("⠀⠀⠀⠀")
                    await member.send(
                    embed=discord.Embed(
                        title=f"{languages[language]['allCould']}!",
                        color=0xFF00FF,
                    )
                )
                    dateTimes = cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][0]
                    dateTimes = [datetime.datetime.fromisoformat(dateTime_str) for dateTime_str in dateTimes]
                    weeekandmonth0 = get_declension(dateTimes[0],language)
                    weeekandmonth1 = get_declension(dateTimes[1],language)
                    if (dateTimes[1] - dateTimes[0]) >= datetime.timedelta(
                        hours=2, minutes=30
                    ):
                        await member.send(embed=discord.Embed(title=languages[language]['timeing'],description=f"****__{languages[language]['from']} {dateTimes[0].strftime('%d')} {weeekandmonth0[1]} {weeekandmonth0[0]} {languages[language]['by']} {dateTimes[1].strftime('%d')} {weeekandmonth1[1]} {weeekandmonth1[0]}  \n {languages[language]['from']} { dateTimes[0].strftime('%H:%M')} {languages[language]['to']} { dateTimes[1].strftime('%H:%M')}__****",color=0x00BFFF))
		                
                    else:
                        await member.send(embed=discord.Embed(title=languages[language]['timeing'],description=f"{languages[language]['from']} {dateTimes[0].strftime('%d')} {weeekandmonth0[1]} {weeekandmonth0[0]} {languages[language]['by']} {dateTimes[1].strftime('%d')} {weeekandmonth1[1]} {weeekandmonth1[0]}  \n {languages[language]['from']} { dateTimes[0].strftime('%H:%M')} {languages[language]['to']} { dateTimes[1].strftime('%H:%M')}",color=0x00BFFF
                ))

                except:
                    pass 
            
    cache1 = json.dumps(cache,cls=DateTimeEncoder)
    rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=textChannel).first()#Обновить кэш 
    rowForUploadCache.cache = cache1
    session.commit()
    session.close()
    #message= discord.Embed(title="***БУДУТ:***",description="\n".join("**{}. {}**".format(n, i) for n, i in enumerate(cache["old_formatedData"][list(cache["old_formatedData"])[0]][index_][1], start=1)),color=0x00FF7F)
    message= discord.Embed(title=f"***{languages[language]["notedUsers"]}***",color=0x00FF7F)
    members = cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]][index_][1]
    cancelView = BtnViewCancel(textChannel,index_,members)
    await interaction.followup.send(embed=message,view=cancelView,ephemeral=True)   

@bot.tree.command(name="free")
async def free(ctx, *,howmuch:Optional[str] = None,ex:Optional[bool] = True):
    """Free dates"""
    data=convertDBtodict(ctx)
 


    await printDataTime(ctx, howmuch,ex=ex,data=data,language=data['language'])

@bot.command()
async def free(ctx, *,howmuch:Optional[str] = None,ex:Optional[bool] = True):
    """Free dates"""
    data=convertDBtodict(ctx)
 


    await printDataTime(ctx, howmuch,ex=ex,data=data,language=data['language'])


@bot.tree.command(name="busy")
async def busy(ctx:commands.Context):
    """Busy dates"""
    howmuch = None
    data=convertDBtodict(ctx)

    await printDataTimeReversed(ctx, howmuch,data=data,language=data['language'])

@bot.command()
async def busy(ctx:commands.Context, *, howmuch:Optional[str] = None):
    """Busy dates"""

    data=convertDBtodict(ctx)

    await printDataTimeReversed(ctx, howmuch,data=data,language=data['language'])

@bot.tree.command(name="delete_calendar")
async def delete_calendar(interaction:discord.Interaction):
    """Delete calendar"""
    await interaction.response.send_message(content="Удалено!",ephemeral=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    if interaction.guild_id:
        user_id = str(interaction.channel.id)
        user = session.query(TextChannels).filter_by(id=user_id).first()
    else:
        user_id = str(interaction.channel.id)
        user = session.query(Names).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
    


@bot.tree.command(name="conf")
async def conf(interaction:discord.Interaction):
    """Configurate"""
    Base.metadata.create_all(engine)
    session = Session()
    existing_record = session.query(TextChannels).filter_by(id=str(interaction.channel.id)).first()
    #Тут мы должны связаться с базой данных и посмотреть числиться ли с данный канал id в базе ,если числиться то мы меняем,то есть с requried False иначе True
    if existing_record:
        language = existing_record.relation.language
        view = MyModal(False,language)
        await interaction.response.send_modal(view)
    else:
        view = MyModal(True,'eng')
        await interaction.response.send_modal(view)
    session.commit()
    session.close()

@bot.tree.command(name="language")
@app_commands.describe(language="Choose language")
@app_commands.choices(language=[
    app_commands.Choice(name="English", value="eng"),
    app_commands.Choice(name="Русский", value="rus"),
    app_commands.Choice(name="中国人", value="zh"),
    app_commands.Choice(name="español", value="es"),
    app_commands.Choice(name="हिंदी", value="hi"),
])
async def language(interaction: discord.Interaction, language: str):
    languages = {"eng": "English language!", "rus": "Русский язык!","es": "Español!", "zh": "中国人!","hi": "हिंदी!"}
    await interaction.response.send_message(languages[language],ephemeral=True)
    # Ответ пользователю на выбранном языке
    Base.metadata.create_all(engine)
    session = Session()
    existing_record = session.query(TextChannels).filter_by(id=interaction.channel.id).first()
    existing_record.relation.language = language
    session.commit()
    session.close()
    

@bot.tree.command(name="update")
async def update(inter:discord.Interaction):
    """Update calendar"""
    try:
        session = Session()
        Base.metadata.create_all(engine)
        txtChannels1 = session.query(TextChannels.id).all()  
        txtChannel = txtChannels1[0][0]
        data=convertDBtodict(txtChannel)    
        language = data["language"]
        await inter.response.send_message(content=f"{languages[language]['uploadSuccesful']}!",ephemeral=True)
        a = data["cache"]
        cache = json.loads(data["cache"], cls=DecodeDateTime)
        events = get_calendar_events( data['GOOGLE_API_KEY'], data['GOOGLE_CALENDAR_ID'])
        guild = bot.get_guild(int(data['guild']))
        CHANNEL_ID =txtChannel
        #events = get_calendar_events( data['GOOGLE_API_KEY'], data['GOOGLE_CALENDAR_ID'])
        howmuch = len(
            constructEmailDateTimesDict(events)[0]
    )
        channel = bot.get_channel(int(CHANNEL_ID))
        cache["new_events"] = constructEmailDateTimesDict(events)[0]
        cache["new_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
        cache["new_formatedData"] = returnDataTime(channel, howmuch, events,cashed=True)
        cache = json.dumps(cache,cls=DateTimeEncoder)
        rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=txtChannel).first()#Обновить кэш 
        rowForUploadCache.cache = cache
        session.commit()
        session.close()
        Base.metadata.create_all(engine)
        session = Session()
        txtChannels1 = session.query(TextChannels.id).all()  
        txtChannel = txtChannels1[0][0]
        data=convertDBtodict(txtChannel) 
        a = data["cache"]
        cache = json.loads(data["cache"], cls=DecodeDateTime)





        if cache["old_reversed_formatedData"] != cache["new_reversed_formatedData"]:
            cache["old_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
            if channel:
                await channel.send("⠀⠀⠀⠀")
                await channel.send(
                embed=discord.Embed(
                        title=f"{languages[language]['uploadTimeCouldnt']}!", color=0xFF00FF
                    )
                )

                await printDataTimeReversed(channel,howmuch,data=data,language=data['language'])

        if cache["old_events"] != cache["new_events"]:
                    
            cache["old_events"] = constructEmailDateTimesDict(events)[0]
                    

            try:
                a = [zxc[0] for zxc in [*cache["new_formatedData"][list(cache["new_formatedData"].keys())[0]]]]

            except:
                a = []
            try:
                b =[zxc[0] for zxc in [*cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]]]
            except:
                b = []
            if a == []:
                a.append([])
            if b ==[]:
                b.append([])

                
            if (a != b):
                dataTimeForCache = returnDataTime(channel, howmuch, events,cashed=True)
                users_len = len(list(cache["old_formatedData"].keys())[0].split('@'))
                
                isContains = False
                if howmuch!= users_len:
                    cache["old_formatedData"] = dataTimeForCache
                    users_len = len(list(cache["old_formatedData"].keys())[0].split('@'))
                else:
                    new_dataTime = {}
                    new_dataTime[list(dataTimeForCache.keys())[0]] = []
                    for dataTime in dataTimeForCache[list(dataTimeForCache.keys())[0]]:
                        for cache_timeData in cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]:
                            oldCacheTimeData = [[datetime.datetime.fromisoformat(dateTime_str) for dateTime_str in cache_timeData[0]],cache_timeData[1]]
                            if list(dataTime[0]) == list(oldCacheTimeData[0]) :
                                new_dataTime[list(dataTimeForCache.keys())[0]].append(oldCacheTimeData)
                                isContains = True
                                break
                        if not isContains:
                            new_dataTime[list(dataTimeForCache.keys())[0]].append(dataTime)
                        isContains = False
                    cache["old_formatedData"] = new_dataTime

                            

                if guild:
                    if channel:
                        print(cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]])
                        if (users_len == int(data['lenUsers'])) or not cache["old_formatedData"][list(cache["old_formatedData"].keys())[0]]:
                            await channel.send("⠀⠀⠀⠀")
                            await channel.send(
                                embed=discord.Embed(
                                    title=f"{languages[language]['uploadTimeCould']}!", color=0xFF00FF
                                )
                            )
                            await printDataTime(channel, howmuch,data=data,withButton=True,language=data['language'])
                


        cache["new_events"] = constructEmailDateTimesDict(events)[0]
        cache["new_reversed_formatedData"] = constructEmailDateTimesDict(events)[1]
        cache["new_formatedData"] = returnDataTime(channel, howmuch, events,cashed=True)
        cache = json.dumps(cache,cls=DateTimeEncoder)
        rowForUploadCache = session.query(DataFor_TextChannels).filter_by(relationID=txtChannel).first()#Обновить кэш 
        rowForUploadCache.cache = cache
        session.commit()
        session.close()
        
        
    except:
        pass




@bot.command()
async def sync(ctx:commands.Context):
    """Sync"""
    session = Session()
    Base.metadata.create_all(engine)
    existing_record = session.query(TextChannels).filter_by(id=ctx.channel.id).first()
    language = existing_record.relation.language
    a= await bot.tree.sync()
    await ctx.send(f"{languages[language]['success']}!",ephemeral=True)  
    session.commit()
    session.close()

async def run_bot():
    while True:
        try:
            await bot.start(DISCORD_TOKEN)  # Замените на ваш токен Discord
        except discord.errors.ConnectionClosed:
            print("Connection closed, attempting to reconnect...")
              # Ждем перед повторной попыткой подключения
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            


if __name__ == "__main__":

    def run():
        app.run(host="0.0.0.0", port=8080)

    def keep_alive():
        t = Thread(target=run)
        t.start()

    keep_alive()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())