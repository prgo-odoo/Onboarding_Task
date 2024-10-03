from odoo import models, fields, api


class ProductPalletSpecification(models.Model):
    _name = 'product.palletspec'
    _description = 'Product Pallet Specification'
    _order = 'sequence'

    name = fields.Char('Pallet Type', required=True)
    sequence = fields.Integer()
    cases_per_layer = fields.Float('Cases per Layer')
    layers_per_pallet = fields.Float('Layers per Pallet')
    qty = fields.Float('Pallet Quantity', compute='_compute_qty')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True)
    length = fields.Float('Pallet Length (m)')
    width = fields.Float('Pallet Width (m)')
    height = fields.Float('Pallet Height (m)')
    weight = fields.Float('Pallet Weight (kg)')
    units = fields.Integer('Pcs per Pallet', compute='_compute_units')
    volume = fields.Float(string='Pallet Volume (m³)', compute='_compute_volume')

    product_tmpl_id = fields.Many2one('product.template', string='Product')

    @api.depends('cases_per_layer', 'layers_per_pallet')
    def _compute_qty(self):
        for record in self:
            record.qty = record.cases_per_layer * record.layers_per_pallet

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):
        for record in self:
            record.volume = record.length * record.width * record.height

    @api.depends('cases_per_layer', 'layers_per_pallet')
    def _compute_units(self):
        for record in self:
            if record.product_tmpl_id:
                pcs_per_pallet = sum(record.product_tmpl_id.packaging_ids.mapped('qty'))
                record.units = (record.cases_per_layer * record.layers_per_pallet) * pcs_per_pallet
            else:
                record.units = 0
