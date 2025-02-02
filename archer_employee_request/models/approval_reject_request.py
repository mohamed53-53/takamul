from odoo import models, fields


# class ApprovalRejectWizard(models.TransientModel):
#     _inherit = 'approval.reject.wizard'
#
#     def action_reject(self):
#         model = self._context.get('active_model')
#         record_id = self._context.get('active_id')
#         record = self.env[model].browse(record_id)
#         if record._context.get("residency_issuance"):
#             record.write({
#                 'state': 'rejected',
#                 'number': '',
#                 'serial_number': '',
#                 're_job_title': '',
#                 'place_of_issuance': '',
#                 'issuance_date': '',
#                 'expiration_date': '',
#                 'expiration_date_in_hijri': '',
#                 'arrival_date': '',
#                 'rejection_reason': self.reason,
#             })
#
#         assert record._isinstance('approval.record')
#         return record.action_reject(self.reason)