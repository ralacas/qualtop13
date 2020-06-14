# -*- coding: utf-8 -*-

from odoo import models, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _l10n_mx_edi_sign(self):
        acc_move = self.env['account.move'].search([('name', '=', self.communication)])
        if acc_move.not_sign_complement:
            self.message_post(
                body=_('Este complemento no se timbrará')
            )
            return True
        return super(AccountPayment, self)._l10n_mx_edi_sign()