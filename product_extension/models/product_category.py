from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    categ_desc = fields.Char(string='Category Description')
