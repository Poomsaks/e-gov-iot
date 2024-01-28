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
        login_check = self.env['main.board.iot'].sudo().search([])
        date_time_database = ""
        humidity = ""
        temperature = ""

        for record in login_check:
            time_count = record.time_count
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

            if record.message_send_notify != temperature:
                if record.time_notify == '1':
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)
                if record.time_notify == '2' and time_count != 1 and time_count != 3 and time_count != 5:
                    # print("แจ้งเตือนทุก 2 นาที " + record.position)
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        record.write({'message_send_notify': temperature})
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)
                if record.time_notify == '3' and time_count != 1 and time_count != 2 and time_count != 4 and time_count != 5:
                    # print("แจ้งเตือนทุก 3 นาที " + record.position)
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        record.write({'message_send_notify': temperature})
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)
                if record.time_notify == '4' and time_count != 1 and time_count != 2 and time_count != 3 and time_count != 5 and time_count != 6:
                    # print("แจ้งเตือนทุก 4 นาที " + record.position)
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        record.write({'message_send_notify': temperature})
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)
                if record.time_notify == '5' and time_count != 1 and time_count != 2 and time_count != 3 and time_count != 4 and time_count != 6:
                    # print("แจ้งเตือนทุก 5 นาที " + record.position)
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        record.write({'message_send_notify': temperature})
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)
                if record.time_notify == '6' and time_count != 1 and time_count != 2 and time_count != 3 and time_count != 4 and time_count != 5:
                    # print("แจ้งเตือนทุก 6 นาที " + record.position)
                    with api.Environment.manage():
                        record.write({'message_send_notify': temperature})
                    if time_difference <= timedelta(minutes=15):
                        with api.Environment.manage():
                            record.write({'message_send_notify': temperature})
                        self.send_line_notification(record.token_line_notify, record.position, temperature, humidity,
                                                    formatted_time, avg_humidity, avg_temperature)
                    else:
                        self.send_other_notification(record.token_line_notify, record.position)

            else:
                self.send_later_notification(record.token_line_notify, record.mac_address)

            with api.Environment.manage():
                record.write({
                    'time_count': time_count + 1,
                })
            if time_count == 6:
                with api.Environment.manage():
                    record.write({
                        'time_count': 1,
                    })

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
        message = f'\n ⚠️จุดบริการ {position} มีปัญหา⚠️'
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

    def send_later_notification(self, token_line_notify, mac_address):
        time.sleep(60)
        login_check = self.env['main.board.iot'].sudo().search([('mac_address', '=', mac_address)])
        humidity = ""
        temperature = ""
        avg_humidity = ""
        avg_temperature = ""
        formatted_time = ""
        position = ""
        for record in login_check:
            sorted_board_iot_ids = sorted(record.board_iot_ids, key=lambda x: x.date, reverse=True)[:50]
            if sorted_board_iot_ids:
                latest_board_iot = sorted_board_iot_ids[0]
                temperature = latest_board_iot.temperature
                humidity = latest_board_iot.humidity
            position = record.position
            avg_humidity = round(float(record.avg_humidity), 2)
            avg_temperature = round(float(record.avg_temperature), 2)
            ICT = timezone('Asia/Bangkok')
            date_time_now = datetime.now(ICT)
            date_time_zone = date_time_now.astimezone(ICT)
            formatted_time = date_time_zone.strftime('%Y-%m-%d %H:%M:%S')
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
