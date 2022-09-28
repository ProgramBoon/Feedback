import xml.etree.ElementTree as ET

SettingTree = ET.parse('settings.xml')
SettingRoot = SettingTree.getroot()

class XMLParser(object):

    @staticmethod
    def Settings():
        _Row = {}
        _Row['DatabaseHost'] = SettingRoot.find('DatabaseHost').text
        _Row['Database'] = SettingRoot.find('Database').text
        _Row['DatabaseUser'] = SettingRoot.find('DatabaseUser').text
        _Row['DatabasePassword'] = SettingRoot.find('DatabasePassword').text
        return (_Row)

    @staticmethod
    def Mail():
        _Row = {}
        _Row['MailPetition'] = SettingRoot.find('MailPetition').text
        _Row['MailAdmin'] = SettingRoot.find('MailAdmin').text
        _Row['MailPassword'] = SettingRoot.find('MailPassword').text
        _Row['MailHost'] = SettingRoot.find('MailHost').text
        _Row['MailPort'] = SettingRoot.find('MailPort').text
        return (_Row)