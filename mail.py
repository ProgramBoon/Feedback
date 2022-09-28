from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import psycopg2

import parser
from pathlib import Path




class Mail(object):

    @staticmethod
    def GetSet():

        settings = parser.XMLParser.Mail()
        host=settings.get('MailHost')
        port=settings.get('MailPort')
        mailpetition=settings.get('MailPetition')
        mailadmin=settings.get('MailAdmin')
        password=settings.get('MailPassword')
        Getset = {"host":host, "port": port, "Petition": mailpetition,"Admin": mailadmin,"Password":password}

        return Getset


    def SendToAdmin(self, theme,message,tread,files = None):
        Settings = Mail.GetSet()

        msg = MIMEMultipart()
        msg["From"] =Settings.get("Petition")
        msg["To"] = Settings.get("Admin")
        msg['Subject'] = theme + " Идентификатор (" + str(tread) + ")"
        body_text = message
        body_part = MIMEText(body_text, 'plain')
        msg.attach(body_part)
        host= Settings.get("host")
        port = Settings.get("port")
        password = Settings.get("Password")




        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

        with smtplib.SMTP(host=host, port=port) as smtp_obj:  # ENVIAR DESDE UN DOMINIO PERSONALIZADO.
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.ehlo()
            smtp_obj.login(msg["From"], password)

            try:
                smtp_obj.sendmail(msg["From"], msg["To"], msg.as_string())
            except Exception as e:
                print(e)