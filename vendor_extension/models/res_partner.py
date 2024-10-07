from odoo import api, fields, models, _
from odoo.exceptions import AccessError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_vendor_status_id(self):
        all_users = self.env['res.users'].search([('active', '=', True)]).ids
        print(all_users)
        return self.env['vendor.status'].search([('status_change_ids', 'in', all_users)])
    vendor_status_id = fields.Many2one('vendor.status', string="Vendor Status", default=_default_vendor_status_id)

    product_category_ids = fields.Many2many('product.category', string="Product Categories")

    sedex_registered = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Sedex Registered?")

    sedex_no = fields.Char(string="Sedex Number")

    ethical_audit = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Ethical Audit Conducted?")

    gfsi_certification = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="GFSI Certification")

    fsc_certified = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="FSC Certified?")

    pefc_certified = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="PEFC Certified?")

    certification_ids = fields.Many2many('other.certification', string="Certifications")

    gfsi_scheme_id = fields.Many2one('gfsi.scheme', string="GFSI Scheme")

    gfsi_grade_id = fields.Many2one('gfsi.grade', string="GFSI Grade")

    is_verified_grade_1 = fields.Boolean(string='Verified - Grade 1')
    is_verified_grade_2 = fields.Boolean(string='Verified - Grade 2')
    is_on_hold = fields.Boolean(string='Active - On Hold')

    @api.constrains('vendor_status_id')
    def _check_vendor_status(self):
        new_status = self.vendor_status_id
        if new_status.status_change_ids and self.env.user not in new_status.status_change_ids:
            raise AccessError(_('You do not have the required permissions to change the vendor status.'))

    def write(self, vals):
        if 'vendor_status_id' in vals:
            new_status = self.env['vendor.status'].browse(vals['vendor_status_id'])
            current_status = self.vendor_status_id
            if new_status.hierarchy < current_status.hierarchy:
                raise ValidationError(_('You cannot change to a lower status in the hierarchy.'))

        return super(ResPartner, self).write(vals)
