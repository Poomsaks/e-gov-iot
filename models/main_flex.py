from odoo import models, fields


class MainFlex(models.Model):
    _name = 'main.flex'
    _description = 'เมนูต่างๆ ใน line'
    _rec_name = 'name'

    name = fields.Char(string='ข้อความที่ส่ง', required=False)
    flex = fields.Text(string='Flex', required=False)