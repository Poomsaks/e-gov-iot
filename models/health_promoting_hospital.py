from odoo import models, fields


class HealthPromotingHospital(models.Model):
    _name = 'health.promoting.hospital'
    _description = 'โรงพยาบาลส่งเสริมสุขภาพตําบล'
    _rec_name = 'name'

    name = fields.Char(string='ชื่อโรงพยาบาลส่งเสริมสุขภาพตําบล', required=False)
    flex = fields.Text(string='ที่อยู่', required=False)
    image = fields.Char(string="โลโก้", required=False, )

