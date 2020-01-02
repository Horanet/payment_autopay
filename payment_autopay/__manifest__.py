{
    'name': "Intermédiaire de paiement Autopay",
    'version': '11.0.1.0.0',
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
