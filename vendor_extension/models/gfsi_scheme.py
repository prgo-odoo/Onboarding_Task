from odoo import fields, models


class GfsiScheme(models.Model):
    _name = 'gfsi.scheme'
    _description = 'GFSI Scheme'

    name = fields.Char(string="Name")
