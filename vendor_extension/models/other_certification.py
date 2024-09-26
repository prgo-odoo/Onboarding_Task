from odoo import fields, models


class OtherCertification(models.Model):
    _name = 'other.certification'
    _description = 'Other Certification'

    name = fields.Char(string="Name")
