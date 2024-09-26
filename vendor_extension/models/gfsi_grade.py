from odoo import fields, models


class GfsiGrade(models.Model):
    _name = 'gfsi.grade'
    _description = 'GFSI Grade'

    name = fields.Char(string="Name")
