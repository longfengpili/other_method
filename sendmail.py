# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2020-11-12 17:11:17
# @Last Modified time: 2020-11-12 18:26:06
# @github: https://github.com/longfengpili

# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header

from settings import *


class Singleton(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class SendEmail(Singleton):

    def __init__(self, host: str, port: str, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def gmail_login(self):
        server = smtplib.SMTP(host=self.host, port=self.port)
        server.ehlo()
        server.starttls()
        # server.set_debuglevel(1)
        server.login(self.username, self.password)
        return server

    def email_body(self, fromname: str, toname: str, subject: str, bodytext: str, imgs: dict=None):
        body = MIMEMultipart()
        body['From'] = Header(fromname, 'utf-8')
        body['To'] = Header(toname, 'utf-8')
        body['Subject'] = Header(subject, 'utf-8')
        bodytext = MIMEText(bodytext, 'html', 'utf-8')
        body.attach(bodytext)

        if imgs:
            for iname, ipath in imgs.items():
                with open(ipath, 'rb') as f:
                    eimg = MIMEImage(f.read())
                eimg['Content-ID'] = f"<{iname}>"  # 需要在bodytext中标注<img src="cid:{iname}" class="img">
                body.attach(eimg)

        return body

    def email_attach(self, body: MIMEMultipart, attachs: list):
        for attach in attachs:
            attachname = os.path.basename(attach)
            with open(attach, 'rb') as f:
                eattach = f.read()
            eattach = MIMEText(eattach, 'base64', 'utf-8')
            eattach['content-Type'] = 'application/octet-stream'
            eattach['Content-Disposition'] = f'attachment; filename="{attachname}"'
            body.attach(eattach)

        return body

    def sendmail(self, fromaddr: str, toaddr: str or list, body: MIMEMultipart):
        server = self.gmail_login()
        server.sendmail(fromaddr, toaddr, body.as_string())


if __name__ == '__main__':
    smail = SendEmail(SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)
    bodytext = '''
    <b>test</b>
    <font color="red">rest</font>
    '''
    body = smail.email_body(fromname='test', toname='test', subject='test', bodytext=bodytext)
    smail.sendmail(FROM_ADDR, TO_ADDR, body)
