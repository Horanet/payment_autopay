# coding: utf8

from odoo import http
from odoo.http import request
from odoo.addons.payment.models.payment_acquirer import ValidationError

import pprint
import logging
import werkzeug
import urlparse

_logger = logging.getLogger(__name__)


class AutoPayController(http.Controller):

    @http.route('/payment/autopay', type='http', auth="none", methods=['POST', 'GET'], csrf=False)
    def autopay_payment(self, **post):
        """Process AutoPay DPN."""
        _logger.debug('Beginning AutoPay DPN form_feedback with post data %s', pprint.pformat(post))
        self.autopay_validate_data(**post)
        tx = request.env['payment.transaction']._autopay_form_get_tx_from_data(post)
        return werkzeug.utils.redirect('%s' % tx.acquirer_id.autopay_get_confirmation_url())

    def autopay_validate_data(self, **post):
        """Check data returned from AutoPay."""
        if not post or not post.get('reference', False):
            raise ValidationError("No reference found for transaction on AutoPay")

        values = {
            'reference': post.get('reference', False),
        }

        return request.env['payment.transaction'].form_feedback(values, 'autopay')
