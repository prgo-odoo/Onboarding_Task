from odoo import fields, models


class ProductStatus(models.Model):
    _name = 'product.status'
    _description = 'Product Status'

    name = fields.Char(string='Product Status')
    hierarchy = fields.Integer()
    group_change_up_id = fields.Many2one('res.groups', 'Group Name - Status Change Up')
    group_change_down_id = fields.Many2one('res.groups', 'Group Name - Status Change Down')
