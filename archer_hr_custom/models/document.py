from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrDocumentDocument(models.Model):
    _name = 'hr.document.document'

    name = fields.Char(name='Document')
    description = fields.Text(string='Description')
    is_required = fields.Boolean(string='Required')
    in_portal = fields.Boolean(string='Show In Portal')
    job_id = fields.Many2one(comodel_name='hr.job', string='For Job')
    country_id = fields.Many2one(comodel_name='res.country', string='Nationality')
    used_for = fields.Selection(selection=[('both', _('Employee & Contract')), ('employee', _('Employee')), ('contract', _('Contract'))],
                                default='both')
    document_type = fields.Selection(
        selection=[
            ('civil', _('Civil ID')),
            ('passport', _('Passport')),
            ('birth', _('Birth Certificate')),
            ('national_address', _('National Address')),
            ('education', _('Education')),
            ('gosi', _('GOSI')),
            ('residency', _('Residency')),
            ('experience', _('Experience')),
            ('father_birth', _('Father Birth Certificate')),
            ('mother_birth', _('Mother Birth Certificate')),
            ('spouse_birth', _('Spouse Birth Certificate')),
            ('child_birth', _('Child Birth Certificate')),
            ('other', _('Other)'))
        ])


class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.document'

    document_id = fields.Many2one(comodel_name='hr.document.document', string='Document Name', required=True)
    doc_type = fields.Selection(related='document_id.document_type')
    is_required = fields.Boolean(related='document_id.is_required', readonly=False)
    in_portal = fields.Boolean(related='document_id.in_portal', readonly=False)
    job_id = fields.Many2one(comodel_name='hr.job',related='document_id.job_id')
    country_id = fields.Many2one(comodel_name='res.country', related='document_id.country_id')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    contract_id = fields.Many2one(comodel_name='hr.contract', string='Contract')
    attach = fields.Binary(string='Attach', attachment=True)
    state = fields.Selection(selection=[('new', _('New')), ('return', _('Return')), ('approve', _('Approve'))])
    used_for = fields.Selection(selection=[('both', _('Employee & Contract')), ('employee', _('Employee')), ('contract', _('Contract'))],
                                related='document_id.used_for', string='Used For')
    def unlink(self):
        if self.attach or self.state != 'new':
            raise ValidationError('You Can\'t delete document have attachment or status in ["Return", "Approve"]')
        else:
            return super(HrEmployeeDocument, self).unlink()

    def approve_document(self):
        for rec in self:
            rec.state = 'approve'
    def reject_document(self):
        for rec in self:
            rec.state = 'return'