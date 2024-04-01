import time

import requests
from pytz import timezone

from odoo import models, fields, api
from odoo.http import request
from datetime import datetime, timedelta


class LineNotify(models.Model):
    _name = 'line.notify'

    @api.model
    def sent_line_notify(self):
        login_check = self.env['main.board.iot'].sudo().search(
            [('time_notify', '=', '1'), ('notify_active', '=', True)])
        date_time_database = ""
        humidity = ""
        temperature = ""

        if login_check:
            for record in login_check:
                sorted_board_iot_ids = sorted(record.board_iot_ids, key=lambda x: x.date, reverse=True)[:50]
                if sorted_board_iot_ids:
                    latest_board_iot = sorted_board_iot_ids[0]  # เลือกเพียงค่าล่าสุด
                    date_time_database = latest_board_iot.date
                    temperature = latest_board_iot.temperature
                    humidity = latest_board_iot.humidity

                avg_humidity = round(float(record.avg_humidity), 2)
                avg_temperature = round(float(record.avg_temperature), 2)
                ICT = timezone('Asia/Bangkok')
                date_time_now = datetime.now(ICT)
                date_time_zone = date_time_now.astimezone(ICT)
                formatted_time = date_time_zone.strftime('%Y-%m-%d %H:%M:%S')
                time1 = datetime.strptime(str(date_time_database), '%Y-%m-%d %H:%M:%S')
                time2 = datetime.strptime(str(formatted_time), '%Y-%m-%d %H:%M:%S')
                time_difference = time2 - time1

                if record.token_line_notify:
                    if time_difference <= timedelta(minutes=15):
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)

    def send_line_notification(self, token_line_notify, position, temperature, humidity, formatted_time,
                               avg_temperature, avg_humidity):
        message = f'\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} % \nอุณหภูมิเฉลี่ย : {avg_temperature} °C\nความชื้นเฉลี่ย : {avg_humidity} % \nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {position or ""}'
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': f'Bearer {token_line_notify}'
        }
        payload = {
            'message': message
        }
        response = requests.post(url, headers=headers, data=payload)
        data = {'status': 200, 'response': response, 'message': 'success'}
        return data

    def send_other_notification(self, token_line_notify, position):
        message = f'\n 🔴จุดบริการ {position} มีปัญหา🔴'
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': f'Bearer {token_line_notify}'
        }
        payload = {
            'message': message
        }
        response = requests.post(url, headers=headers, data=payload)
        data = {'status': 200, 'response': response, 'message': 'success'}
        return data

    # temperature = ""
    # humidity = ""
    # formatted_time = ""
    # for board_iot_id in record.board_iot_ids:
    #     temperature = board_iot_id.temperature
    #     humidity = board_iot_id.humidity
    #     date_time_now = board_iot_id.date
    #     formatted_time = date_time_now.strftime('%Y-%m-%d %H:%M:%S')
    #
    # token_line_notify = record.token_line_notify
    # message = f'\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {record.position or ""}'
    # url = 'https://notify-api.line.me/api/notify'
    # headers = {
    #     'Authorization': f'Bearer {token_line_notify}'
    # }
    # payload = {
    #     'message': message
    # }
    # response = requests.post(url, headers=headers, data=payload)
    # data = {'status': 200, 'response': response, 'message': 'success'}
    # return data

# ตั้งค่าการระบบ Cron Job
# ในไฟล์ manifest (ไฟล์ __manifest__.py) ของโมดูล
# 'data': [
#     'data/cron.xml',
# ],

# สร้างไฟล์ cron.xml ในโฟลเดอร์ data ของโมดูล
# <record id="ir_cron_my_background_job" model="ir.cron">
#     <field name="name">My Background Job</field>
#     <field name="interval_number">1</field>
#     <field name="interval_type">days</field>
#     <field name="numbercall">-1</field>
#     <field name="model_id" ref="model_my_model"/>
#     <field name="state">code</field>
#     <field name="code">model.my_background_job()</field>
# </record>
