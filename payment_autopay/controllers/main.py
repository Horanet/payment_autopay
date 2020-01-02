from odoo import http
from odoo.http import request

import pprint
import logging
import werkzeug

_logger = logging.getLogger(__name__)


class AutopayController(http.Controller):

    @http.route('/payment/autopay', type='http', auth="none", methods=['POST', 'GET'], csrf=False)
    def autopay_payment(self, **post):
        """Process AutoPay DPN."""
        _logger.debug('Beginning AutoPay DPN form_feedback with post data %s', pprint.pformat(post))
        request.env['payment.transaction'].sudo().form_feedback(post, 'autopay')
        return werkzeug.utils.redirect(post.pop('return_url', '/'))