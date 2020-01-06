from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class AutoPayAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('autopay', 'AutoPay')])

    @api.model
    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(AutoPayAcquirer, self)._get_feature_support()
        return res

    @api.multi
    def autopay_get_form_action_url(self):
        return '/payment/autopay'

    @api.multi
    def autopay_form_generate_values(self, values):
        self.ensure_one()

        autopay_tx_values = dict((k, v) for k, v in list(values.items()) if v)

        return autopay_tx_values
