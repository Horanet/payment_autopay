# -*- coding: utf-8 -*-
{
    'name': "Intermédiaire de paiement Autopay",
    'version': '10.0.0.0.1',
    'summary': """Intermédiaire de paiement : Implémentation de Autopay""",
    'description': "no warning",
    'author': "Horanet",
    'website': "http://www.horanet.com/",
    'license': "AGPL-3",
    'category': 'Accounting',
    'external_dependencies': {
        'python': []
    },
    'depends': [
        'payment'
    ],
    'qweb': [],
    'init_xml': [],
    'update_xml': [],
    'data': [
       'views/payment_autopay_templates.xml',
       'views/payment_views.xml',

       'data/payment_acquirer.xml',
    ],
    'demo': [
    ],
    'application': False,
    'auto_install': False,
    'installable': True,
}