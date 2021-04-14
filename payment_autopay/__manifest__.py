{
    'name': "Intermédiaire de paiement Autopay",
    'version': '13.0.1.0.0',
    'summary': """Intermédiaire de paiement : Implémentation de Autopay""",
    'author': "Horanet",
    'website': "http://www.horanet.com/",
    'license': "AGPL-3",
    'category': 'Accounting/Payment Acquirers',
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
    'application': True,
    'auto_install': False,
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
