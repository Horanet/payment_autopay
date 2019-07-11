# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.http import request
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
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return txs[0]

    @api.multi
    def _autopay_form_validate(self, data):
        _logger.info('Validated AutoPay payment for tx %s: set as done' % self.reference)

        res = {
            'acquirer_reference': uuid.uuid4(),
            'state': 'done',
            'date_validate': fields.Datetime.now()
        }

        request.session.update({
            'sale_order_id': False,
            'sale_transaction_id': False,
            'website_sale_current_pl': False,
        })

        return self.write(res)
