import mail
import psycopg2
import parser
from random import randint
import json
import os
import psycopg
from datetime import datetime
import threading




class Database(object):


    parent_dir = "/home/avin/PycharmProjects/Feedback/files"

    @staticmethod
    def random_with_N_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    @staticmethod
    def GetConncetion():
        # @@ parsing settings
        settings = parser.XMLParser.Settings()
        conn = psycopg2.connect(
            host=settings.get('DatabaseHost'),
            dbname=settings.get('Database'),
            user=settings.get('DatabaseUser'),
            password=settings.get('DatabasePassword'))
        return conn


    @staticmethod
    def GetTreadMessages(id):
        try:
            conn = Database.GetConncetion()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM public.maintable WHERE treadid ='%s';",[id])
            mobile_records = cursor.fetchall()
            return mobile_records

        except (Exception, psycopg.Error) as error:
            return error
        finally:
            if conn:
                cursor.close()
                conn.close()

    @staticmethod
    def GetTreadNumbers():
        try:
            conn = Database.GetConncetion()
            cursor = conn.cursor()
            postgreSQL_select_Query = "SELECT treadnumber FROM public.treads;"
            cursor.execute(postgreSQL_select_Query)
            TreadNumbers = cursor.fetchall()
            return TreadNumbers

        except (Exception, psycopg.Error) as error:
            return datetime.now()
        finally:
            if conn:
                cursor.close()
                conn.close()


    @staticmethod
    def Put(theme,message,files,tread=None):
        try:
            conn = Database.GetConncetion()
            cursor = conn.cursor()
            if tread == None:
                notRandomCheck = "Thmsng"
                while notRandomCheck != None:
                    tread = Database.random_with_N_digits(6)
                    cursor.execute("SELECT * FROM public.maintable WHERE treadid = '%s';", [tread])
                    notRandomCheck = cursor.fetchone()

                cursor.execute("INSERT INTO treads (treadnumber) VALUES(%s)", (tread,))


            print("connected")
            try:
                cursor.execute("INSERT INTO maintable (TreadId, Theme, Message) VALUES( %s, %s, %s)",
                               (tread, theme, message))
            except Exception as e:
                print(e)

            cursor.execute("SELECT id FROM public.maintable WHERE treadid = %s and theme = %s and message = %s;",
                           (tread, theme, message))


            tempid = cursor.fetchall()
            tmpfiles = []
            if files != []:

                directory = str(tempid[0][0])

                # Parent Directory path

                # Path
                path = os.path.join(Database.parent_dir, directory)

                os.mkdir(path)

                print("OKOKOKOKOKOKOKOKOKOKOK")
                for file in files:
                    try:
                        temfilename = 'files/' + str(tempid[0][0]) + '/'

                        open(temfilename + file['filename'], 'wb').write(file['content'])
                        cursor.execute("INSERT INTO public.filetable (messageid, file) VALUES (%s, %s);",
                                       (tempid[0][0], (path + "/" + file['filename'])))
                        tmpfiles.append((path + "/" + file['filename']))
                    except Exception as e:
                        print(e)


            mailbox = mail.Mail()
            thread = threading.Thread(target=mailbox.SendToAdmin, args=(theme, message, tread, tmpfiles))
            thread.start()
        except (Exception, psycopg.Error) as error:
            return error
        finally:
            if conn:
                cursor.close()
                conn.commit()
                conn.close()

        return tread




    @staticmethod
    def GetFiles(id):
        try:

            conn = Database.GetConncetion()
            cursor = conn.cursor()
            cursor.execute("SELECT file FROM public.filetable WHERE messageid = %s;",(id,))
            files = cursor.fetchall()

            return files
        except Exception as e:
            print(e)
        finally:
            if conn:
                cursor.close()
                conn.commit()
                conn.close()