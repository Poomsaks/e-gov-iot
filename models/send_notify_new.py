import time

import requests
from pytz import timezone

from odoo import models, fields, api
from odoo.http import request
from datetime import datetime, timedelta


class SendLineNotifyNew(models.Model):
    _name = 'send.line.notify.new'

    @api.model
    def sent_line_notify_new(self, temperature, humidity, token_line_notify, position, formatted_time):
        message = f'\n 🔴อุณหภูมิมีการเปลี่ยนแปลง🔴\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {position or ""}'
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': f'Bearer {token_line_notify}'
        }
        payload = {
            'message': message
        }
        requests.post(url, headers=headers, data=payload)
