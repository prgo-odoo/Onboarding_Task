from odoo import api, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.constrains('partner_id')
    def _check_vendor_status(self):
        vendor = self.partner_id
        if vendor.vendor_status_id.prevent_po == 'yes':
            raise ValidationError(_("You cannot create a Purchase Order for this vendor as 'Prevent PO' is set to 'Yes'."))

        if vendor.vendor_status_id and vendor.vendor_status_id.name in ['Verified- Grade 1', 'Verified- Grade 2']:
            vendor.vendor_status_id = self.env.ref('vendor_extension.vendor_status_active').id

        if vendor.vendor_status_id and vendor.vendor_status_id.name == 'Active - On Hold' and vendor.vendor_status_id.prevent_po == 'alert':
            notify_user = vendor.vendor_status_id.notify_user_id
            if notify_user:
                activity_vals = {
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'res_id': self.id,
                    'res_model_id': self.env.ref('vendor_extension.model_purchase_order').id,
                    'note': (
                        f"A Purchase Order has been created for {vendor.name} "
                        f"(Status: 'Active - On Hold') and requires {notify_user.name}'s approval."
                    ),
                    'user_id': notify_user.id,
                }
                self.env['mail.activity'].create(activity_vals)