from odoo import api, models, _
from odoo.exceptions import ValidationError

def odoo_app_api(method):
    method._odoo_app = True
    return method


class OdooApp(models.AbstractModel):
    _name = 'odoo.app'

    @api.model
    def _check_request(self, token, data):
        pass

    def _get_user_domain(self, token):
        return [
            ('app_login', '=', token)
        ]

    @api.model
    def _get_user(self, token):
        return self.env.user.sudo().env.user
        user = self.env['res.users'].search(self._get_user_domain(token), limit=1)
        if not user:
            raise ValidationError(_('User was not found'))
        return 

    @api.model
    def execute(self, method, data):
        if not hasattr(self, method):
            raise ValidationError(_('Method is not defined'))
        attribute = getattr(self, method)
        if callable(attribute) and hasattr(attribute, '_odoo_app'):
            return attribute(data)
        raise ValidationError(_('Method attribute %s was not found') % method)
