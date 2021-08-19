odoo.define('pos_customer_uso_cfdi.get_customer', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields("res.partner", ['l10n_mx_edi_usage']);

    var obj 
    self.usos_cfdi = [
        {code:'G01', description: 'G01 - Adquisición de mercancias'},
        {code:'G02', description: 'G02 - Devoluciones, descuentos o bonificaciones'},
        {code:'G03', description: 'G03 - Gastos en genera'},
        {code:'I01', description: 'I01 - Construcciones'},
        {code:'I02', description: 'I02 - Mobilario y equipo de oficina por inversiones'},
        {code:'I03', description: 'I03 - Equipo de transporte'},
        {code:'I04', description: 'I04 - Equipo de computo y accesorios'},
        {code:'I05', description: 'I05 - Dados, troqueles, moldes, matrices y herramienta'},
        {code:'I06', description: 'I06 - Comunicaciones telefónicas'},
        {code:'I07', description: 'I07 - Comunicaciones satelitales'},
        {code:'I08', description: 'I08 - Otra maquinaria y equipo'},
        {code:'D01', description: 'D01 - Honorarios médicos, dentales y gastos hospitalarios.'},
        {code:'D02', description: 'D02 - Gastos médicos por incapacidad o discapacidad'},
        {code:'D03', description: 'D03 - Gastos funerales'},
        {code:'D04', description: 'D04 - Donativos'},
        {code:'D05', description: 'D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'},
        {code:'D06', description: 'D06 - Aportaciones voluntarias al SAR'},
        {code:'D07', description: 'D07 - Primas por seguros de gastos médicos'},
        {code:'D08', description: 'D08 - Gastos de transportación escolar obligatoria'},
        {code:'D09', description: 'D09 - Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'},
        {code:'D10', description: 'D10 - Pagos por servicios educativos (colegiaturas)'},
        {code:'P01', description: 'P01 - Por definir'},
    ];


    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_uso_cfdi: function(uso_code){
            console.log("# get_uso_cfdi >>> ");
            console.log("# uso_code >>> ",uso_code);
            /*if(!uso_code){
                console.log("### No tiene Codigo >>> ");
                return 'N/A';
            } */
            var usos_cfdi = {
                    'G01': 'G01 - Adquisición de mercancias',
                    'G02': 'G02 - Devoluciones, descuentos o bonificaciones',
                    'G03': 'G03 - Gastos en genera',
                    'I01': 'I01 - Construcciones',
                    'I02': 'I02 - Mobilario y equipo de oficina por inversiones',
                    'I03': 'I03 - Equipo de transporte',
                    'I04': 'I04 - Equipo de computo y accesorios',
                    'I05': 'I05 - Dados, troqueles, moldes, matrices y herramienta',
                    'I06': 'I06 - Comunicaciones telefónicas',
                    'I07': 'I07 - Comunicaciones satelitales',
                    'I08': 'I08 - Otra maquinaria y equipo',
                    'D01': 'D01 - Honorarios médicos, dentales y gastos hospitalarios.',
                    'D02': 'D02 - Gastos médicos por incapacidad o discapacidad',
                    'D03': 'D03 - Gastos funerales',
                    'D04': 'D04 - Donativos',
                    'D05': 'D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)',
                    'D06': 'D06 - Aportaciones voluntarias al SAR',
                    'D07': 'D07 - Primas por seguros de gastos médicos',
                    'D08': 'D08 - Gastos de transportación escolar obligatoria',
                    'D09': 'D09 - Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.',
                    'D10': 'D10 - Pagos por servicios educativos (colegiaturas)',
                    'P01': 'P01 - Por definir',
                };
            return usos_cfdi[uso_code];
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this, arguments);
            if (this.pos.config.default_partner_id) {
            	this.set_client(this.pos.db.get_partner_by_id(this.pos.config.default_partner_id[0]));
            }
        },
        
    });
});