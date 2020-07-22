# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    second_cfdi = fields.Binary(copy=False, string="Cargar CFDI",
                                attachment=True,
                                help="Agregue la factura timbrada desde otro sistema")
    second_cfdi_name = fields.Char(copy=False)
    not_sign_complement = fields.Boolean(string='No timbrar complemento', copy=False)
    not_sign = fields.Boolean(string='No timbrar', copy=False)

    def _l10n_mx_edi_sign(self):
        '''Call the sign service with records that can be signed.
        '''
        if self.not_sign:
            return super(AccountMove, self)._l10n_mx_edi_sign()
        res = super(AccountMove, self)._l10n_mx_edi_sign()
        return res

    def l10n_mx_edi_update_sat_status(self):
        if self.not_sign:
            return
        res = super(AccountMove, self).l10n_mx_edi_update_sat_status
        return res

    def button_draft(self):
        if self.not_sign:
            return super(AccountMove, self).button_draft()
        res = super(AccountMove, self).button_draft()
        return res

    def _l10n_mx_edi_retry(self):
        if self.not_sign:
            return True
        result = super(AccountMove, self)._l10n_mx_edi_retry()
        att_obj = self.env['ir.attachment']
        for inv in self.filtered('second_cfdi'):
            inv.message_post(body=_('Este documento no fue generado en odoo'),)
            ctx = self.env.context.copy()
            ctx.pop('default_type', False)
            att_obj.search([
                ('name', '=', inv.l10n_mx_edi_cfdi_name),
                ('res_id', '=', inv.id),
                ('res_model', '=', inv._name)
            ]).unlink()
            att_obj.with_context(ctx).create({
                'name': inv.second_cfdi_name,
                'res_id': inv.id,
                'res_model': inv._name,
                'datas': inv.second_cfdi,
                'description': 'Mexican Invoice'
            })
            inv.l10n_mx_edi_cfdi_name = inv.second_cfdi_name
        return result