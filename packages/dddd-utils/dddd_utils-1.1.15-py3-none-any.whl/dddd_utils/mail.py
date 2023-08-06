# -*- coding: utf-8 -*-
import yagmail


class UtilMail(object):
    def __init__(self, mail_config):
        """
        mail_config = {
            'user':
            'password':
            'host':
            'port'
        }
        """
        self.__yag = yagmail.SMTP(**mail_config)

    def send(self, to, subject, contents: list, cc=None, attachments=None):
        """发送"""
        self.__yag.send(to=to, subject=subject, contents=contents, cc=cc, attachments=attachments)
