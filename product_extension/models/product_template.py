from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _default_product_status(self):
        return self.env['product.status'].search([('group_change_up_id', '=', self.env.ref("base.group_user").id)])

    product_status_id = fields.Many2one('product.status', string='Product Status', default=_default_product_status)
    customer_ref = fields.Char(string='Customer Reference')
    hs_code = fields.Char(string='HS Code', required=True)

    pallet_spec_ids = fields.One2many('product.palletspec', 'product_tmpl_id', string='Pallet Specification')

    landing_cost = fields.Float(string='Landing Cost')
    margin = fields.Float(string='Margin', compute='_compute_margin')

    is_archived = fields.Boolean(string='Is Archived')
    is_pricing = fields.Boolean(string='Is Pricing')
    is_active = fields.Boolean(string='Is Active')
    is_dormant = fields.Boolean(string='Is Dormant')
    is_npd = fields.Boolean(string='Is NPD')

    @api.depends('landing_cost', 'list_price', 'standard_price')
    def _compute_margin(self):
        for product in self:
            if product.list_price:
                product.margin = ((product.list_price - (product.standard_price + product.landing_cost)) / product.list_price)
            else:
                product.margin = 0.0

    @api.constrains('product_status_id')
    def _check_product_status_id(self):
        new_status = self.product_status_id
        if new_status.group_change_up_id and new_status.group_change_up_id not in self.env.user.groups_id:
            raise AccessError(_('You do not have the required permissions to change the product status.'))

    @api.model
    def write(self, vals):
        if 'product_status_id' in vals:
            new_status = self.env['product.status'].browse(vals['product_status_id'])
            current_status = self.product_status_id

            if self.is_archived is True:
                if 'is_pricing' not in vals and 'is_active' not in vals:
                    raise ValidationError(_('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

                elif 'is_pricing' in vals and vals['is_pricing'] is False:
                    raise ValidationError(_('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

                elif 'is_active' in vals and vals['is_active'] is False:
                    raise ValidationError(_('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

                else:
                    self.is_archived = False
            elif current_status.group_change_down_id not in self.env.user.groups_id:
                if new_status.hierarchy <= current_status.hierarchy:
                    raise ValidationError(_('Status changes cannot be made to a lower hierarchy'))
            else:
                self.is_pricing = False
                self.is_active = False

        return super(ProductTemplate, self).write(vals)
