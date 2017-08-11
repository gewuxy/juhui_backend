# -*- coding: utf8 -*-
import logging
import json
from apps import get_response_data
from django.http import JsonResponse
_logger = logging.getLogger('Oauth2Middleware')


class Oauth2Middleware(object):

    def process_response(self, request, response):
        # _logger.info('response is {0}'.format(response.content))
        try:
            r = json.loads(response.content.decode('utf8'))
        except Exception:
            return response
        detail = r.get('detail')
        if detail:
            if detail == 'Authentication credentials were not provided.':
                _logger.info('========认证失败========')
                return JsonResponse(get_response_data('000007'))
            elif 'Method' in detail and 'not allowed' in detail:
                _logger.info('========请求方法错误========')
                return JsonResponse(get_response_data('000001'))
            else:
                _logger.info('========认证其它错误========')
                return JsonResponse(get_response_data('000007'))
        else:
            return JsonResponse(r)
