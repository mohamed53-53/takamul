# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import api, fields, models, _


class AccountMoveline(models.Model):
    _inherit = "account.move.line"

    tds_tag = fields.Boolean("TDS Tag", default=False)
    tax_id = fields.Many2one('account.tax', string='Tax', )


class AccountMove(models.Model):
    _inherit = "account.move"

    tax_based_on = fields.Selection([('untaxed', 'Untaxed'), ('total', 'Total')], string='Tax Based On',
                                    default='total')

    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state', 'tds_tax_ids')
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for move in self:
            if move.tds:
                move.total_gross = move.amount_untaxed + move.amount_tax
                total_tds_tax_amount = 0.0
                for tax in move.tds_tax_ids:
                    applicable = True
                    if move.partner_id and move.partner_id.tds_threshold_check and tax:
                        applicable = move.check_turnover(move.partner_id.id, tax.payment_excess,
                                                         move.total_gross)
                    if not applicable or not tax.tds:
                        continue
                    if move.tax_based_on == 'total':
                        taxes = tax._origin.compute_all(
                            move.total_gross)
                        total_tds_tax_amount += taxes['total_included'] - taxes[
                            'total_excluded'] if taxes else move.total_gross * (tax.amount / 100)
                    elif move.tax_based_on == 'untaxed':
                        taxes = tax._origin.compute_all(
                            move.amount_untaxed)
                        total_tds_tax_amount += taxes['total_included'] - taxes[
                            'total_excluded'] if taxes else move.amount_untaxed * (tax.amount / 100)
                move.tds_amt = -total_tds_tax_amount
                if move.tax_based_on == 'total':
                    move.amount_total = move.amount_untaxed + move.amount_tax + move.tds_amt

                elif move.tax_based_on == 'untaxed':
                    move.total_gross = move.amount_untaxed + move.tds_amt
                    move.amount_total = move.amount_untaxed + move.tds_amt + move.amount_tax
                move.amount_total_signed = move.total_gross + move.tds_amt

            else:
                move.total_gross = move.amount_untaxed + move.amount_tax
                move.tds_amt = 0.0
                move.amount_total = move.amount_untaxed + move.amount_tax + move.tds_amt

                move.tds_tax_ids = False

    tds = fields.Boolean('Apply TDS', default=False,
                         states={'draft': [('readonly', False)]})
    tds_tax_ids = fields.Many2many('account.tax', string='TDS',
                                   states={'draft': [('readonly', False)]})
    tds_amt = fields.Monetary(string='TDS Amount',
                              readonly=True, compute='_compute_amount')
    total_gross = fields.Monetary(string='Total',
                                  store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Monetary(string='Net Total',
                                   store=True, readonly=True, compute='_compute_amount')
    vendor_type = fields.Selection(related='partner_id.company_type', string='Partner Type')
    display_in_report = fields.Boolean('Display TDS in Report', default=False)

    @api.onchange('tds', 'partner_id')
    def _onchange_tds(self):
        # print(self)
        if self.tds:
            for rec in self:
                # print(rec.partner_id.company_type)
                return {'domain': {
                    'tds_tax_ids': [('tds_applicable', '=', rec.partner_id.company_type)]}}

    def check_turnover(self, partner_id, threshold, total_gross):
        domain = [('partner_id', '=', partner_id), ('account_id.internal_type', '=', 'payable'),
                  ('move_id.state', '=', 'posted'), ('account_id.reconcile', '=', True)]
        journal_items = self.env['account.move.line'].search(domain)
        credits = sum([item.credit for item in journal_items])
        credits += total_gross
        if credits >= threshold:
            return True
        else:
            return False

    @api.onchange('tax_based_on')
    def onchange_tax_based_on(self):

        if self.tds:
            self._compute_amount()
            self.tds_tax_ids = False
            self._onchange_tds_tax_id()

    @api.onchange('tds')
    def onchange_tds(self):
        for invoice in self:
            if self.tds == False:
                invoice.tax_based_on = 'total'
                invoice.tds_tax_ids = False
                invoice._onchange_tds_tax_id()

    @api.onchange('tds_tax_ids')
    def _onchange_tds_tax_id(self):
        for invoice in self:
            if not invoice.tds_tax_ids:
                existing_lines = invoice.line_ids.filtered(lambda x: x.tds_tag)
                existing_lines.credit = 0
                existing_lines.debit = 0
                invoice.line_ids -= existing_lines
                invoice._onchange_recompute_dynamic_lines()
            tax_ids = []
            tds_list = []
            for tax in invoice.tds_tax_ids:
                if tax.amount_type == 'group':
                    for child in tax.children_tax_ids:
                        tds_list.append(child.name)
                else:
                    tds_list.append(tax.name)
            for tax in invoice.tds_tax_ids:
                applicable = True
                if invoice.partner_id and invoice.partner_id.tds_threshold_check:
                    applicable = invoice.check_turnover(invoice.partner_id.id, tax.payment_excess,
                                                        invoice.total_gross)
                tax_repartition_lines = tax.invoice_repartition_line_ids.filtered(
                    lambda x: x.repartition_type == 'tax') if tax else None
                tds_amount = abs(invoice.tds_amt) if tax and applicable else 0
                tds_tax = tax if tax else None
                if invoice.tax_based_on == 'total':
                    taxes = tax._origin.compute_all(
                        invoice.total_gross)
                elif invoice.tax_based_on == 'untaxed':
                    taxes = tax._origin.compute_all(
                        invoice.amount_untaxed)
                tds_tax_amount = taxes['total_included'] - taxes[
                    'total_excluded'] if taxes else 0
                converted_tds_tax_amount = invoice.currency_id._convert(tds_tax_amount,
                                                                     invoice.company_id.currency_id,
                                                                     invoice.company_id, invoice.date)
                tag_ids = []
                for tax_rec in taxes.get('taxes'):
                    if tax._origin.id == tax_rec.get('id'):
                        tag_ids = (tax_rec.get('tax_tag_ids'))
                credit = 0
                debit = 0
                if invoice.move_type in ['in_invoice', 'out_refund', 'in_receipt']:
                    credit = converted_tds_tax_amount
                elif invoice.move_type in ['out_invoice', 'in_refund', 'out_receipt']:
                    debit = converted_tds_tax_amount
                existing_lines = self.env['account.move.line']
                if tax.amount_type == 'group':
                    for child in tax.children_tax_ids:
                        tax_ids.append(child.name)
                        existing_lines = invoice.line_ids.filtered(lambda x: x.tds_tag and x.name == child.name)
                else:
                    tax_ids.append(tax.name)
                    existing_lines = invoice.line_ids.filtered(lambda x: x.tds_tag and x.name == tax.name)
                for ex_line in invoice.line_ids.filtered(lambda x: x.tds_tag):
                    if ex_line.name not in tds_list:
                        invoice.line_ids -= ex_line
                if applicable and tds_tax_amount and tds_tax and tax_repartition_lines and not existing_lines:
                    create_method = invoice.env['account.move.line'].new
                    if tds_tax.amount_type == 'group':
                        for child in tds_tax.children_tax_ids:
                            tax_repartition_lines = child.invoice_repartition_line_ids.filtered(
                                lambda x: x.repartition_type == 'tax') if child else None
                            tds_amount = child.amount * (invoice.total_gross / 100)
                            taxes = child._origin.compute_all(
                                invoice.total_gross)
                            for tax_rec in taxes.get('taxes'):
                                if child._origin.id == tax_rec.get('id'):
                                    tag_ids = tax_rec.get('tax_tag_ids')
                            tds_tax_amount = taxes['total_included'] - taxes[
                                'total_excluded'] if taxes else 0
                            converted_tds_tax_amount = invoice.currency_id._convert(tds_tax_amount,
                                                                                 invoice.company_id.currency_id,
                                                                                 invoice.company_id, invoice.date)
                            if invoice.move_type in ['in_invoice', 'out_refund', 'in_receipt']:
                                credit = converted_tds_tax_amount
                            elif invoice.move_type in ['out_invoice', 'in_refund', 'out_receipt']:
                                debit = converted_tds_tax_amount
                            if invoice.move_type in ['in_invoice', 'out_refund', 'in_receipt']:
                                create_method({
                                    'name': child.name,
                                    'debit': debit,
                                    'credit': credit,
                                    'quantity': 1.0,
                                    'amount_currency': -tds_tax_amount,
                                    'date_maturity': invoice.invoice_date,
                                    'move_id': invoice.id,
                                    'currency_id': invoice.currency_id.id if invoice.currency_id != invoice.company_id.currency_id else False,
                                    'account_id': tax_repartition_lines.account_id.id if tax_repartition_lines else None,
                                    'partner_id': invoice.commercial_partner_id.id,
                                    'tds_tag': True,
                                    'tax_id': tax.id,
                                    'tax_ids': [(6, 0, tax.ids)],
                                    'tax_tag_ids': [(6, 0, tag_ids)],
                                    'exclude_from_invoice_tab': True,
                                })
                            elif invoice.move_type in ['out_invoice', 'in_refund', 'out_receipt']:
                                create_method({
                                    'name': child.name,
                                    'debit': debit,
                                    'credit': credit,
                                    'quantity': 1.0,
                                    'amount_currency': tds_tax_amount,
                                    'date_maturity': invoice.invoice_date,
                                    'move_id': invoice.id,
                                    'currency_id': invoice.currency_id.id if invoice.currency_id != invoice.company_id.currency_id else False,
                                    'account_id': tax_repartition_lines.account_id.id if tax_repartition_lines else None,
                                    'partner_id': invoice.commercial_partner_id.id,
                                    'tds_tag': True,
                                    'tax_id': tax.id,
                                    'tax_ids': [(6, 0, tax.ids)],
                                    'tax_tag_ids': [(6, 0, tag_ids)],
                                    'exclude_from_invoice_tab': True,
                                })
                    else:

                        if invoice.move_type in ['in_invoice', 'out_refund', 'in_receipt']:
                            create_method({
                                'name': tax.name,
                                'debit': debit,
                                'credit': credit,
                                'quantity': 1.0,
                                'amount_currency': -tds_tax_amount,
                                'date_maturity': invoice.invoice_date,
                                'move_id': invoice.id,
                                'currency_id': invoice.currency_id.id if invoice.currency_id != invoice.company_id.currency_id else False,
                                'account_id': tax_repartition_lines.account_id.id if tax_repartition_lines else None,
                                'partner_id': invoice.commercial_partner_id.id,
                                'tax_ids': [(6, 0, tax.ids)],
                                'tds_tag': True,
                                'tax_id': tax.id,
                                'exclude_from_invoice_tab': True,
                            })
                        elif invoice.move_type in ['out_invoice', 'in_refund', 'out_receipt']:
                            create_method({
                                'name': tax.name,
                                'debit': debit,
                                'credit': credit,
                                'quantity': 1.0,
                                'amount_currency': tds_tax_amount,
                                'date_maturity': invoice.invoice_date,
                                'move_id': invoice.id,
                                'currency_id': invoice.currency_id.id if invoice.currency_id != invoice.company_id.currency_id else False,
                                'account_id': tax_repartition_lines.account_id.id if tax_repartition_lines else None,
                                'partner_id': invoice.commercial_partner_id.id,
                                'tax_ids': [(6, 0, tax.ids)],
                                'tds_tag': True,
                                'tax_id': tax.id,
                                'exclude_from_invoice_tab': True,
                            })
                invoice._onchange_recompute_dynamic_lines()

    def _recompute_tax_lines(self, recompute_tax_base_amount=False, tax_rep_lines_to_recompute=None):
        ''' Compute the dynamic tax lines of the journal entry.

        :param lines_map: The line_ids dispatched by type containing:
            * base_lines: The lines having a tax_ids set.
            * tax_lines: The lines having a tax_line_id set.
            * terms_lines: The lines generated by the payment terms of the invoice.
            * rounding_lines: The cash rounding lines of the invoice.
        '''
        self.ensure_one()
        in_draft_mode = self != self._origin

        def _serialize_tax_grouping_key(grouping_dict):
            ''' Serialize the dictionary values to be used in the taxes_map.
            :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
            :return: A string representing the values.
            '''
            return '-'.join(str(v) for v in grouping_dict.values())

        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                is_refund = move.move_type in ('out_refund', 'in_refund')
                if move.tax_based_on == 'total':
                    price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
                elif move.tax_based_on == 'untaxed':
                    price_unit_wo_discount = sign * move.total_gross
                else:
                    price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
            else:
                handle_price_include = False
                quantity = 1.0
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
                price_unit_wo_discount = base_line.amount_currency

            return base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_wo_discount,
                currency=base_line.currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
                include_caba_tags=move.always_tax_exigible,
            )

        taxes_map = {}

        to_remove = self.env['account.move.line']
        for line in self.line_ids.filtered('tax_repartition_line_id'):
            grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
            grouping_key = _serialize_tax_grouping_key(grouping_dict)
            if grouping_key in taxes_map:
                to_remove += line
            else:
                taxes_map[grouping_key] = {
                    'tax_line': line,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                }
        if not recompute_tax_base_amount:
            self.line_ids -= to_remove

        for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
            if not line.tax_ids:
                if not recompute_tax_base_amount:
                    line.tax_tag_ids = [(5, 0, 0)]
                continue

            compute_all_vals = _compute_base_line_taxes(line)

            if not recompute_tax_base_amount:
                line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

            for tax_vals in compute_all_vals['taxes']:
                grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
                grouping_key = _serialize_tax_grouping_key(grouping_dict)

                tax_repartition_line = self.env['account.tax.repartition.line'].browse(
                    tax_vals['tax_repartition_line_id'])
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

                taxes_map_entry = taxes_map.setdefault(grouping_key, {
                    'tax_line': None,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                })
                taxes_map_entry['amount'] += tax_vals['amount']
                taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'],
                                                                                       tax_repartition_line,
                                                                                       tax_vals['group'])
                taxes_map_entry['grouping_dict'] = grouping_dict

        taxes_map = self._preprocess_taxes_map(taxes_map)

        for taxes_map_entry in taxes_map.values():
            if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
                if not recompute_tax_base_amount:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

            if currency.is_zero(taxes_map_entry['amount']):
                if taxes_map_entry['tax_line'] and not recompute_tax_base_amount:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id,
                                                self.company_id, self.date or fields.Date.context_today(self))

            if recompute_tax_base_amount:
                if taxes_map_entry['tax_line']:
                    taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
                continue

            balance = currency._convert(
                taxes_map_entry['amount'],
                self.company_currency_id,
                self.company_id,
                self.date or fields.Date.context_today(self),
            )
            to_write_on_line = {
                'amount_currency': taxes_map_entry['amount'],
                'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
                'tax_base_amount': tax_base_amount,
            }

            if taxes_map_entry['tax_line']:
                taxes_map_entry['tax_line'].update(to_write_on_line)
            else:
                create_method = in_draft_mode and self.env['account.move.line'].new or self.env[
                    'account.move.line'].create
                tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
                taxes_map_entry['tax_line'] = create_method({
                    **to_write_on_line,
                    'name': tax.name,
                    'move_id': self.id,
                    'partner_id': line.partner_id.id,
                    'company_id': line.company_id.id,
                    'company_currency_id': line.company_currency_id.id,
                    'tax_base_amount': tax_base_amount,
                    'exclude_from_invoice_tab': True,
                    **taxes_map_entry['grouping_dict'],
                })

            if in_draft_mode:
                taxes_map_entry['tax_line'].update(
                    taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        res = super(AccountMove, self)._onchange_invoice_line_ids()
        self._onchange_tds_tax_id()
        return res


class AccountInvoiceTax(models.Model):
    _inherit = "account.tax"

    tds = fields.Boolean('TDS', default=False)
