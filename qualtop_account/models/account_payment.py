# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _l10n_mx_edi_sign(self):
        acc_move = self.env['account.move'].search([('name', '=', self.communication),('state','!=', 'cancel')])
        if acc_move.not_sign_complement:
            self.message_post(
                body=_('Este complemento no se timbrará')
            )
            return True
        return super(AccountPayment, self)._l10n_mx_edi_sign()

    def l10n_mx_edi_is_required(self):
        self.ensure_one()
        acc_move = self.env['account.move'].search([('name', '=', self.communication), ('state', '!=', 'cancel')])
        if len(acc_move) > 1:
            raise UserError('Lo siento, hay dos facturas con el Folio : {}  , favor de contactar con el administrador'.format(self.communication))

        if acc_move.not_sign_complement or acc_move.not_sign:
            return True
        return super(AccountPayment, self).l10n_mx_edi_is_required()
