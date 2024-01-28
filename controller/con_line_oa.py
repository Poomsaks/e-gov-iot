import datetime
import json

import requests
from pytz import timezone

from odoo import http
from odoo.http import request
from .config_database import ConfigDatabase


class LineNotifyOA(http.Controller):
    hospital_name = ""

    position_lap = []
    name_flex = []
    hospital = []
    data1 = []

    @http.route('/webhook_line_oa', type='json', auth="none", methods=['POST'])
    def webhook_line_oa(self, **post):
        message_data = request.httprequest.data
        message_data_dict = json.loads(message_data)  # แปลง bytes เป็น dictionary
        events = message_data_dict.get("events", [])
        for event in events:
            self.get_hospital()
            message_type = event.get('message', {}).get('type')
            if message_type == 'text':
                self.text_message = event.get('message', {}).get('text')
                self.userIds = event.get('source', {}).get('userId')
                reply_token = event.get('replyToken')
                if self.text_message in self.hospital:
                    self.hospital_name = self.text_message
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, self.hospital_name, self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token(self.hospital_name)
                    self.repy_message_other(reply_token, self.text_message)

        return {"status": "success"}

    def send_one_by_one(self, reply_token, hospital, position_repy):
        login_check = request.env['main.board.iot'].sudo().search(
            [('name', '=', hospital), ('position', '=', position_repy)])
        date_time_database = ""
        humidity = ""
        temperature = ""
        position = ""
        for record in login_check:
            position = record.position
            for board_iot_id in record.board_iot_ids:
                date_time_database = board_iot_id.formatted_date
                temperature = board_iot_id.temperature
                humidity = board_iot_id.humidity

        message = f'อุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {date_time_database} \nตำแหน่งที่ตั้ง : {position or ""}'
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        data = {
            'replyToken': reply_token,
            'messages': [{'type': 'text', 'text': message}]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print('Failed to reply to LINE:', response.text)

    def repy_message_ok_02(self, reply_token, position, temperature, humidity, formatted_time):
        message = f'\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {position or ""}'
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "flex",
                    "altText": "This is a flex message with buttons",
                    "contents": {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "เลือกจุดติดตั้ง"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "message",
                                        "label": "ห้องยา1",
                                        "text": message
                                    }
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "message",
                                        "label": "ห้องยา2",
                                        "text": message
                                    }
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "message",
                                        "label": "ยกเลิก",
                                        "text": "ยกเลิก"
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
        requests.post(url, headers=headers, json=payload)
        # print("Response Status Code:", response.status_code)
        # print("Response Content:", response.text)

    def repy_message_ok(self, reply_token, hospital):
        # data_board_hospital = request.env['health.promoting.hospital'].sudo().search([('name', '=', hospital)])
        # for rec in data_board_hospital:
        #     self.flex = rec.flex
        # json_data = json.loads(self.flex)
        # print(json_data)
        # print("แจ้งเตือนอุณหภูมิและความชื้น")
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = {
            "replyToken": reply_token,
            "messages": [self.set_flex(hospital)]
        }

        # print(payload)
        requests.post(url, headers=headers, json=payload)
        # print("Response Status Code:", response.status_code)
        # print("Response Content:", response.text)

    def repy_message_other(self, reply_token, message):
        data_flex = request.env['main.flex'].sudo().search([('name', '=', message)])
        for rec in data_flex:
            self.flex = rec.flex
        json_data = json.loads(self.flex)
        # print(json_data)
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        payload = {
            "replyToken": reply_token,
            "messages": [json_data]
        }

        # print(payload)
        requests.post(url, headers=headers, json=payload)
        # print("Response Status Code:", response.status_code)
        # print("Response Content:", response.text)

    def get_date_flex_other(self):

        request.session.db = ConfigDatabase.database
        data_flex = request.env['main.flex'].sudo().search([])
        for rec in data_flex:
            self.name_flex.append(rec.name)

    def get_date_token(self, hospital):

        request.session.db = ConfigDatabase.database
        data_board_hospital = request.env['main.board.iot'].sudo().search([('name', '=', hospital)])
        for rec in data_board_hospital:
            self.token = rec.token_line_oa
            self.position_lap.append(rec.position)
        # print(self.token)

    def get_hospital(self):
        request.session.db = ConfigDatabase.database
        data_board_hospital = request.env['health.promoting.hospital'].sudo().search([])
        for rec in data_board_hospital:
            self.hospital.append(rec.name)

    def set_flex(self, hospital):
        self.data1 = []
        request.session.db = ConfigDatabase.database
        data_board_hospital = request.env['main.board.iot'].sudo().search([('name', '=', hospital)])
        for rec in data_board_hospital:
            flex1 = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": rec.flex_image_url,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": rec.room_name,
                            "weight": "bold",
                            "size": "xxl",
                            "wrap": True,
                            "contents": []
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "จุดที่ 1 : " + rec.position,
                                    "weight": "bold",
                                    "size": "sm",
                                    "flex": 0,
                                    "wrap": True,
                                    "contents": []
                                }
                            ]
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "ดูอุณหภูมิ",
                                "text": rec.position
                            },
                            "color": "#00AFF5FF",
                            "style": "primary"
                        }
                    ]
                }
            }
            self.data1.append(flex1)
        payload = {
            "type": "flex",
            "altText": "แจ้งเตือนอุณหภูมิและความชื้น",
            "contents": {
                "type": "carousel",
                "contents": self.data1
            }
        }
        return payload
