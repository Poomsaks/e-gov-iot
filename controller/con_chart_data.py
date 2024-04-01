# -*- coding: utf-8 -*-
import base64
import json

import numpy as np
import pytz
import requests
import werkzeug
from numpy import average
from pytz import timezone

from odoo import http
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from .con_check_role import ConCheckRole
from .config_database import ConfigDatabase
import datetime


class ConChartData(http.Controller):

    @http.route('/api/get_time_data', type='json', auth='none')
    def get_time_data(self, **post):
        request.session.db = ConfigDatabase.database
        hospital_info = request.env['main.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address'))])
        if hospital_info:
            data_info = request.env['main.board.iot'].sudo().search(
                [('hospital_id', '=', hospital_info.hospital_id.id)])
            if data_info:
                data_s = []
                for rec in data_info:
                    vals = {
                        'id': rec.id,
                        'hospital_id': rec.hospital_id.id or "",
                        'name': rec.name or "",
                        'image': rec.image or "",
                        'address': rec.address or "",
                        'position': rec.position or "",
                        'calibrate': rec.calibrate or "",
                        'mac_address': rec.mac_address or "",
                        'time_notify_select_id': rec.time_notify,
                        'time_notify': dict(rec._fields['time_notify'].selection).get(rec.time_notify),
                    }
                    data_s.append(vals)
                data = {'status': 200, 'response': data_s, 'message': 'success'}
                return data
            else:
                data = {'status': 500, 'response': 'ไม่พบข้อมูล', 'message': 'error'}
                return data
        else:
            data = {'status': 500, 'response': 'ไม่พบข้อมูล', 'message': 'error'}
            return data

    @http.route('/api/get_time_data_excel', type='json', auth='none')
    def get_time_data_excel(self, **post):
        request.session.db = ConfigDatabase.database
        start_datetime_str = post.get('start_datetime')
        end_datetime_str = post.get('end_datetime')
        records = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address')),
            ('date', '>=', datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')),
            ('date', '<=', datetime.datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S'))
        ])
        data_all = []
        temperature_data = []
        humidity_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        date_data = []

        for record in records:
            data_all.append({
                'temperature': float(record.temperature),
                'humidity': float(record.humidity),
                'date': record.date.strftime('%Y-%m-%d %H:%M:%S')
            })
            temperature_data.append(float(record.temperature))
            humidity_data.append(float(record.humidity))
            max_humidity_data.append(float(record.temperature))
            min_humidity_data.append(float(record.temperature))
            max_temperature_data.append(float(record.humidity))
            min_temperature_data.append(float(record.humidity))
            date_data.append(record.date.strftime('%Y-%m-%d %H:%M:%S'))

        average_temperature = sum(temperature_data) / len(temperature_data) if temperature_data else 0
        average_humidity = sum(humidity_data) / len(humidity_data) if humidity_data else 0

        data = {
            'status': 200,
            'response': data_all,
            'temperature': temperature_data,
            'humidity': humidity_data,
            'average_temperature': average_temperature,
            'average_humidity': average_humidity,
            'max_humidity_data': max(max_humidity_data, default=0),
            'min_humidity_data': min(min_humidity_data, default=0),
            'max_temperature_data': max(max_temperature_data, default=0),
            'min_temperature_data': min(min_temperature_data, default=0),
            'date_data': date_data,
        }
        return data

    @http.route('/api/get_time_data_by_day', type='json', auth='none')
    def get_time_data_by_day(self, **post):
        request.session.db = ConfigDatabase.database
        ICT = timezone('Asia/Bangkok')
        current_datetime = datetime.datetime.now(ICT)
        data_info = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address')),
            ('date', '>=', current_datetime.strftime('%Y-%m-%d 00:00:00')),
            ('date', '<=', current_datetime.strftime('%Y-%m-%d 23:59:59'))
        ])
        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        if data_info:
            data_s = []
            for rec in data_info:
                # existing_hours = {data[:2] for data in date_data if data}
                if rec.date:
                    rounded_date = rec.date.replace(second=0, microsecond=0, minute=(rec.date.minute // 30) * 30)
                    hour_to_append = rounded_date.strftime('%H:%M')
                    if hour_to_append not in date_data:
                        date_data.append(hour_to_append)
                        temperature_data.append(rec.temperature or "")
                        humidity_data.append(rec.humidity or "")

                vals = {
                    'id': rec.id,
                    'mac_address': rec.mac_address or "",
                    'temperature': rec.temperature or "",
                    'humidity': rec.humidity or "",
                    'light': rec.light or "",
                    'ip_connect': rec.ip_connect or "",
                    'date': rec.date or "",
                    'status': rec.status or "",
                }
                data_s.append(vals)
            hospital_info = request.env['main.board.iot'].sudo().search([
                ('mac_address', '=', post.get('mac_address'))], limit=1)

            max_humidity_data.append(hospital_info.max_temperature)
            min_humidity_data.append(hospital_info.min_temperature)

            max_temperature_data.append(hospital_info.max_humidity)
            min_temperature_data.append(hospital_info.min_humidity)

            data = {'status': 200, 'response': data_s, 'message': 'success',
                    'max_humidity_data': max_humidity_data,
                    'min_humidity_data': min_humidity_data,
                    'max_temperature_data': max_temperature_data,
                    'min_temperature_data': min_temperature_data,
                    'temperature': temperature_data,
                    'humidity': humidity_data,
                    'date_data': date_data,
                    'current_datetime': current_datetime}
            return data
        else:
            data = {'status': 500, 'response': 'ไม่พบข้อมูล', 'message': 'error'}
            return data

    @http.route('/api/get_time_data_by_all', type='json', auth='none')
    def get_time_data_by_all(self, **post):
        request.session.db = ConfigDatabase.database
        start_datetime_str = post.get('start_datetime')
        end_datetime_str = post.get('end_datetime')
        mac_address = post.get('mac_address')
        start_datetime = datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
        sum_date = end_datetime - start_datetime
        records = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', mac_address),
            ('date', '>=', datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')),
            ('date', '<=', datetime.datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S'))
        ])
        if sum_date.days <= 1:
            return self.get_data_chart_by_day(records, start_datetime, end_datetime)
        elif 2 <= sum_date.days <= 30:
            return self.get_data_chart_by_week(records, start_datetime, end_datetime)
        elif 30 <= sum_date.days <= 365:
            return self.get_data_chart_by_year(records, start_datetime, end_datetime)

    def get_data_chart_by_day(self, records, start_datetime, end_datetime):
        result = {}
        interval = datetime.timedelta(minutes=30)  # Set the interval to 1 hour

        for record in records:
            record_datetime = datetime.datetime.strptime(str(record.date), "%Y-%m-%d %H:%M:%S")

            # Round down the datetime to the nearest hour
            rounded_datetime = record_datetime.replace(second=0, microsecond=0,
                                                       minute=(record_datetime.minute // 30) * 30)

            if rounded_datetime not in result:
                result[rounded_datetime] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }

            result[rounded_datetime]['temperature_sum'] += float(record.temperature)
            result[rounded_datetime]['humidity_sum'] += float(record.humidity)
            result[rounded_datetime]['count'] += 1

            result[rounded_datetime]['max_temperature'] = max(result[rounded_datetime]['max_temperature'],
                                                              float(record.temperature))
            result[rounded_datetime]['min_temperature'] = min(result[rounded_datetime]['min_temperature'],
                                                              float(record.temperature))
            result[rounded_datetime]['max_humidity'] = max(result[rounded_datetime]['max_humidity'],
                                                           float(record.humidity))
            result[rounded_datetime]['min_humidity'] = min(result[rounded_datetime]['min_humidity'],
                                                           float(record.humidity))

        data_all = []
        temperature_data = []
        humidity_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        date_data = []

        start_datetime = min(result.keys())
        end_datetime = max(result.keys())

        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            if current_datetime in result:
                values = result[current_datetime]
                data_all.append({
                    'day': str(current_datetime.day).zfill(2),
                    'month': str(current_datetime.month).zfill(2),
                    'year': current_datetime.year,
                    'hour': str(current_datetime.hour).zfill(2),
                    'average_temperature': values['temperature_sum'] / values['count'],
                    'average_humidity': values['humidity_sum'] / values['count'],
                    'max_temperature': values['max_temperature'],
                    'min_temperature': values['min_temperature'],
                    'max_humidity': values['max_humidity'],
                    'min_humidity': values['min_humidity'],
                })
                temperature_data.append(values['temperature_sum'] / values['count'])
                humidity_data.append(values['humidity_sum'] / values['count'])

                max_humidity_data.append(values['max_temperature'])
                min_humidity_data.append(values['min_temperature'])
                max_temperature_data.append(values['max_humidity'])
                min_temperature_data.append(values['min_humidity'])
                date_data.append(current_datetime.strftime("%H:%M"))

            current_datetime += interval

        data = {
            'status': 200,
            'response': data_all,
            'temperature': temperature_data,
            'humidity': humidity_data,
            'average_temperature': sum(temperature_data) / len(temperature_data),
            'average_humidity': sum(humidity_data) / len(humidity_data),
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'current_datetime': end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        }

        return data

    def get_data_chart_by_week(self, records, start_datetime, end_datetime):
        result = {}
        for record in records:
            day = record.date.day
            month = record.date.month
            year = record.date.year

            if (day, month, year) not in result:
                result[(day, month, year)] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['humidity_sum'] += float(record.humidity)
            result[(day, month, year)]['count'] += 1

            result[(day, month, year)]['max_temperature'] = max(result[(day, month, year)]['max_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['min_temperature'] = min(result[(day, month, year)]['min_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['max_humidity'] = max(result[(day, month, year)]['max_humidity'],
                                                             float(record.humidity))
            result[(day, month, year)]['min_humidity'] = min(result[(day, month, year)]['min_humidity'],
                                                             float(record.humidity))

        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        data_all = []
        for (day, month, year), values in result.items():
            data_all.append({
                'day': str(day).zfill(2),
                'month': str(month).zfill(2),
                'year': year,
                'average_temperature': values['temperature_sum'] / values['count'],
                'average_humidity': values['humidity_sum'] / values['count'],
                'max_temperature': values['max_temperature'],
                'min_temperature': values['min_temperature'],
                'max_humidity': values['max_humidity'],
                'min_humidity': values['min_humidity'],
            })

            temperature_data.append(values['temperature_sum'] / values['count'])
            humidity_data.append(values['humidity_sum'] / values['count'])

            max_humidity_data.append(values['max_temperature'])
            min_humidity_data.append(values['min_temperature'])
            max_temperature_data.append(values['max_humidity'])
            min_temperature_data.append(values['min_humidity'])
            date_data.append(f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}")
        data = {
            'status': 200,
            'response': data_all,
            'temperature': temperature_data,
            'humidity': humidity_data,
            'average_temperature': sum(temperature_data) / len(temperature_data),
            'average_humidity': sum(humidity_data) / len(humidity_data),
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime,
            'current_datetime': end_datetime
        }
        return data

    def get_data_chart_by_year(self, records, start_datetime, end_datetime):
        result = {}
        for record in records:
            day = record.date.day
            month = record.date.month
            year = record.date.year

            if (month, year) not in result:
                result[(month, year)] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }
            result[(month, year)]['temperature_sum'] += float(record.temperature)
            result[(month, year)]['temperature_sum'] += float(record.temperature)
            result[(month, year)]['humidity_sum'] += float(record.humidity)
            result[(month, year)]['count'] += 1

            result[(month, year)]['max_temperature'] = max(result[(month, year)]['max_temperature'],
                                                           float(record.temperature))
            result[(month, year)]['min_temperature'] = min(result[(month, year)]['min_temperature'],
                                                           float(record.temperature))
            result[(month, year)]['max_humidity'] = max(result[(month, year)]['max_humidity'],
                                                        float(record.humidity))
            result[(month, year)]['min_humidity'] = min(result[(month, year)]['min_humidity'],
                                                        float(record.humidity))

        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        averages = []
        for (month, year), values in result.items():
            averages.append({
                'month': str(month).zfill(2),
                'year': year,
                'average_temperature': values['temperature_sum'] / values['count'],
                'average_humidity': values['humidity_sum'] / values['count'],
                'max_temperature': values['max_temperature'],
                'min_temperature': values['min_temperature'],
                'max_humidity': values['max_humidity'],
                'min_humidity': values['min_humidity'],
            })

            temperature_data.append(values['temperature_sum'] / values['count'])
            humidity_data.append(values['humidity_sum'] / values['count'])

            max_humidity_data.append(values['max_temperature'])
            min_humidity_data.append(values['min_temperature'])
            max_temperature_data.append(values['max_humidity'])
            min_temperature_data.append(values['min_humidity'])
            date_data.append(f"{str(month).zfill(2)}/{year}")
        data = {
            'status': 200,
            'response': averages,
            'temperature': temperature_data,
            'humidity': humidity_data,
            'average_temperature': sum(temperature_data) / len(temperature_data),
            'average_humidity': sum(humidity_data) / len(humidity_data),
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime,
            'current_datetime': end_datetime
        }
        return data

    @http.route('/api/get_data_print_day', type='json', auth='none')
    def get_data_print_day(self, **post):
        request.session.db = ConfigDatabase.database
        query = """
            WITH filtered_data AS (
                SELECT *,
                       ROW_NUMBER() OVER (PARTITION BY DATE_TRUNC('day', date), EXTRACT(HOUR FROM date) ORDER BY date) AS row_num
                FROM public.mdm_board_iot 
                WHERE date BETWEEN %s AND %s AND mac_address = %s
                AND (EXTRACT(HOUR FROM date) = 9 OR EXTRACT(HOUR FROM date) = 15)
            )
            SELECT *
            FROM filtered_data
            WHERE row_num = 1;
        """
        start_date = post.get('start_datetime')
        end_date = post.get('end_datetime')
        mac_address = post.get('mac_address')
        request.env.cr.execute(query, (start_date, end_date, mac_address))
        return request.env.cr.dictfetchall()

    @http.route('/api/get_data_print_day_v2', type='json', auth='none')
    def get_data_print_day_v2(self, **post):
        request.session.db = ConfigDatabase.database
        query = """
                    SELECT date, temperature, humidity
FROM (
    SELECT date, temperature, humidity,
           ROW_NUMBER() OVER (PARTITION BY date::date, EXTRACT(HOUR FROM date) ORDER BY date) AS rn
    FROM mdm_board_iot 
    WHERE (EXTRACT(HOUR FROM date) = 9 OR EXTRACT(HOUR FROM date) = 15)
    AND date BETWEEN '2024-02-01' AND '2024-02-10'
) AS sub
WHERE rn = 1;

                """
        start_date = post.get('start_datetime')
        end_date = post.get('end_datetime')
        mac_address = post.get('mac_address')
        request.env.cr.execute(query, (start_date, end_date, mac_address))
        return request.env.cr.dictfetchall()

    # @http.route('/api/get_data_print_day', type='json', auth='none')
    # def get_data_print_day(self, **post):
    #     request.session.db = ConfigDatabase.database
    #     start_datetime_str = post.get('start_datetime')
    #     end_datetime_str = post.get('end_datetime')
    #     records = request.env['mdm.board.iot'].search([
    #         ('mac_address', '=', post.get('mac_address')),
    #         ('date', '>=', datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')),
    #         ('date', '<=', datetime.datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')),
    #         '|', ('date', 'like', '% 09:%'), ('date', 'like', '% 15:%')
    #     ])
    #     data_all = []
    #     temperature_data = []
    #     humidity_data = []
    #     date_data = []
    #
    #     for record in records:
    #         data_all.append({
    #             'temperature': float(record.temperature),
    #             'humidity': float(record.humidity),
    #             'date': record.date.strftime('%Y-%m-%d %H:%M:%S')
    #         })
    #         temperature_data.append(float(record.temperature))
    #         humidity_data.append(float(record.humidity))
    #         date_data.append(record.date.strftime('%Y-%m-%d %H:%M:%S'))
    #     data = {
    #         'status': 200,
    #         'response': data_all,
    #         'temperature': temperature_data,
    #         'humidity': humidity_data,
    #         'date_data': date_data,
    #     }
    #     return data

    @http.route('/api/get_time_data_by_week', type='json', auth='none')
    def get_time_data_by_week(self, **post):
        request.session.db = ConfigDatabase.database
        ICT = timezone('Asia/Bangkok')
        current_datetime = datetime.datetime.now(ICT)
        start_datetime = current_datetime - datetime.timedelta(days=7)
        records = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address')),
            ('date', '>=', start_datetime.strftime('%Y-%m-%d 00:00:00')),
            ('date', '<=', current_datetime.strftime('%Y-%m-%d 23:59:59'))
        ])
        result = {}
        for record in records:
            day = int(record.date.split(' ')[0].split('/')[0])
            month = int(record.date.split(' ')[0].split('/')[1])
            year = int(record.date.split(' ')[0].split('/')[2])

            if (day, month, year) not in result:
                result[(day, month, year)] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['humidity_sum'] += float(record.humidity)
            result[(day, month, year)]['count'] += 1

            result[(day, month, year)]['max_temperature'] = max(result[(day, month, year)]['max_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['min_temperature'] = min(result[(day, month, year)]['min_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['max_humidity'] = max(result[(day, month, year)]['max_humidity'],
                                                             float(record.humidity))
            result[(day, month, year)]['min_humidity'] = min(result[(day, month, year)]['min_humidity'],
                                                             float(record.humidity))

        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        averages = []
        for (day, month, year), values in result.items():
            averages.append({
                'day': str(day).zfill(2),
                'month': str(month).zfill(2),
                'year': year,
                'average_temperature': values['temperature_sum'] / values['count'],
                'average_humidity': values['humidity_sum'] / values['count'],
                'max_temperature': values['max_temperature'],
                'min_temperature': values['min_temperature'],
                'max_humidity': values['max_humidity'],
                'min_humidity': values['min_humidity'],
            })

            temperature_data.append(values['temperature_sum'] / values['count'])
            humidity_data.append(values['humidity_sum'] / values['count'])

            max_humidity_data.append(values['max_temperature'])
            min_humidity_data.append(values['min_temperature'])
            max_temperature_data.append(values['max_humidity'])
            min_temperature_data.append(values['min_humidity'])
            date_data.append(f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}")
        data = {
            'status': 200,
            'response': averages,
            'temperature': temperature_data,
            'humidity_data': humidity_data,
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime,
            'current_datetime': current_datetime
        }
        return data

    @http.route('/api/get_time_data_by_month', type='json', auth='none')
    def get_time_data_by_month(self, **post):
        request.session.db = ConfigDatabase.database
        ICT = timezone('Asia/Bangkok')
        current_datetime = datetime.datetime.now(ICT)
        start_datetime = current_datetime - datetime.timedelta(days=30)
        records = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address')),
            ('date', '>=', start_datetime.strftime('%Y-%m-%d 00:00:00')),
            ('date', '<=', current_datetime.strftime('%Y-%m-%d 23:59:59'))
        ])
        result = {}
        for record in records:
            day = int(record.date.split(' ')[0].split('/')[0])
            month = int(record.date.split(' ')[0].split('/')[1])
            year = int(record.date.split(' ')[0].split('/')[2])

            if (day, month, year) not in result:
                result[(day, month, year)] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['humidity_sum'] += float(record.humidity)
            result[(day, month, year)]['count'] += 1

            result[(day, month, year)]['max_temperature'] = max(result[(day, month, year)]['max_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['min_temperature'] = min(result[(day, month, year)]['min_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['max_humidity'] = max(result[(day, month, year)]['max_humidity'],
                                                             float(record.humidity))
            result[(day, month, year)]['min_humidity'] = min(result[(day, month, year)]['min_humidity'],
                                                             float(record.humidity))

        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        averages = []
        for (day, month, year), values in result.items():
            averages.append({
                'day': str(day).zfill(2),
                'month': str(month).zfill(2),
                'year': year,
                'average_temperature': values['temperature_sum'] / values['count'],
                'average_humidity': values['humidity_sum'] / values['count'],
                'max_temperature': values['max_temperature'],
                'min_temperature': values['min_temperature'],
                'max_humidity': values['max_humidity'],
                'min_humidity': values['min_humidity'],
            })

            temperature_data.append(values['temperature_sum'] / values['count'])
            humidity_data.append(values['humidity_sum'] / values['count'])

            max_humidity_data.append(values['max_temperature'])
            min_humidity_data.append(values['min_temperature'])
            max_temperature_data.append(values['max_humidity'])
            min_temperature_data.append(values['min_humidity'])
            date_data.append(f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}")
        data = {
            'status': 200,
            'response': averages,
            'temperature': temperature_data,
            'humidity_data': humidity_data,
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime,
            'current_datetime': current_datetime
        }
        return data

    @http.route('/api/get_time_data_chart_year', type='json', auth='none')
    def get_time_data_chart_year(self, **post):
        request.session.db = ConfigDatabase.database
        ICT = timezone('Asia/Bangkok')
        current_datetime = datetime.datetime.now(ICT)
        start_datetime = current_datetime - datetime.timedelta(days=365)
        records = request.env['mdm.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address')),
            ('date', '>=', start_datetime.strftime('%Y-%m-%d 00:00:00')),
            ('date', '<=', current_datetime.strftime('%Y-%m-%d 23:59:59'))
        ])
        result = {}
        for record in records:
            day = int(record.date.split(' ')[0].split('/')[0])
            month = int(record.date.split(' ')[0].split('/')[1])
            year = int(record.date.split(' ')[0].split('/')[2])

            if (day, month, year) not in result:
                result[(day, month, year)] = {
                    'temperature_sum': 0,
                    'humidity_sum': 0,
                    'count': 0,
                    'max_temperature': float('-inf'),
                    'min_temperature': float('inf'),
                    'max_humidity': float('-inf'),
                    'min_humidity': float('inf'),
                }
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['temperature_sum'] += float(record.temperature)
            result[(day, month, year)]['humidity_sum'] += float(record.humidity)
            result[(day, month, year)]['count'] += 1

            result[(day, month, year)]['max_temperature'] = max(result[(day, month, year)]['max_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['min_temperature'] = min(result[(day, month, year)]['min_temperature'],
                                                                float(record.temperature))
            result[(day, month, year)]['max_humidity'] = max(result[(day, month, year)]['max_humidity'],
                                                             float(record.humidity))
            result[(day, month, year)]['min_humidity'] = min(result[(day, month, year)]['min_humidity'],
                                                             float(record.humidity))

        temperature_data = []
        humidity_data = []
        date_data = []
        max_humidity_data = []
        min_humidity_data = []
        max_temperature_data = []
        min_temperature_data = []
        averages = []
        for (day, month, year), values in result.items():
            averages.append({
                'day': str(day).zfill(2),
                'month': str(month).zfill(2),
                'year': year,
                'average_temperature': values['temperature_sum'] / values['count'],
                'average_humidity': values['humidity_sum'] / values['count'],
                'max_temperature': values['max_temperature'],
                'min_temperature': values['min_temperature'],
                'max_humidity': values['max_humidity'],
                'min_humidity': values['min_humidity'],
            })

            temperature_data.append(values['temperature_sum'] / values['count'])
            humidity_data.append(values['humidity_sum'] / values['count'])

            max_humidity_data.append(values['max_temperature'])
            min_humidity_data.append(values['min_temperature'])
            max_temperature_data.append(values['max_humidity'])
            min_temperature_data.append(values['min_humidity'])
            date_data.append(f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}")
        data = {
            'status': 200,
            'response': averages,
            'temperature': temperature_data,
            'humidity_data': humidity_data,
            'max_humidity_data': max(max_humidity_data),
            'min_humidity_data': min(min_humidity_data),
            'max_temperature_data': max(max_temperature_data),
            'min_temperature_data': min(min_temperature_data),
            'date_data': date_data,
            'start_datetime': start_datetime,
            'current_datetime': current_datetime
        }
        return data
