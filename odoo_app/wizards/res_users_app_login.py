# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import base64


class ResUsersAppLogin(models.TransientModel):

    _name = 'res.users.app.login'

    user_id = fields.Many2one(
        'res.users',
        required=True,
        readonly=True,
    )
    qr_data = fields.Char(
        required=True,
        readonly=True
    )
    qr_image = fields.Char(
        compute='_compute_qr_image'
    )

    @api.depends('qr_data')
    def _compute_qr_image(self):
        obj = self.env['ir.actions.report']
        for record in self:
            record.qr_image = base64.b64encode(
                obj.qr_generate(record.qr_data))

