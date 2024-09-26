from odoo import fields, models


class VendorStatus(models.Model):
    _name = "vendor.status"
    _description = "Vendor Status"

    name = fields.Char(string="Vendor Status")
    hierarchy = fields.Integer()
    status_change_ids = fields.Many2many('res.users', string="Status Change")
    prevent_po = fields.Selection(string="Prevent PO", selection=[('yes', 'Yes'), ('no', 'No'), ('alert', 'Alert')])
    notify_user_id = fields.Many2one('res.users', string="Notify User")
