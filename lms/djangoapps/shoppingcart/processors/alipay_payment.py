# -*- coding: utf-8 -*-
import logging
import traceback

from django.conf import settings

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.domain.AlipayTradeCloseModel import AlipayTradeCloseModel

from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.request.AlipayTradeCloseRequest import AlipayTradeCloseRequest

from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
from alipay.aop.api.response.AlipayTradeCloseResponse import AlipayTradeCloseResponse

from arfrontconfig.models import AlipayinfoConfig


logger = logging.getLogger(__name__)


def alipay_config_get():
    config = AlipayinfoConfig.current()
    if config.enabled:
        appid = str(config.appid)
        app_private_key = str(config.app_private_key)
        alipay_public_key = str(config.alipay_public_key)
    else:
        return None
    
    alipay = Alipay(appid, app_private_key, alipay_public_key, sandbox_debug=False)
    return alipay


class Alipay(object):

    def __init__(self, appid, app_private_key, alipay_public_key, sandbox_debug=False):
        self._appid = appid
        self._app_private_key = app_private_key
        self._alipay_public_key = alipay_public_key
        self._sandbox_debug = sandbox_debug
        self._client = self.__init_client()

    def __init_client(self):
        alipay_client_config = AlipayClientConfig(sandbox_debug=self._sandbox_debug)
        alipay_client_config.app_id = self._appid
        alipay_client_config.app_private_key = self._app_private_key
        alipay_client_config.alipay_public_key = self._alipay_public_key
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        return client

    def get_alipay_url(self, out_trade_no, subject, total_amount, body='', product_code='FAST_INSTANT_TRADE_PAY'):
        model = AlipayTradePagePayModel()
        model.out_trade_no = str(out_trade_no)
        model.total_amount = total_amount
        model.subject = subject  # 订单标题
        if body == "":
            body = subject

        model.body = body  # 订单描述
        model.product_code = product_code
        request = AlipayTradePagePayRequest(biz_model=model)
        request.return_url = str(settings.LMS_ROOT_URL) + '/shoppingcart/alipay_callback/'
        request.notify_url = str(settings.LMS_ROOT_URL) + '/shoppingcart/alipay_notify_url_callback/'
        response_url = self._client.page_execute(request, http_method="GET")
        return response_url
    
    def find_pay_result(self, out_trade_no):
        model = AlipayTradeQueryModel()
        model.out_trade_no = str(out_trade_no)
        request = AlipayTradeQueryRequest(biz_model=model)
        
        response_content = None
        try:
            response_content = self._client.execute(request)
        except Exception as e:
            logger.error(traceback.format_exc())
        
        if response_content:
            response = AlipayTradeQueryResponse()
            response.parse_response_content(response_content)
            print(response)
            
            if response.is_success():
                trade_status = response.trade_status
                return trade_status
        
        return None
    
    def cancle_order(self, out_trade_no):
        model = AlipayTradeCloseModel()
        model.out_trade_no = str(out_trade_no)
        request = AlipayTradeCloseRequest(biz_model=model)
        response_content = None
        try:
            response_content = self._client.execute(request)
        except Exception as e:
            logger.error(traceback.format_exc())
            
        if response_content:
            response = AlipayTradeCloseResponse()
            response.parse_response_content(response_content)
            print(response)
            
            if response.is_success():
                code = response.code
                if code == '10000':
                    return True
                
        return None
