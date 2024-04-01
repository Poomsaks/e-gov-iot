import datetime
import json

import pytz
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

    # TODO โรงพยาบาลส่งเสริมสุขภาพตำบลดงเย็น
    @http.route('/line_oa_dong_yen', type='json', auth="none", methods=['POST'])
    def line_oa_dong_yen(self, **post):
        hospital_name_text = "โรงพยาบาลส่งเสริมสุขภาพตำบลดงเย็น"
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
                if self.text_message == hospital_name_text:
                    self.hospital_name = hospital_name_text
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, hospital_name_text, self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token(hospital_name_text)
                    self.repy_message_other(reply_token, self.text_message)
                if self.text_message == "ติดต่อเรา":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_contact(reply_token)
                if self.text_message == "เกี่ยวกับ":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_about(reply_token)

        return {"status": "success"}

    # TODO โรงพยาบาลส่งเสริมสุขภาพตำบลศรีเจริญ
    @http.route('/line_oa_sri_charoen', type='json', auth="none", methods=['POST'])
    def line_oa_sri_charoen(self, **post):
        hospital_name_text = "โรงพยาบาลส่งเสริมสุขภาพตำบลศรีเจริญ"
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
                if self.text_message == hospital_name_text:
                    self.hospital_name = hospital_name_text
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, hospital_name_text, self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token(hospital_name_text)
                    self.repy_message_other(reply_token, self.text_message)
                if self.text_message == "ติดต่อเรา":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_contact(reply_token)
                if self.text_message == "เกี่ยวกับ":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_about(reply_token)

        return {"status": "success"}

    # TODO โรงพยาบาลส่งเสริมสุขภาพตำบลถ่อนนาลับ
    @http.route('/line_oa_withdraw_secret', type='json', auth="none", methods=['POST'])
    def line_oa_withdraw_secret(self, **post):
        hospital_name_text = "โรงพยาบาลส่งเสริมสุขภาพตำบลถ่อนนาลับ"
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
                if self.text_message == hospital_name_text:
                    self.hospital_name = hospital_name_text
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, hospital_name_text, self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token(hospital_name_text)
                    self.repy_message_other(reply_token, self.text_message)
                if self.text_message == "ติดต่อเรา":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_contact(reply_token)
                if self.text_message == "เกี่ยวกับ":
                    self.get_date_token(hospital_name_text)
                    self.repy_message_about(reply_token)

        return {"status": "success"}

    # TODO โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล
    @http.route('/line_oa_sand_dung', type='json', auth="none", methods=['POST'])
    def line_oa_sand_dung(self, **post):
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
                if self.text_message == "โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล":
                    self.hospital_name = "โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล"
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, "โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล", self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล")
                    self.repy_message_other(reply_token, self.text_message)
                if self.text_message == "ติดต่อเรา":
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล")
                    self.repy_message_contact(reply_token)
                if self.text_message == "เกี่ยวกับ":
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตำบลทรายมูล")
                    self.repy_message_about(reply_token)

        return {"status": "success"}

    # TODO โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง
    @http.route('/line_oa_wang_thong', type='json', auth="none", methods=['POST'])
    def line_oa_wang_thong(self, **post):
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
                if self.text_message == "โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง":
                    self.hospital_name = "โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง"
                    self.get_date_token(self.text_message)
                    self.repy_message_ok(reply_token, self.text_message)
                if self.text_message in self.position_lap:
                    self.get_date_token(self.text_message)
                    self.send_one_by_one(reply_token, "โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง", self.text_message)
                if self.text_message in self.name_flex:
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง")
                    self.repy_message_other(reply_token, self.text_message)
                if self.text_message == "ติดต่อเรา":
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง")
                    self.repy_message_contact(reply_token)
                if self.text_message == "เกี่ยวกับ":
                    self.get_date_token("โรงพยาบาลส่งเสริมสุขภาพตําบลวังทอง")
                    self.repy_message_about(reply_token)

        return {"status": "success"}

    def send_one_by_one(self, reply_token, hospital, position_repy):
        thailand_timezone = pytz.timezone('Asia/Bangkok')
        login_check = request.env['main.board.iot'].sudo().search(
            [('name', '=', hospital), ('position', '=', position_repy)])
        date_time_database = ""
        humidity = ""
        temperature = ""
        position = ""
        date_time_database_thailand = ""
        for record in login_check:
            position = record.position
            for board_iot_id in record.board_iot_ids:
                # date_time_database = board_iot_id.date
                date_time_database_thailand = board_iot_id.date.astimezone(thailand_timezone)
                temperature = board_iot_id.temperature
                humidity = board_iot_id.humidity
        real_time_thailand = (date_time_database_thailand - datetime.timedelta(hours=7)).date()
        message = f'อุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {real_time_thailand} \nตำแหน่งที่ตั้ง : {position or ""}'
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

    def repy_message_contact(self, reply_token):
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
                    "altText": "Flex Message",
                    "contents": {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": "https://e-govs.com/images/Artboard_2s.png",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "label": "Action",
                                "uri": "https://linecorp.com/"
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "flex": 1,
                                    "contents": [
                                        {
                                            "type": "image",
                                            "url": "https://e-govs.com/images/16_0.jpg",
                                            "gravity": "bottom",
                                            "size": "sm",
                                            "aspectRatio": "4:3",
                                            "aspectMode": "cover"
                                        },
                                        {
                                            "type": "image",
                                            "url": "https://e-govs.com/images/17_0.jpg",
                                            "margin": "md",
                                            "size": "sm",
                                            "aspectRatio": "4:3",
                                            "aspectMode": "cover"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "flex": 2,
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Email : poomsak1994@gmail.com",
                                            "size": "xs",
                                            "flex": 1,
                                            "gravity": "top",
                                            "contents": []
                                        },
                                        {
                                            "type": "separator"
                                        },
                                        {
                                            "type": "text",
                                            "text": "85 หมู่ ต.นาพู่ อ.เพ็ญ จ.อุดรธานี 41190",
                                            "size": "xs",
                                            "flex": 2,
                                            "gravity": "center",
                                            "contents": []
                                        },
                                        {
                                            "type": "separator"
                                        },
                                        {
                                            "type": "text",
                                            "text": "086-2295093",
                                            "size": "xs",
                                            "flex": 2,
                                            "gravity": "center",
                                            "contents": []
                                        }
                                    ]
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
                                        "type": "uri",
                                        "label": "สายด่วนถึงเรา",
                                        "uri": "tel:0610375299"
                                    },
                                    "color": "#0097FFFF",
                                    "margin": "lg",
                                    "height": "sm",
                                    "style": "primary"
                                }
                            ]
                        }
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

    def repy_message_about(self, reply_token):
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
                    "altText": "Flex Message",
                    "contents": {
                        "type": "carousel",
                        "contents": [
                            {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://e-govs.com/images/11.jpg",
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
                                            "text": "ตู้เย็นเก็บวัคซีน หรือ ตู้เย็นเก็บยา คืออะไร",
                                            "weight": "bold",
                                            "size": "xl",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "เป็นตู้เย็นที่ใช้สำหรับแช่เวชภัณฑ์วัคซีน ยา เภสัชภัณฑ์ และผลิตภัณฑ์ทางชีวภาพต่างๆ",
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
                                                "label": "เรียนรู้เพิ่มเติม",
                                                "text": "ตู้วัคซีน"
                                            },
                                            "color": "#0092FFFF",
                                            "style": "primary"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://e-govs.com/images/10.png",
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
                                            "text": "ข้อควรคำนึงในการตัดสินใจเลือกซื้อตู้เย็นเก็บวัคซีน",
                                            "weight": "bold",
                                            "size": "xl",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "ผลิตภัณฑ์มีเอกสารรับรองการสอบเทียบอุณหภูมิตามมาตรฐาน ISO 17025 เพื่อความถูกต้องของอุณหภูมิ",
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
                                                "label": "เรียนรู้เพิ่มเติม",
                                                "text": "ข้อควรคำนึง"
                                            },
                                            "color": "#0092FFFF",
                                            "style": "primary"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://e-govs.com/images/12.png",
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
                                            "text": "มาตรฐานตู้เย็นวัคซีนที่ใช้ในหน่วยงานโรงพยาบาล",
                                            "weight": "bold",
                                            "size": "xl",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "ตู้เย็นวัคซีนควบคุมอุณหภูมิ 2-8 องศาเซลเซียสได้คงที่ และเก็บความเย็นไว้ได้นาน",
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
                                                "label": "เรียนรู้เพิ่มเติม",
                                                "text": "มาตรฐานตู้เย็น"
                                            },
                                            "color": "#0092FFFF",
                                            "style": "primary"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://e-govs.com/images/13.jpg",
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
                                            "text": "ตู้เย็นเก็บวัคซีน ไฟฟ้าดับทำอย่างไรดี",
                                            "weight": "bold",
                                            "size": "xl",
                                            "wrap": True,
                                            "contents": []
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "    ถ้าหากวัคซีนหรือเวชภัณฑ์ยา ที่ต้องการความเย็นในการเก็บรักษา ไม่อยู่ในสภาวะแวดล้อมเหมาะสม อาจเกิดจากการที่ ตู้แช่ยา ตู้เย็นเก็บยา ชำรุดหรือกระแสไฟฟ้าผิดปกติ ก็ส่งผลให้วัคซีนหรือยาเสื่อมคุณภาพได้",
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
                                                "label": "เรียนรู้เพิ่มเติม",
                                                "text": "ตู้เก็บวัคซีน"
                                            },
                                            "color": "#0092FFFF",
                                            "style": "primary"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

    def repy_message_ok(self, reply_token, hospital):
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
        response = requests.post(url, headers=headers, json=payload)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

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
