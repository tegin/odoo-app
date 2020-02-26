# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Odoo App',
    'summary': """
        Access Odoo from an App""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'www.creublanca.es',
    'depends': [
        'report_qr'
    ],
    'data': [
        'views/assets.xml',
        'views/res_users.xml',
        'wizards/res_users_app_login.xml',
    ],
    'qweb': ['static/src/xml/base.xml']
}
