# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Saldos iniciales UUID',
    'version': '13.1',
    'description': ''' Saldos iniciales
    ''',
    'category': 'Accounting',
    'author': 'Qualtop',
    'website': 'www.qualtop.com.mx',
    'depends': [
        'account','l10n_mx_edi'
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'application': False,
    'installable': True,
    'license': 'OPL-1',
}
