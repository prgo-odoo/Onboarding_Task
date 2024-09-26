from odoo import fields, models


class VendorPricelist(models.Model):
    _inherit = "product.supplierinfo"

    qty_per_case = fields.Integer(string="Quantity Per Case")
    cases_per_container = fields.Integer(string="Cases Per Container")
    price_per_1000 = fields.Float(string="Cost Per 1000")
    incoterm_id = fields.Many2one('account.incoterms')
    incoterm = fields.Integer(related="incoterm_id.id", string="Incoterm")
