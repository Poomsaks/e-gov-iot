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


class ConRegister(http.Controller):

    @http.route('/api/register_user', type='json', auth='none')
    def register_user(self, **post):
        request.session.db = ConfigDatabase.database
        db_name = ConfigDatabase.database
        email = post.get("email")
        name = post.get("name")
        pass_word = post.get("password")

        time_notify = post.get("time_notify")
        position = post.get("position")
        token_line_notify = post.get("token_line_notify")
        token_line_oa = post.get("token_line_oa")
        calibrate = post.get("calibrate")

        mac_address = post.get("mac_address")

        hospital_name = post.get("hospital_name")
        hospital_address = post.get("hospital_address")
        login_check = http.request.env['res.users'].sudo().search([('login', '=', email)])
        if login_check:
            data = {'status': 200, 'response': login_check.id, 'message': 'success'}
            return data
        else:
            values = {
                'login': email,
                'name': name,
                'password': pass_word
            }
            db, login, password = http.request.env['res.users'].sudo().signup(values, None)
            request.env.cr.commit()
            uid = request.session.authenticate(db_name, login, password)
            if not uid:
                data = {'status': 400, 'message': 'เกิดข้อผิดพลาดจาก server ไม่สามารถทำรายการได้ กรุณาลองใหม่อีกครั้ง'}
                return data
            else:
                hospital_model = request.env['health.promoting.hospital'].sudo().create({
                    'name': hospital_name,
                    'flex': hospital_address,
                })
                if hospital_model:
                    data_model = request.env['main.board.iot'].sudo().search([('mac_address', '=', mac_address)])
                    if data_model:
                        data_model.write({
                            'hospital_id': hospital_model.id,
                            'time_notify': time_notify or data_model.time_notify,
                            'position': position or data_model.position,
                            'room_name': position or data_model.position,
                            'token_line_notify': token_line_notify or data_model.token_line_notify,
                            'token_line_oa': token_line_oa or data_model.token_line_oa,
                            'calibrate': calibrate or data_model.calibrate,
                            'flex_image_url': "https://e-govs.com/images/7.png" or data_model.flex_image_url
                        })
                data = {'status': 200, 'response': "success", 'message': 'success'}
                return data
