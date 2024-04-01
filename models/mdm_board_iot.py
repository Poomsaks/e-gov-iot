import datetime
from datetime import timedelta, date

import pytz
import requests

from odoo import models, fields, api


class MdmMainBoardIot(models.Model):
    _name = 'main.board.iot'
    _description = 'บอร์ด'
    _rec_name = 'name'

    hospital_id = fields.Many2one(comodel_name='health.promoting.hospital', string='ชื่อ รพสต.',
                                  required=False)
    name = fields.Char(string='ชื่อ รพสต.', related='hospital_id.name')
    image = fields.Char(string='โลโก้', related='hospital_id.image')
    address = fields.Text(string='ที่อยู่', related='hospital_id.flex')
    position = fields.Char(string='ตำแหน่งที่ตั้ง บอร์ด', required=False)
    mac_address = fields.Char(string='Mac Address', required=False)
    token_line_notify = fields.Char(string='Token Line Notify', required=False)
    token_line_oa = fields.Char(string="Token Line OA", required=False, )
    time_count = fields.Integer(string='นับเวลา', requests=False, default=1)
    time_notify = fields.Selection(string="เวลาแจ้งเตือน",
                                   selection=[('1', '10 นาที'),
                                              ('2', '20 นาที'),
                                              ('3', '30 นาที'),
                                              ('4', '40 นาที'),
                                              ('5', '50 นาที'),
                                              ('6', '60 นาที')],
                                   required=False, defaul='2')
    message_send_notify = fields.Char(string='message_send_notify', required=False)
    board_iot_ids = fields.One2many(comodel_name='mdm.board.iot', inverse_name='main_board_iot_id',
                                    string='รายละเอียด', required=False)
    flex_image_url = fields.Char(string="url รูปภาพ", required=False, )
    room_name = fields.Char(string="ห้องที่ติดตั้ง", required=False, )

    calibrate = fields.Char(string="Calibrate", required=False, default='0')
    notify_active = fields.Boolean(string="สถานะ", default=True)

    @api.multi
    def action_active(self):
        for record in self:
            record.notify_active = not record.notify_active

    @api.depends('board_iot_ids')
    def _compute_max_value(self):
        current_datetime = datetime.datetime.now()
        local_tz = pytz.timezone('Asia/Bangkok')
        current_datetime_local = fields.Datetime.context_timestamp(self, current_datetime).astimezone(local_tz)
        formatted_date = current_datetime_local.strftime('%Y-%m-%d')
        query = '''
            SELECT
                MAX(CAST(temperature AS FLOAT)),
                MIN(CAST(temperature AS FLOAT)),
                MAX(CAST(humidity AS FLOAT)),
                MIN(CAST(humidity AS FLOAT)) ,
                AVG(CAST(temperature AS FLOAT)) ,
                AVG(CAST(humidity AS FLOAT))
            FROM mdm_board_iot
            WHERE main_board_iot_id = %s AND date BETWEEN %s AND %s '''
        date_start = formatted_date + ' 00:00:00'
        date_end = formatted_date + ' 23:59:59'
        self._cr.execute(query, (self.id, date_start, date_end))
        view_ref_res = self._cr.fetchone()

        self.max_temperature = view_ref_res[0]
        self.min_temperature = view_ref_res[1]
        self.max_humidity = view_ref_res[2]
        self.min_humidity = view_ref_res[3]
        self.avg_humidity = view_ref_res[4]
        self.avg_temperature = view_ref_res[5]

    max_temperature = fields.Char(string='ค่าอุณหภูมิสูงสุด', compute='_compute_max_value', store=True)
    min_temperature = fields.Char(string='ค่าอุณหภูมิต่ำสุด', compute='_compute_max_value', store=True)
    max_humidity = fields.Char(string='ค่าความชื้นสูงสุด', compute='_compute_max_value', store=True)
    min_humidity = fields.Char(string='ค่าความชื้นต่ำสุด', compute='_compute_max_value', store=True)
    avg_humidity = fields.Char(string='ค่าความชื้นเฉลี่ย', compute='_compute_max_value', store=True)
    avg_temperature = fields.Char(string='ค่าอุณหภูมิเฉลี่ย', compute='_compute_max_value', store=True)

    # @api.depends('board_iot_ids')
    # def _compute_max_value_week(self):
    #     board_id = ""
    #     for record in self:
    #         main_board_iot_ids = [board_iot.main_board_iot_id.id for board_iot in record.board_iot_ids]
    #         if main_board_iot_ids:
    #             board_id = main_board_iot_ids[0]
    #
    #     current_datetime = datetime.datetime.now()
    #     local_tz = pytz.timezone('Asia/Bangkok')
    #     current_datetime_local = fields.Datetime.context_timestamp(self, current_datetime).astimezone(local_tz)
    #     date_end = current_datetime_local.strftime('%Y/%m/%d')
    #     date_start = (current_datetime_local - datetime.timedelta(days=7)).strftime('%Y/%m/%d')
    #     query = '''
    #                 SELECT
    #                     MAX(CAST(temperature AS FLOAT)),
    #                     MIN(CAST(temperature AS FLOAT)),
    #                     MAX(CAST(humidity AS FLOAT)),
    #                     MIN(CAST(humidity AS FLOAT))
    #                 FROM mdm_board_iot
    #                 WHERE id = %s AND TO_TIMESTAMP(formatted_date, 'DD/MM/YYYY') BETWEEN %s AND %s
    #             '''
    #     self._cr.execute(query, (board_id, date_start, date_end))
    #     view_ref_res = self._cr.fetchone()
    #     self.max_temperature_week = view_ref_res[0]
    #     self.min_temperature_week = view_ref_res[1]
    #     self.max_humidity_week = view_ref_res[2]
    #     self.min_humidity_week = view_ref_res[3]
    #
    # max_temperature_week = fields.Char(string='ค่าอุณหภูมิสูงสุด week', compute='_compute_max_value_week', store=True)
    # min_temperature_week = fields.Char(string='ค่าอุณหภูมิต่ำสุด week', compute='_compute_max_value_week', store=True)
    # max_humidity_week = fields.Char(string='ค่าความชื้นสูงสุด week', compute='_compute_max_value_week', store=True)
    # min_humidity_week = fields.Char(string='ค่าความชื้นต่ำสุด week', compute='_compute_max_value_week', store=True)
    #
    # @api.depends('board_iot_ids')
    # def _compute_max_value_month(self):
    #     board_id = ""
    #     for record in self:
    #         main_board_iot_ids = [board_iot.main_board_iot_id.id for board_iot in record.board_iot_ids]
    #         if main_board_iot_ids:
    #             board_id = main_board_iot_ids[0]
    #     current_datetime = datetime.datetime.now()
    #     local_tz = pytz.timezone('Asia/Bangkok')
    #     current_datetime_local = fields.Datetime.context_timestamp(self, current_datetime).astimezone(local_tz)
    #     date_end = current_datetime_local.strftime('%Y/%m/%d')
    #     date_start = (current_datetime_local - datetime.timedelta(days=30)).strftime('%Y/%m/%d')
    #     query = '''
    #         SELECT
    #             MAX(CAST(temperature AS FLOAT)),
    #             MIN(CAST(temperature AS FLOAT)),
    #             MAX(CAST(humidity AS FLOAT)),
    #             MIN(CAST(humidity AS FLOAT))
    #         FROM mdm_board_iot
    #         WHERE id = %s AND TO_TIMESTAMP(formatted_date, 'DD/MM/YYYY') BETWEEN %s AND %s
    #     '''
    #     self._cr.execute(query, (board_id, date_start, date_end))
    #     view_ref_res = self._cr.fetchone()
    #     self.max_temperature_month = view_ref_res[0]
    #     self.min_temperature_month = view_ref_res[1]
    #     self.max_humidity_month = view_ref_res[2]
    #     self.min_humidity_month = view_ref_res[3]
    #
    # max_temperature_month = fields.Char(string='ค่าอุณหภูมิสูงสุด month', compute='_compute_max_value_month',
    #                                     store=True)
    # min_temperature_month = fields.Char(string='ค่าอุณหภูมิต่ำสุด month', compute='_compute_max_value_month',
    #                                     store=True)
    # max_humidity_month = fields.Char(string='ค่าความชื้นสูงสุด month', compute='_compute_max_value_month', store=True)
    # min_humidity_month = fields.Char(string='ค่าความชื้นต่ำสุด month', compute='_compute_max_value_month', store=True)
    #
    # @api.depends('board_iot_ids')
    # def _compute_max_value_year(self):
    #     board_id = ""
    #     for record in self:
    #         main_board_iot_ids = [board_iot.main_board_iot_id.id for board_iot in record.board_iot_ids]
    #         if main_board_iot_ids:
    #             board_id = main_board_iot_ids[0]
    #     current_datetime = datetime.datetime.now()
    #     local_tz = pytz.timezone('Asia/Bangkok')
    #     current_datetime_local = fields.Datetime.context_timestamp(self, current_datetime).astimezone(local_tz)
    #     date_end = current_datetime_local.strftime('%Y/%m/%d')
    #     date_start = current_datetime_local.replace(year=current_datetime_local.year - 1).strftime('%Y/%m/%d')
    #     query = '''
    #                 SELECT
    #                     MAX(CAST(temperature AS FLOAT)),
    #                     MIN(CAST(temperature AS FLOAT)),
    #                     MAX(CAST(humidity AS FLOAT)),
    #                     MIN(CAST(humidity AS FLOAT))
    #                 FROM mdm_board_iot
    #                 WHERE id = %s AND TO_TIMESTAMP(formatted_date, 'DD/MM/YYYY') BETWEEN %s AND %s
    #             '''
    #     self._cr.execute(query, (board_id, date_start, date_end))
    #     view_ref_res = self._cr.fetchone()
    #     self.max_temperature_year = view_ref_res[0]
    #     self.min_temperature_year = view_ref_res[1]
    #     self.max_humidity_year = view_ref_res[2]
    #     self.min_humidity_year = view_ref_res[3]
    #
    # max_temperature_year = fields.Char(string='ค่าอุณหภูมิสูงสุด year', compute='_compute_max_value_year', store=True)
    # min_temperature_year = fields.Char(string='ค่าอุณหภูมิต่ำสุด year', compute='_compute_max_value_year', store=True)
    # max_humidity_year = fields.Char(string='ค่าความชื้นสูงสุด year', compute='_compute_max_value_year', store=True)
    # min_humidity_year = fields.Char(string='ค่าความชื้นต่ำสุด year', compute='_compute_max_value_year', store=True)

    # records = YourModel.search([
    #     ('formatted_date', '>=', '2023-01-01 00:00:00'),
    #     ('formatted_date', '<=', '2024-01-21 00:00:00'),
    # ])
    #
    # if records:
    #     result['max_temperature'] = max(record.temperature for record in records)
    #     result['min_temperature'] = min(record.temperature for record in records)
    #     result['max_humidity'] = max(record.humidity for record in records)
    #     result['min_humidity'] = min(record.humidity for record in records)
    # @api.depends('board_iot_ids')
    # def _compute_min_value(self):
    #     local_tz = pytz.timezone('Asia/Bangkok')
    #     for record in self:
    #         formatted_date = datetime.datetime.today()
    #         formatted_date = fields.Datetime.from_string(formatted_date).replace(tzinfo=pytz.utc).astimezone(local_tz)
    #         formatted_date = formatted_date.strftime('%Y-%m-%d')
    #         print(formatted_date)
    #         current_records_today = record.board_iot_ids.filtered(
    #             lambda r: r.date == formatted_date
    #         )
    #
    #         # record.min_temperature = max(current_records_today.mapped('temperature'), default=None)
    #         print(current_records_today)
    # min_temperature = fields.Char(string='ค่าต่ำสุด', compute='_compute_min_value', store=True)


class MDMBoardIOT(models.Model):
    _name = 'mdm.board.iot'
    _description = 'บอร์ด'
    _rec_name = 'mac_address'

    main_board_iot_id = fields.Many2one(comodel_name='main.board.iot', string='รหัส Max address', required=False)
    mac_address = fields.Char(string='Mac Address', required=False)
    temperature = fields.Char(string='อุณหภูมิ', required=False)
    humidity = fields.Char(string='ความชื้น', required=False)
    light = fields.Char(string='แสง', required=False)
    ip_connect = fields.Char(string='เลข ip wifi', required=False)
    date = fields.Datetime(string="วันที่", required=False)
    status = fields.Boolean(string='สถานะ', required=False, default=True)

    # @api.depends('date')
    # def _compute_formatted_date(self):
    #     for record in self:
    #         if record.date:
    #             local_tz = pytz.timezone('Asia/Bangkok')
    #             formatted_date = fields.Datetime.to_string(record.date)
    #             formatted_date = fields.Datetime.from_string(formatted_date).replace(tzinfo=pytz.utc).astimezone(
    #                 local_tz)
    #             formatted_date = formatted_date - timedelta(hours=7)
    #             record.formatted_date = formatted_date.strftime('%d/%m/%Y %H:%M:%S')
    #
    # formatted_date = fields.Char(string='วันที่', compute='_compute_formatted_date', store=True)
