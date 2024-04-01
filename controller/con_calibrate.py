from odoo import http
from odoo.http import request
from .config_database import ConfigDatabase


class ConChartData(http.Controller):

    @http.route('/api/get_calibrate', type='json', auth='none')
    def get_calibrate(self, **post):
        request.session.db = ConfigDatabase.database
        hospital_info = request.env['main.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address'))])
        if hospital_info:
            data_s = []
            for rec in hospital_info:
                vals = {
                    'id': rec.id,
                    'calibrate': rec.calibrate or "",
                }
                data_s.append(vals)
            data = {'status': 200, 'response': data_s, 'message': 'success'}
            return data
        else:
            data = {'status': 500, 'response': 'ไม่พบข้อมูล', 'message': 'error'}
            return data

    @http.route('/api/get_calibrate_2', type='json', auth='none')
    def get_calibrate_2(self, **post):
        request.session.db = ConfigDatabase.database
        hospital_info = request.env['main.board.iot'].sudo().search([
            ('mac_address', '=', post.get('mac_address'))])
        if hospital_info:
            vals = ""
            for rec in hospital_info:
                vals = rec.calibrate or "",
            data = vals
            return data
        else:
            data = 'ไม่พบข้อมูล'
            return data
