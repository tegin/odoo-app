# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from io import StringIO
import traceback
from odoo import http
from odoo.fields import Datetime
import logging
_logger = logging.getLogger(__name__)


class CallApp(http.Controller):
    @http.route([
        '/odooapp/login',
        ], type='json', auth="none", methods=['POST', 'OPTIONS'], cors='*')
    def login_app(self, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps({})
        data = request.jsonrequest
        if 'login' not in data or not data['login']:
            return json.dumps({})
        result = request.env['res.users'].sudo()._request_app_login(
            data['login']
        )
        _logger.info(result)
        return json.dumps(result)

    @http.route([
        '/odooapp/execute',
        ], type='json', auth="none", methods=['POST', 'OPTIONS'], cors='*')
    def execute_app(self, *args, **kwargs):
        request = http.request
        if not request.env:
            return json.dumps({})
        try:
            obj = request.env['odoo.app']
            data = request.jsonrequest
            token = data.pop('token')
            method = data.pop('method')
            obj._check_request(token, data)
            user = obj._get_user(token)
            result = obj.sudo(user.id).with_context(
                odoo_app_token=token
            ).execute(method, data)
            return json.dumps(result)
        except Exception:
            buff = StringIO()
            traceback.print_exc(file=buff)
            _logger.error(buff.getvalue())
            return json.dumps({'status': 0})
