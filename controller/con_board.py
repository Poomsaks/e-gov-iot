# -*- coding: utf-8 -*-
import base64
import json
import numpy as np
import pytz
import requests
import werkzeug
from pytz import timezone

from odoo import http, api
from odoo.http import request
from .config_database import ConfigDatabase
import datetime


class ConBoard(http.Controller):
    @http.route('/api/test_bot_notify', type='json', auth='none')
    def test_bot_notify(self, **post):
        request.session.db = ConfigDatabase.database
        login_check = http.request.env['main.board.iot'].sudo().search([('mac_address', '=', post.get("mac_address"))])
        ICT = timezone('Asia/Bangkok')
        date_time_now = datetime.datetime.now(ICT)
        date_time_zone = date_time_now.astimezone(ICT)
        formatted_time = date_time_zone.strftime('%Y-%m-%d %H:%M:%S')
        temperature = post.get("temperature")
        humidity = post.get("humidity")

        message = f'\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {login_check.position or ""}'

        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': 'Bearer H5QxwkazDGJXRrbXltym16g2CLTMHTMAp7Kq7pTniEL'
        }
        payload = {
            'message': message
        }
        response = requests.post(url, headers=headers, data=payload)
        data = {'status': 200, 'response': response, 'message': 'success'}
        return json.dumps(data)
        # print(response.json())

    def line_notify(self, temperature, humidity, token_line_notify, position, formatted_time):
        message = f'\n 🔴อุณหภูมิมีการเปลี่ยนแปลง🔴\nอุณหภูมิ : {temperature} °C\nความชื้น : {humidity} %\nวันที่ : {formatted_time} \nตำแหน่งที่ตั้ง : {position or ""}'
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': f'Bearer {token_line_notify}'
        }
        payload = {
            'message': message
        }
        requests.post(url, headers=headers, data=payload)

    def get_session_info(self):
        request.session.check_security()
        request.uid = request.session.uid
        request.disable_db = False
        return request.env['ir.http'].session_info()

    @http.route('/api/update_time_data', type='json', auth='none')
    def update_time_data(self, **post):
        request.session.db = ConfigDatabase.database
        db_name = ConfigDatabase.database

        email = post.get("mac_address")
        temperature = post.get('temperature')
        humidity = post.get('humidity')
        light = post.get('light')
        ip_connect = post.get('ip_connect')

        login_check = http.request.env['res.users'].sudo().search([('login', '=', email)])
        if login_check:
            self.update_data(email, temperature, humidity, light, ip_connect)
            data = {'status': 200, 'response': login_check.id, 'message': 'success'}
            return data
        else:
            values = {
                'login': email,
                'name': email,
                'password': "1234"
            }
            db, login, password = request.env['res.users'].sudo().signup(values, None)
            request.env.cr.commit()
            uid = request.session.authenticate(db_name, login, password)
            if not uid:
                data = {'status': 400, 'message': 'เกิดข้อผิดพลาดจาก server ไม่สามารถทำรายการได้ กรุณาลองใหม่อีกครั้ง'}
                return data
            else:
                self.update_data(email, temperature, humidity, light, ip_connect)
                data = {'status': 200, 'response': "success", 'message': 'success'}
                return data

    def update_data(self, mac_address, temperature, humidity, light, ip_connect):
        ICT = timezone('Asia/Bangkok')
        date_time_now_utc = datetime.datetime.utcnow()
        date_time_now = date_time_now_utc.replace(tzinfo=timezone('UTC')).astimezone(ICT)
        formatted_time = date_time_now.strftime('%Y-%m-%d %H:%M:%S')

        data_model = http.request.env['main.board.iot'].sudo().search(
            [('mac_address', '=', mac_address)], limit=1)
        if data_model:
            with api.Environment.manage():
                data_model.write({
                    'board_iot_ids': [(0, 0, {
                        'mac_address': mac_address,
                        'temperature': temperature,
                        'date': formatted_time,
                        'humidity': humidity,
                        'light': light,
                        'ip_connect': ip_connect,
                    })],
                })
        else:
            with api.Environment.manage():
                new_data_model = http.request.env['main.board.iot'].sudo().create({
                    'mac_address': mac_address,
                    'board_iot_ids': [(0, 0, {
                        'mac_address': mac_address,
                        'temperature': temperature,
                        'date': formatted_time,
                        'humidity': humidity,
                        'light': light,
                        'ip_connect': ip_connect,
                    })],
                })
            data_model = new_data_model

        data = {'status': 200, 'response': data_model.id, 'message': 'success'}
        return json.dumps(data)

    @http.route('/api/send_notify', type='json', auth='none')
    def send_notify(self, **post):
        request.session.db = ConfigDatabase.database

        email = post.get("mac_address")
        temperature = post.get('temperature')
        humidity = post.get('humidity')
        light = post.get('light')
        ip_connect = post.get('ip_connect')

        self.update_data_send(email, temperature, humidity, light, ip_connect)

    def update_data_send(self, mac_address, temperature, humidity, light, ip_connect):
        ICT = timezone('Asia/Bangkok')
        date_time_now_utc = datetime.datetime.utcnow()
        date_time_now = date_time_now_utc.replace(tzinfo=timezone('UTC')).astimezone(ICT)
        formatted_time = date_time_now.strftime('%Y-%m-%d %H:%M:%S')

        with api.Environment.manage():
            data_model = http.request.env['main.board.iot'].sudo().search(
                [('mac_address', '=', mac_address)], limit=1)
            if data_model:
                data_model.write({
                    'board_iot_ids': [(0, 0, {
                        'mac_address': mac_address,
                        'temperature': temperature,
                        'date': formatted_time,
                        'humidity': humidity,
                        'light': light,
                        'ip_connect': ip_connect,
                    })],
                })
            else:
                new_data_model = http.request.env['main.board.iot'].sudo().create({
                    'mac_address': mac_address,
                    'board_iot_ids': [(0, 0, {
                        'mac_address': mac_address,
                        'temperature': temperature,
                        'date': formatted_time,
                        'humidity': humidity,
                        'light': light,
                        'ip_connect': ip_connect,
                    })],
                })
                data_model = new_data_model
        # self.line_notify(temperature, humidity, data_model.token_line_notify, data_model.position, formatted_time)
        request.env['send.line.notify.new'].sent_line_notify_new(temperature, humidity, data_model.token_line_notify, data_model.position, formatted_time)
        data = {'status': 200, 'response': data_model.id, 'message': 'success'}
        return json.dumps(data)

    # @http.route('/api/authenticate_iot', type='json', auth='none')
    # def authenticate_iot(self, **post):
    #     request.session.db = ConfigDatabase.database
    #     db_name = ConfigDatabase.database
    #     email = post.get("mac_address")
    #     login_check = http.request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
    #     if login_check:
    #         request.session.authenticate(db_name, email, "1234")
    #         return request.env['ir.http'].session_info()
    #     else:
    #         values = {
    #             'login': email,
    #             'name': email,
    #             'password': "1234"
    #         }
    #         db, login, password = request.env['res.users'].sudo().signup(values, None)
    #         request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
    #         uid = request.session.authenticate(db_name, login, password)
    #         if not uid:
    #             data = {'status': 400, 'message': 'เกิดข้อผิดพลาดจาก server ไม่สามารถทำรายการได้ กรุณาลองใหม่อีกครั้ง'}
    #             return data
    #         else:
    #             return request.env['ir.http'].session_info()
    #
    # @http.route('/api/update_time_data', type='json', auth="none")
    # def update_time_data(self, **post):
    #     request.session.db = ConfigDatabase.database
    #     ICT = timezone('Asia/Bangkok')
    #     date_time_now = datetime.datetime.now(ICT)
    #     formatted_time = date_time_now.strftime('%Y-%m-%d %H:%M:%S')
    #
    #     mac_address = post.get('mac_address')
    #     temperature = post.get('temperature')
    #     humidity = post.get('humidity')
    #     light = post.get('light')
    #     ip_connect = post.get('ip_connect')
    #
    #     data_model = http.request.env['main.board.iot'].sudo().search(
    #         [('mac_address', '=', mac_address)], limit=1)
    #     doc_detail = [{
    #         'main_board_iot_id': data_model.id if data_model else False,
    #         'mac_address': mac_address,
    #         'temperature': temperature,
    #         'date': formatted_time,
    #         'humidity': humidity,
    #         'light': light,
    #         'ip_connect': ip_connect,
    #     }]
    #
    #     if data_model:
    #         data_model.write({
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #     else:
    #         data_model.create({
    #             'mac_address': mac_address,
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #     data = {'status': 200, 'response': data_model.id, 'message': 'success'}
    #     return json.dumps(data)

    # @http.route('/api/update_time_data', type='json', auth='none')
    # def update_time_data(self, **post):
    #     request.session.db = ConfigDatabase.database
    #     db_name = ConfigDatabase.database
    #     email = post.get("mac_address")
    #     login_check = http.request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
    #     if login_check:
    #         request.session.authenticate(db_name, email, "1234")
    #         return request.env['ir.http'].session_info()
    #     else:
    #         values = {
    #             'login': email,
    #             'name': email,
    #             'password': "1234"
    #         }
    #         db, login, password = request.env['res.users'].sudo().signup(values, None)
    #         request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
    #         uid = request.session.authenticate(db_name, login, password)
    #         if not uid:
    #             data = {'status': 400, 'message': 'เกิดข้อผิดพลาดจาก server ไม่สามารถทำรายการได้ กรุณาลองใหม่อีกครั้ง'}
    #             return data
    #         else:
    #             return request.env['ir.http'].session_info()
    #
    # def update_data(self, mac_address, temperature, humidity, light, ip_connect):
    #     ICT = timezone('Asia/Bangkok')
    #     date_time_now = datetime.datetime.now(ICT)
    #     date_time_zone = date_time_now.astimezone(ICT)
    #     formatted_time = date_time_zone.strftime('%Y-%m-%d %H:%M:%S')
    #
    #     data_model = http.request.env['main.board.iot'].sudo().search(
    #         [('mac_address', '=', mac_address)])
    #     doc_detail = [{
    #         'main_board_iot_id': data_model.id if data_model else False,
    #         'mac_address': mac_address,
    #         'temperature': temperature,
    #         'date': formatted_time,
    #         'humidity': humidity,
    #         'light': light,
    #         'ip_connect': ip_connect,
    #     }]
    #
    #     if data_model:
    #         data_model.write({
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #         # self.line_notify(mac_address, temperature, humidity)
    #     else:
    #         http.request.env['main.board.iot'].create({
    #             'mac_address': mac_address,
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #         # self.line_notify(mac_address, temperature, humidity)
    #     data = {'status': 200, 'response': data_model.id, 'message': 'success'}
    #     return json.dumps(data)
    # @http.route('/api/update_time_data', type='json', auth="none")
    # def update_time_data(self, **post):
    #     ICT = timezone('Asia/Bangkok')
    #     date_time_now = datetime.datetime.now(ICT)
    #     date_time_zone = date_time_now.astimezone(ICT)
    #     formatted_time = date_time_zone.strftime('%Y-%m-%d %H:%M:%S')
    #
    #     mac_address = post.get('mac_address')
    #     temperature = post.get('temperature')
    #     humidity = post.get('humidity')
    #     light = post.get('light')
    #     ip_connect = post.get('ip_connect')
    #
    #     data_model = http.request.env['main.board.iot'].sudo().search(
    #         [('mac_address', '=', mac_address)], limit=1)
    #     doc_detail = [{
    #         'main_board_iot_id': data_model.id if data_model else False,
    #         'mac_address': mac_address,
    #         'temperature': temperature,
    #         'date': formatted_time,
    #         'humidity': humidity,
    #         'light': light,
    #         'ip_connect': ip_connect,
    #     }]
    #
    #     if data_model:
    #         data_model.write({
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #     else:
    #         data_model.create({
    #             'mac_address': mac_address,
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #     data = {'status': 200, 'response': data_model.id, 'message': 'success'}
    #     return json.dumps(data)

    # @http.route('/api/update_time_data', type='json', auth="none", csrf=False)
    # def update_time_data(self, **post):
    #     if 'authenticated' not in http.request.session:
    #         uid = http.request.session.authenticate("e-gov-iot", "admin", "1234")
    #         if not uid:
    #             data = {'status': 500, 'response': "ไม่ผ่าน", 'message': 'error'}
    #             return json.dumps(data)
    #         else:
    #             http.request.session['authenticated'] = True
    #
    #     data_model = http.request.env['main.board.iot'].sudo().search([('mac_address', '=', post.get('mac_address'))])
    #     doc_detail = [{
    #         'main_board_iot_id': data_model.id if data_model else False,
    #         'mac_address': post.get('mac_address'),
    #         'temperature': post.get('temperature'),
    #         'moisture': post.get('moisture'),
    #         'light': post.get('light'),
    #         'ip_connect': post.get('ip_connect'),
    #     }]
    #
    #     if data_model:
    #         data_model.write({
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #     else:
    #         http.request.env['main.board.iot'].create({
    #             'mac_address': post.get('mac_address'),
    #             'board_iot_ids': [(0, 0, detail) for detail in doc_detail],
    #         })
    #
    #     data = {'status': 200, 'response': "success", 'message': 'success'}
    #     return json.dumps(data)

    # @http.route('/api/update_time_data', type='json', auth="none")
    # def update_time_data(self, **post):
    #     uid = request.session.authenticate("e-gov-iot", "admin", "1234")
    #     if not uid:
    #         data = {'status': 500, 'response': "ไม่ผ่าน", 'message': 'error'}
    #         return json.dumps(data)
    #     else:
    #         data_model = request.env['mdm.board.iot'].sudo().search([])
    #         data_create = data_model.create({
    #             'name': post.get('name'),
    #             'temperature': post.get('temperature'),
    #             'moisture': post.get('moisture'),
    #             'light': post.get('light'),
    #             'ip_connect': post.get('ip_connect'),
    #             'status': post.get('status')
    #         })
    #     data = {'status': 200, 'response': data_create.id, 'message': 'success'}
    #     return json.dumps(data)

    @http.route('/api/update_time_notify', type='json', auth='user')
    def update_time_notify(self, **post):
        data_model = request.env['main.board.iot'].sudo().search([('id', '=', post.get('id'))])
        if data_model:
            with api.Environment.manage():
                data_model.write({
                    'calibrate': post.get('calibrate') or data_model.calibrate,
                    'time_notify': post.get('time_notify') or data_model.time_notify,
                    'position': post.get('position') or data_model.position,
                })
            data = {'status': 200, 'response': data_model.id, 'message': 'success'}
            return json.dumps(data)
        else:
            data = {'status': 200, 'response': 'ไม่พบข้อมูล', 'message': 'success'}
            return json.dumps(data)

    @http.route('/api/authenticate_iot', type='json', auth="none")
    def authenticate_iot(self, **post):
        db = ConfigDatabase.database
        request.session.authenticate(db, post.get('login'), post.get('password'))
        return request.env['ir.http'].session_info()
