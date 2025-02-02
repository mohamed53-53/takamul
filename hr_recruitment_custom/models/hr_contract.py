from odoo import api, fields, models


class HRContract(models.Model):
    _inherit = 'hr.contract'

    def _get_application_annual_basic(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            return emp.application_id.annual_basic_salary

    def _get_application_teaching_certificate(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            if emp.application_id:
                teaching_rule = emp.application_id.salary_breakdown_ids.filtered(
                    lambda x: 'Teaching Certifi' in x.salary_breakdown_id.name)
                return teaching_rule[0].subtotal

    def _get_application_master_degree(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            if emp.application_id:
                master_rule = emp.application_id.salary_breakdown_ids.filtered(
                    lambda x: 'Master' in x.salary_breakdown_id.name)
                if master_rule:
                    return master_rule[0].subtotal

    def _get_application_phd_degree(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            if emp.application_id:
                phd_rule = emp.application_id.salary_breakdown_ids.filtered(
                    lambda x: 'PhD' in x.salary_breakdown_id.name)
                if phd_rule:
                    return phd_rule[0].subtotal

    def _get_application_first_five_year_experience(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            if emp.application_id:
                first_five_rule = emp.application_id.salary_breakdown_ids.filtered(
                    lambda x: 'First Five' in x.salary_breakdown_id.name)
                if first_five_rule:
                    return first_five_rule[0].subtotal

    def _get_application_second_five_year_experience(self):
        active_id = self._context.get('active_id')
        if active_id:
            emp = self.env['hr.employee'].browse(active_id)
            if emp.application_id:
                second_five_rule = emp.application_id.salary_breakdown_ids.filtered(
                    lambda x: 'Years 6-10' in x.salary_breakdown_id.name)
                if second_five_rule:
                    return second_five_rule[0].subtotal

    annual_basic_currency = fields.Many2one('res.currency', string="Annual Basic Currency",
                                            default=lambda self: self.env.company.currency_id)
    annual_basic = fields.Monetary(string="Annual Basic Salary", default=_get_application_annual_basic,
                                   currency_field='annual_basic_currency')
    teaching_certificate_currency = fields.Many2one('res.currency', string="Teaching Certificate Currency",
                                                    default=lambda self: self.env.company.currency_id)
    teaching_certificate = fields.Monetary(string="Teaching Certificate", default=_get_application_teaching_certificate,
                                           currency_field='teaching_certificate_currency')
    master_degree_currency = fields.Many2one('res.currency', string="Master Degree Currency",
                                             default=lambda self: self.env.company.currency_id)
    master_degree = fields.Monetary(string="Master Degree", default=_get_application_master_degree,
                                    currency_field='master_degree_currency')
    phd_degree_currency = fields.Many2one('res.currency', string="PhD Degree Currency",
                                          default=lambda self: self.env.company.currency_id)

    phd_degree = fields.Monetary(string="PhD Degree", default=_get_application_phd_degree,
                                 currency_field='phd_degree_currency')
    first_five_year_experience_currency = fields.Many2one('res.currency',
                                                          string="First Five Years Teaching Experience Currency",
                                                          default=lambda self: self.env.company.currency_id)

    first_five_year_experience = fields.Monetary(string="First Five Years Teaching Experience",
                                                 defaul=_get_application_first_five_year_experience,
                                                 currency_field='first_five_year_experience_currency')
    second_five_year_experience_currency = fields.Many2one('res.currency',
                                                           string="Years 6-10 of Teaching Experience Currency",
                                                           default=lambda self: self.env.company.currency_id)

    second_five_year_experience = fields.Monetary(string="Years 6-10 of Teaching Experience",
                                                  default=_get_application_second_five_year_experience,
                                                  currency_field='second_five_year_experience_currency')
    #############################################################################################
    annual_basic_today_currency = fields.Monetary(string="", compute="get_today_currency")
    teaching_certificate_today_currency = fields.Monetary(string="", compute="get_today_currency")
    master_degree_today_currency = fields.Monetary(string="", compute="get_today_currency")
    phd_degree_today_currency = fields.Monetary(string="", compute="get_today_currency")
    first_five_year_experience_currency_today_currency = fields.Monetary(string="", compute="get_today_currency")
    second_five_year_today_currency = fields.Monetary(string="", compute="get_today_currency")

    @api.onchange('annual_basic_currency', 'annual_basic', 'teaching_certificate_currency', 'teaching_certificate',
                  'master_degree_currency', 'master_degree', 'phd_degree_currency', 'phd_degree',
                  'first_five_year_experience_currency', 'first_five_year_experience',
                  'second_five_year_experience_currency', 'second_five_year_experience'
                  )
    def get_today_currency(self):
        for rec in self:
            rec.annual_basic_today_currency = rec.annual_basic_currency._convert(rec.annual_basic,
                                                                                 rec.company_id.currency_id,
                                                                                 rec.company_id, fields.Date.today())
            rec.teaching_certificate_today_currency = rec.teaching_certificate_currency._convert(
                rec.teaching_certificate, rec.company_id.currency_id, rec.company_id, fields.Date.today())
            rec.master_degree_today_currency = rec.master_degree_currency._convert(rec.master_degree,
                                                                                   rec.company_id.currency_id,
                                                                                   rec.company_id, fields.Date.today())
            rec.phd_degree_today_currency = rec.phd_degree_currency._convert(rec.phd_degree, rec.company_id.currency_id,
                                                                             rec.company_id, fields.Date.today())
            rec.first_five_year_experience_currency_today_currency = rec.first_five_year_experience_currency._convert(
                rec.first_five_year_experience, rec.company_id.currency_id, rec.company_id, fields.Date.today())
            rec.second_five_year_today_currency = rec.second_five_year_experience_currency._convert(
                rec.second_five_year_experience, rec.company_id.currency_id, rec.company_id, fields.Date.today())

    Monthly_Salary = fields.Monetary(string="Monthly Salary", )
    Net_Due = fields.Monetary(string="Net Due", )
    Tuition_Fee = fields.Monetary(string="Tuition Fee", )
    Monthly_Retirement = fields.Monetary(string="Monthly Retirement", )
    Health_Insurance = fields.Monetary(string="Health Insurance", )
    Rent = fields.Monetary(string="Rent", )
