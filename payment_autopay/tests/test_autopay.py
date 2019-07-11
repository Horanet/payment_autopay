# -*- coding: utf-8 -*-

from lxml import objectify

from odoo.tools import mute_logger

from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment.tests.common import PaymentAcquirerCommon


class AutopayPayment(PaymentAcquirerCommon):

    def setUp(self):
        super(AutopayPayment, self).setUp()
        self.autopay = self.env.ref('payment_autopay.payment_acquirer_autopay')

    def test_10_autopay_form_render(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        # be sure not to do stupid thing
        self.assertEqual(self.autopay.environment, 'test', 'test without test environment')

        # ----------------------------------------
        # Test: button direct rendering + shasign
        # ----------------------------------------

        form_values = {
            'reference': 'test_ref0',
            'return_url': None,
        }

        # render the button
        res = self.autopay.render(
            'test_ref0', 0.01, self.currency_euro.id,
            partner_id=None,
            values=self.buyer_values
        )

        # check form result
        tree = objectify.fromstring(res)
        self.assertEqual(tree.get('action'), '/payment/autopay', 'Autopay: wrong form POST url')
        for form_input in tree.input:
            if form_input.get('name') in ['submit']:
                continue
            self.assertEqual(
                form_input.get('value'),
                form_values[form_input.get('name')],
                'Autopay: wrong value for input %s: received %s instead of %s' % (
                    form_input.get('name'),
                    form_input.get('value'),
                    form_values[form_input.get('name')]
                )
            )

        # ----------------------------------------
        # Test2: button using tx + validation
        # ----------------------------------------

        # create a new draft tx
        tx = self.env['payment.transaction'].create ({
            'amount': 0.01,
            'acquirer_id': self.autopay.id,
            'currency_id': self.currency_euro.id,
            'reference': 'test_ref0',
            'partner_id': self.buyer_id
        })
        # render the button
        res = self.autopay.render(
            'should_be_erased', 0.01, self.currency_euro,
            partner_id=None,
            values=self.buyer_values
        )

        # check form result
        tree = objectify.fromstring(res)
        self.assertEqual(tree.get('action'), '/payment/autopay', 'Autopay: wrong form POST url')
        for form_input in tree.input:
            if form_input.get('name') in ['submit']:
                continue
            self.assertEqual(
                form_input.get('value'),
                form_values[form_input.get('name')],
                'Autopay: wrong value for form input %s: received %s instead of %s' % (
                    form_input.get('name'),
                    form_input.get('value'),
                    form_values[form_input.get('name')]
                )
            )

    @mute_logger('odoo.addons.payment_autopay.models.inherited_payment_acquirer', 'ValidationError')
    def test_20_autopay_form_management(self):
        # be sure not to do stupid thing
        self.assertEqual(self.autopay.environment, 'test', 'test without test environment')

        # typical data posted by autopay after client has successfully paid
        autopay_post_data = {
            'reference': u'test_ref_2',
            'return_url': None,
        }

        # should raise error about unknown tx
        with self.assertRaises(ValidationError):
            self.env['payment.transaction'].form_feedback(autopay_post_data, 'autopay')

        # create tx
        tx = self.env['payment.transaction'].create({
            'amount': 1.95,
            'acquirer_id': self.autopay.id,
            'currency_id': self.currency_euro.id,
            'reference': 'test_ref_2',
            'partner_name': 'Norbert Buyer',
            'partner_country_id': self.country_france.id
        })

        # validate it
        tx.form_feedback(autopay_post_data, 'autopay')
        # check state
        self.assertEqual(tx.state, 'done', 'Autopay: validation did not put tx into done state')
