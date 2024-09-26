from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_status_id = fields.Many2one('product.status', string='Product Status', required=True)
    customer_ref = fields.Char(string='Customer Reference')
    hs_code = fields.Char(string='HS Code', required=True)

    pallet_spec_ids = fields.One2many('product.palletspec', 'product_tmpl_id', string='Pallet Specification')

    landing_cost = fields.Float(string='Landing Cost', required=True)

    margin = fields.Float(string='Margin', compute='_compute_margin')

    @api.depends('landing_cost', 'list_price', 'standard_price')
    def _compute_margin(self):
        for product in self:
            if product.list_price:
                product.margin = ((product.list_price - (product.standard_price + product.landing_cost)) / product.list_price)
            else:
                product.margin = 0.0

    @api.model
    def write(self, vals):
        if 'product_status_id' in vals:
            new_status = self.env['product.status'].browse(vals['product_status_id'])
            current_status = self.product_status_id

            # archived_status = self.env.ref('product_extension.product_status_archived')
            # pricing_status = self.env.ref('product_extension.product_status_pricing')
            # active_status = self.env.ref('product_extension.product_status_active')

            archived_status = self.product_status_id.search([('name', '=', 'Archived')])
            pricing_status = self.product_status_id.search([('name', '=', 'Pricing')])
            active_status = self.product_status_id.search([('name', '=', 'Active')])
            
            if current_status == archived_status:
                if new_status not in (pricing_status, active_status):
                    raise ValidationError(_('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

            elif new_status.hierarchy <= current_status.hierarchy:
                raise ValidationError(_('Status changes cannot be made to a lower hierarchy'))

            if new_status.group_change_up_id and new_status.group_change_up_id not in self.env.user.groups_id:
                raise AccessError(_('You do not have the access to change the status.'))

        return super(ProductTemplate, self).write(vals)
