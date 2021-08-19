odoo.define('replace_button_stock_barcode.barcode', function (require){
    "use strict";


    // var client = require('stock_barcode.ClientAction');
    var ClientAction = require('stock_barcode.ClientAction');

    var concurrency = require('web.concurrency');
    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var BarcodeParser = require('barcodes.BarcodeParser');

    var ViewsWidget = require('stock_barcode.ViewsWidget');
    var HeaderWidget = require('stock_barcode.HeaderWidget');
    var LinesWidget = require('stock_barcode.LinesWidget');
    var SettingsWidget = require('stock_barcode.SettingsWidget');
    var utils = require('web.utils');

    var _t = core._t;

    console.log("########## concurrency >>>>>>>>>>>> ", concurrency);
    console.log("########## core >>>>>>>>>>>> ", core);
    console.log("########## ClientAction >>>>>>>>>>>> ", ClientAction);

    var client_action = ClientAction.include({
       _getState: function (recordId, state) {
                var self = this;
                var def;
                if (state) {
                    def = $.Deferred().resolve(state);
                } else {
                    def = this._rpc({
                        'route': '/stock_barcode/get_set_barcode_view_state',
                        'params': {
                            'record_id': recordId,
                            'mode': 'read',
                            'model_name': self.actionParams.model,
                        },
                    });
                }
                return def.then(function (res) {
                    self.currentState = res[0];
                    self.initialState = $.extend(true, {}, res[0]);
                    self.title += self.initialState.name;
                    console.log("### res >>>>>>>>>> ",res);
                    self.groups = {
                        'group_stock_multi_locations': self.currentState.group_stock_multi_locations,
                        'group_tracking_owner': self.currentState.group_tracking_owner,
                        'group_tracking_lot': self.currentState.group_tracking_lot,
                        'group_production_lot': self.currentState.group_production_lot,
                        'group_uom': self.currentState.group_uom,
                        'group_barcode_scanner_sudo': self.currentState.group_barcode_scanner_sudo,
                        'group_barcode_scanner_add_products': self.currentState.group_barcode_scanner_add_products,
                        'group_barcode_scanner_edit_ops': self.currentState.group_barcode_scanner_edit_ops,
                        'group_barcode_scanner_edit_inv': self.currentState.group_barcode_scanner_edit_inv,
                        'group_barcode_scanner_show_qty': self.currentState.group_barcode_scanner_show_qty,
                        'group_barcode_scanner_show_qty_inv': self.currentState.group_barcode_scanner_show_qty_inv,
                    };
                    self.show_entire_packs = self.currentState.show_entire_packs;

                    return res;
                });
            },

    });

core.action_registry.add('stock_barcode_client_action', client_action);

return client_action;

});
	