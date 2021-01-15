from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError

import logging
import uuid

_logger = logging.getLogger(__name__)


class AutoPayTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _autopay_form_get_tx_from_data(self, data):
        reference = data.get('reference', False)

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'AutoPay: received data for reference %s' % reference
            if not txs:
                error_msg += '; no transaction found'
            else:
                error_msg += '; multiple transactions found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        tx = txs[0]
        if not tx.acquirer_reference:
            tx.acquirer_reference = uuid.uuid4()

        return tx

    def _autopay_form_validate(self, data):
        _logger.info('Validated AutoPay payment for tx %s: set as done' % self.reference)

        return self.write({
            'state': 'done',
            'date': fields.Datetime.now()
        })
