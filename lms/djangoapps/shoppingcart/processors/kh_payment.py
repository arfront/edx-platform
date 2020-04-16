# -*- coding:utf-8 -*-
import binascii
import hmac
import datetime
import uuid
from hashlib import sha256
from collections import OrderedDict, defaultdict
from edxmako.shortcuts import render_to_string
from shoppingcart.processors.helpers import get_processor_config
from ..models import Order




def render_purchase_form_html(cart, callback_url=None, extra_data=None):
    """
    Renders the HTML of the hidden POST form that must be used to initiate a purchase with CyberSource

    Args:
        cart (Order): The order model representing items in the user's cart.

    Keyword Args:
        callback_url (unicode): The URL that CyberSource should POST to when the user
            completes a purchase.  If not provided, then CyberSource will use
            the URL provided by the administrator of the account
            (CyberSource config, not LMS config).

        extra_data (list): Additional data to include as merchant-defined data fields.

    Returns:
        unicode: The rendered HTML form.

    """
    return render_to_string('shoppingcart/kh_form.html', {
        'action': get_purchase_endpoint(),
        'params': get_signed_purchase_params(
            cart, callback_url=callback_url, extra_data=extra_data
        ),
    })


def get_purchase_endpoint():
    """
    Return the URL of the payment end-point for CyberSource.

    Returns:
        unicode

    """
    return get_processor_config().get('PURCHASE_ENDPOINT', '')


def get_purchase_params(cart, callback_url=None, extra_data=None):
    """
    This method will build out a dictionary of parameters needed by CyberSource to complete the transaction

    Args:
        cart (Order): The order model representing items in the user's cart.

    Keyword Args:
        callback_url (unicode): The URL that CyberSource should POST to when the user
            completes a purchase.  If not provided, then CyberSource will use
            the URL provided by the administrator of the account
            (CyberSource config, not LMS config).

        extra_data (list): Additional data to include as merchant-defined data fields.

    Returns:
        dict

    """
    total_cost = cart.total_cost
    amount = "{0:0.2f}".format(total_cost)
    params = OrderedDict()

    params['amount'] = amount
    params['currency'] = cart.currency
    params['orderNumber'] = "OrderId: {0:d}".format(cart.id)
    params['reference_number'] = cart.id
    params['transaction_type'] = 'sale'

    params['transaction_uuid'] = uuid.uuid4().hex
    params['payment_method'] = 'card'

    return params


def get_signed_purchase_params(cart, callback_url=None, extra_data=None):
    return get_purchase_params(cart, callback_url, extra_data)


def process_postpay_callback(params):
    order = Order.objects.filter(out_trade_no=params['out_trade_no']).get()
    return {
        'success': True,
        'order': order,
        'error_html': ''
    }
