# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    second_cfdi = fields.Binary(copy=False, string="Cargar CFDI",
                                attachment=True,
                                help="Agregue la factura timbrada desde otro sistema")
    second_cfdi_name = fields.Char(copy=False)

    def _l10n_mx_edi_retry(self):
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