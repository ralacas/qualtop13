
# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to odoo, Open Source Management Solution
#
#    Copyright (c) 2015 http://www.argil.mx/
#    All Rights Reserved.
#    info skype: german_442 email: (german.ponce@argil.mx)
############################################################################
#    Coded by: german_442 email: (german.ponce@argil.mx)
##############################################################################

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)

#### Etiquetas Analiticas ####


class AccountAnalyticTag(models.Model):
    _name = 'account.analytic.tag'
    _inherit ='account.analytic.tag'

    segmentation_tag = fields.Boolean('Segmentación',  
                                      help='Indica que esta etiqueta generara información Analitica dentro de las Facturas.', )

    segmentation_control_ids = fields.One2many('account.analytic.tag.segmentation.control', 'tag_id',
                                               'Lineas Segmentación', copy=False)

    # account_analytic_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica')

    #factura id
    #etiqueta id

class AccountMove(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    segmentation_control_ids = fields.One2many('account.analytic.tag.segmentation.control', 'invoice_id',
                                               'Lineas Segmentación')

    segmentation_control = fields.Boolean('Factura con Segmentación',  
                                      help='Indica que esta etiqueta generara información Analitica dentro de las Facturas.', )
    
    tag_ids = fields.Many2many('account.analytic.tag', 'analytic_tag_invoice_rel', 'move_id', 'tag_id',
                               'Etiquetas Analíticas')

    segmentation_reedit = fields.Boolean('Modificación Segmentación')

class AccountAnalyticTagSegmentationControl(models.Model):
    _name = 'account.analytic.tag.segmentation.control'
    _description = 'Control de Segmentacion de Facturas'
    _rec_name = 'invoice_id' 


    @api.depends('invoice_id')
    def _get_subtotal_from_currency(self):
        company = self.env.user.company_id
        company_currency = company.currency_id
        for rec in self:
            invoice_currency = rec.invoice_id.currency_id
            if invoice_currency.id == company_currency.id:
                rec.subtotal = rec.invoice_id.amount_untaxed
            else:
                total_comp_curr = invoice_currency._convert(rec.invoice_id.amount_untaxed, company_currency, company, rec.invoice_id.invoice_date)
                rec.subtotal = total_comp_curr
                # ctx = dict(self._context, date=rec.invoice_id.invoice_date)
                # compute_currency = company_currency.with_context(ctx).compute(rec.invoice_id.amount_untaxed, invoice_currency)
                # rec.subtotal = compute_currency
    


    tag_id = fields.Many2one('account.analytic.tag', 'Etiqueta Analítica')
    invoice_id = fields.Many2one('account.move', 'Factura')

    account_analytic_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica')

    partner_id = fields.Many2one('res.partner', 'Cliente', related="invoice_id.partner_id", store=True)
    company_id = fields.Many2one('res.company', 'Compañia', related="invoice_id.company_id", store=True)

    invoice_date =  fields.Date('Fecha de Factura', related="invoice_id.invoice_date", store=True)
    currency_id = fields.Many2one('res.currency', 'Moneda', related="invoice_id.currency_id", store=True)
    percentage = fields.Float('Porcentaje', digits=(14,6))
    amount = fields.Float('Monto', digits=(14,2))
    # total = fields.Monetary('Total', related="invoice_id.amount_untaxed", store=True)
    total = fields.Monetary('Total', compute="_get_subtotal_from_currency", store=True)

    last_write_date = fields.Datetime('Ultima modificación', default=fields.Datetime.now())
    last_write_user = fields.Many2one('res.users', 'Modificado por', default=lambda self: self.env.user)


class AccountAnalyticTagSegmentationWizard(models.TransientModel):
    _name = 'account.analytic.tag.segmentation.wizard'
    _description = 'Asistente Segmentación de Etiquetas'


    @api.model  
    def default_get(self, fields):
        res = super(AccountAnalyticTagSegmentationWizard, self.with_context(no_update=True)).default_get(fields)
        record_ids = self._context.get('active_ids', [])
        invoice_obj = self.env['account.move']
        if not record_ids:
            return {}
        
        for invoice_br in invoice_obj.browse(record_ids):
            if invoice_br.state != 'posted':
                raise UserError("El asistente solo se puede ejecutar en Facturas Publicadas.")
            tag_ids = []
            res.update({
                        'invoice_id': invoice_br.id,
                        #'subtotal': invoice_br.amount_untaxed,
                        'currency_id': invoice_br.currency_id.id,
                        })
            account_analytic_id = False
            if invoice_br.segmentation_control_ids:
                segmentation_line_ids = []
                for prev_seg in invoice_br.segmentation_control_ids:
                    if prev_seg.account_analytic_id:
                        account_analytic_id = prev_seg.account_analytic_id.id
                    # xline = (0,0,{
                    #         'tag_id': prev_seg.tag_id.id,
                    #         'percentage': prev_seg.percentage,
                    #         'amount': prev_seg.amount,
                    #     })
                    
                    # segmentation_line_ids.append(xline)
                    tag_ids.append(prev_seg.tag_id.id)

                res.update({
                        'tag_ids': [(6, 0, tag_ids)],
                        # 'segmentation_line_ids': segmentation_line_ids,
                        'segmentation_reedit': True,
                        'account_analytic_id': account_analytic_id,
                        })
            # else:
            #     for line in invoice_br.invoice_line_ids:
            #         if line.analytic_tag_ids:
            #             for an_tag in line.analytic_tag_ids:
            #                 if an_tag.segmentation_tag:
            #                     tag_ids.append(an_tag.id)
            #     if tag_ids:
            #         segmentation_line_ids = []
            #         for tag in tag_ids:
            #             xline = (0,0,{
            #                     'tag_id': tag.id,
            #                 })
            #             segmentation_line_ids.append(xline)
            #         res.with_context(no_update=True).update({
            #                 'tag_ids': [(6, 0, tag_ids)],
            #                 'segmentation_line_ids': segmentation_line_ids,
            #                 })
        return res

    @api.depends('invoice_id')
    def _get_subtotal_from_currency(self):
        _logger.info("\n::::::::::::: _get_subtotal_from_currency >>>>>>>>> ")
        company = self.env.user.company_id
        company_currency = company.currency_id
        invoice_currency = self.invoice_id.currency_id
        _logger.info("\n######### company_currency >>>>>>>>> %s" % company_currency)
        _logger.info("\n######### invoice_currency >>>>>>>>> %s" % invoice_currency)
        if invoice_currency.id == company_currency.id:
            self.subtotal = self.invoice_id.amount_untaxed
        else:
            total_comp_curr = invoice_currency._convert(self.invoice_id.amount_untaxed, company_currency, company, self.invoice_id.invoice_date)
            _logger.info("\n######### total_comp_curr >>>>>>>>> %s" % total_comp_curr)
            # ctx = dict(self._context, date=self.invoice_id.invoice_date)
            # compute_currency = company_currency.with_context(ctx).compute(self.invoice_id.amount_untaxed, invoice_currency)
            self.subtotal = total_comp_curr

    @api.depends('segmentation_line_ids')
    def _get_total_percentage(self):
        for rec in self:
            percentage_sum = 0.0
            for line in rec.segmentation_line_ids:
                percentage_sum += line.percentage
            rec.percentage_sum = percentage_sum
    

    invoice_id = fields.Many2one('account.move', 'Factura')
    segmentation_line_ids = fields.One2many('account.analytic.tag.segmentation.wizard.line', 'wizard_id',
                                               'Distribución')

    # segmentation_line_result_ids = fields.One2many('account.analytic.tag.segmentation.wizard.line.res', 'wizard_id',
                                               # 'Ingresos')

    tag_ids = fields.Many2many('account.analytic.tag', 'analytic_tag_wizard_rel', 'wizard_id', 'tag_id',
                               'Etiquetas Analíticas')

    #subtotal = fields.Monetary('Subtotal', related="invoice_id.amount_untaxed", store=True)
    subtotal = fields.Monetary('Subtotal', compute="_get_subtotal_from_currency", store=True)

    percentage_sum = fields.Monetary('Porcentaje', compute="_get_total_percentage", digits=(14,2))

    currency_id = fields.Many2one('res.currency', 'Moneda', related="invoice_id.currency_id", store=True)

    segmentation_reedit = fields.Boolean('Modificación Segmentación')

    account_analytic_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica')


    # @api.onchange('account_analytic_id')
    # def onchange_account_analytic_id(self):
    #     if self.account_analytic_id:
    #         for xprv in self.segmentation_line_ids:
    #             xprv.update(self.account_analytic_id.id)

    @api.onchange('tag_ids')
    def onchange_tag_ids(self):
        context = dict(self._context)
        if 'no_update' in context and context['no_update']:
            return {}
        if self.tag_ids:
            invoice_br = self.invoice_id
            segmentation_line_ids = []
            if invoice_br.segmentation_control_ids:
                new_tag_ids = [x._origin.id for x in self.tag_ids]
                invoice_tag_ids = []
                for prev_seg in invoice_br.segmentation_control_ids:
                    xline = (0,0,{
                            'tag_id': prev_seg.tag_id.id,
                            # 'account_analytic_id': self.account_analytic_id.id if self.account_analytic_id else False,
                            'percentage': prev_seg.percentage,
                            'amount': prev_seg.amount,
                        })
                    segmentation_line_ids.append(xline)
                    invoice_tag_ids.append(prev_seg.tag_id.id)
                for new_tag in new_tag_ids:
                    if new_tag not in invoice_tag_ids:
                        xline = (0,0,{
                            'tag_id': new_tag,
                            # 'account_analytic_id': self.account_analytic_id.id if self.account_analytic_id else False,
                        })
                        segmentation_line_ids.append(xline)
                        # invoice_tag_ids.append(prev_seg.tag_id.id)
                # self.with_context(no_update=True).tag_ids = False
                # self.with_context(no_update=True).tag_ids = [(6, 0, invoice_tag_ids)]
            else:
                segmentation_line_ids = []
                for tag in self.tag_ids:
                    xline = (0,0,{
                                'tag_id': tag._origin.id,
                            })
                    segmentation_line_ids.append(xline)
            self.segmentation_line_ids = False
            self.segmentation_line_ids = segmentation_line_ids
    

    def execute_segmentation(self):
        record_ids = self._context.get('active_ids', [])
        invoice_obj = self.env['account.move']
        tag_ids = [x.id for x in self.tag_ids]
        # 'last_write_date': fields.Datetime.now(),
        # 'last_write_user': self.env.user.id,
        segmentation_control_obj = self.env['account.analytic.tag.segmentation.control']
        invoice_br = self.invoice_id
        invoice_subtotal = self.subtotal
        if invoice_br.segmentation_control_ids:
            invoice_br.segmentation_control_ids.unlink()
        amount_sum = 0.0
        amount_percentage = 0.0
        for line in self.segmentation_line_ids:
            amount_sum += line.amount
            amount_percentage += line.percentage
        if amount_percentage > 100.01:
            raise UserError("El Porcentaje asignado supera el 100%")
        if amount_percentage < 99.99:
            raise UserError("El Porcentaje asignado debe ser del 100%")
        _logger.info("\n######### amount_sum >>>>>>>>> %s" % amount_sum)
        _logger.info("\n######### invoice_subtotal >>>>>>>>> %s" % invoice_subtotal)
        #### Ajuste para moneda USD #####
        invoice_subtotal = invoice_subtotal+0.1
        if amount_sum > invoice_subtotal:
            raise UserError("El monto asignado supera el Subtotal de la Factura %s" % invoice_subtotal)
        for line in self.segmentation_line_ids:
            xvals = {
                'invoice_id': self.invoice_id.id,
                'tag_id': line.tag_id.id,
                'percentage': line.percentage,
                'amount': line.amount,
                'last_write_date': fields.Datetime.now(),
                'last_write_user': self.env.user.id,
                'account_analytic_id': self.account_analytic_id.id if self.account_analytic_id else False,
            }
            segmentation_record  = segmentation_control_obj.create(xvals)
        invoice_obj.browse(record_ids).write({
            'segmentation_control': True,
            'tag_ids': [(6, 0, tag_ids)],
            })
        return True


class AccountAnalyticTagSegmentationWizardLine(models.TransientModel):
    _name = 'account.analytic.tag.segmentation.wizard.line'
    _description = 'Segmentación de Etiquetas Lineas'
    _order = 'tag_id' 

    wizard_id = fields.Many2one('account.analytic.tag.segmentation.wizard', 'ID Ref')

    tag_id = fields.Many2one('account.analytic.tag', 'Etiqueta Analítica')

    percentage = fields.Float('Porcentaje', digits=(14,6))

    currency_id = fields.Many2one('res.currency', 'Moneda', related="wizard_id.currency_id", store=True)

    amount = fields.Monetary('Monto', digits=(14,2))

    # account_analytic_id = fields.Many2one('account.analytic.account', 'Cuenta Analítica')


    @api.onchange('percentage')
    def onchange_percentage(self):
        context = dict(self._context)
        if 'no_update' in context and context['no_update']:
            return {}
        if self.percentage:
            if self.percentage > 100.0:
                raise UserError("El limite es 100%")
            invoice_subtotal = self.wizard_id.subtotal
            tag_id = self.tag_id.id
            amount = invoice_subtotal * (self.percentage/100.0)
            self.with_context(no_update=True).amount = amount

    @api.onchange('amount')
    def onchange_amount(self):
        context = dict(self._context)
        if 'no_update' in context and context['no_update']:
            return {}
        if self.amount:
            invoice_subtotal = self.wizard_id.subtotal
            if self.amount > invoice_subtotal:
                raise UserError("El monto maximo es %s" % invoice_subtotal)
            tag_id = self.tag_id.id
            percentage = (float(self.amount)/invoice_subtotal)*100.0
            self.with_context(no_update=True).percentage = percentage

