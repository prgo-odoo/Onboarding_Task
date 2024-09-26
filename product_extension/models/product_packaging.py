from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    width = fields.Integer(string='Case Width (mm)', required=True)
    length = fields.Integer(string='Case Length (mm)', required=True)
    height = fields.Integer(string='Case Height (mm)', required=True)
    volume = fields.Integer(string='Case Volume (m³)', compute='_compute_volume')
    net_weight = fields.Float(string='Case Nett Weight', required=True)
    gross_weight = fields.Float(string='Case Gross Weight', required=True)

    @api.depends('width', 'length', 'height')
    def _compute_volume(self):
        for packaging in self:
            packaging.volume = (packaging.width * packaging.length * packaging.height) / 1e9
