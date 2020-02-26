# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from uuid import uuid4
from datetime import timedelta


class ResUsers(models.Model):

    _inherit = 'res.users'

    app_login = fields.Char()
    app_login_date = fields.Datetime()

    @api.model
    def _request_app_login(self, login):
        data = self.env['res.users.app.login'].search([
            ('qr_data', '=', login),
            ('create_date', '>=', fields.Datetime.to_string(
                fields.Datetime.from_string(fields.Datetime.now())
                + timedelta(minutes=-15)
            ))
        ], limit=1)
        if not data:
            return {}
        user = data.user_id
        user.write({
            'app_login': uuid4(),
            'app_login_date': fields.Datetime.now()
        })
        return {
            'uid': user.id,
            'user': user.display_name,
            'token': user.app_login,
            'token_date': user.app_login_date
        }

    @api.model
    def generate_login_qr_model(self):
        return self.env.user.generate_login_qr()

    def generate_login_qr(self):
        self.ensure_one()
        wizard = self.env['res.users.app.login'].create({
            'user_id': self.id,
            'qr_data': uuid4(),
        })
        action = self.env.ref(
            'odoo_app.res_users_app_login_act_window').read()[0]
        action['res_id'] = wizard.id
        return action
