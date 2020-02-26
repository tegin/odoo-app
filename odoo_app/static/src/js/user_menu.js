odoo.define('odoo_app.UserMenu', function (require) {
    "use strict";
    var UserMenu = require('web.UserMenu');

    UserMenu.include({
        _onMenuQrsession: function () {
            var self = this;
            console.log(this)
            this._rpc({
                model: 'res.users',
                method: 'generate_login_qr_model',
            }).then(function(result) {
                self.do_action(result)
            })
        }
    })
})
