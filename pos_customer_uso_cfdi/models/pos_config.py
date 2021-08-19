# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    default_partner_id = fields.Many2one('res.partner', string="Cliente por Defecto")


class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit ='pos.order'

    def action_pos_order_invoice(self):
        moves = self.env['account.move']

        for order in self:
            # Force company for all SUPERUSER_ID action
            if order.account_move:
                moves += order.account_move
                continue

            if not order.partner_id:
                raise UserError(_('Por favor elige un cliente para la venta.'))

            move_vals = {
                'invoice_payment_ref': order.name,
                'invoice_origin': order.name,
                'journal_id': order.session_id.config_id.invoice_journal_id.id,
                'type': 'out_invoice' if order.amount_total >= 0 else 'out_refund',
                'ref': order.name,
                'partner_id': order.partner_id.id,
                'narration': order.note or '',
                # considering partner's sale pricelist's currency
                'currency_id': order.pricelist_id.currency_id.id,
                'invoice_user_id': order.user_id.id,
                'invoice_date':fields.Date.context_today(self),
                'fiscal_position_id': order.fiscal_position_id.id,
                'invoice_line_ids': [(0, None, order._prepare_invoice_line(line)) for line in order.lines],
                'l10n_mx_edi_usage': order.partner_id.l10n_mx_edi_usage,
                
            }
            new_move = moves.sudo()\
                            .with_context(default_type=move_vals['type'], force_company=order.company_id.id)\
                            .create(move_vals)
            message = _("Esta Factura fue creada desde el punto de venta en la sesión: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
            new_move.message_post(body=message)
            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            moves += new_move

        if not moves:
            return {}

        return {
            'name': _('Factura de Cliente'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': moves and moves.ids[0] or False,
        }


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit ='res.partner'

    l10n_mx_edi_usage = fields.Selection([
        ('G01', 'G01 - Adquisición de mercancias'),
        ('G02', 'G02 - Devoluciones, descuentos o bonificaciones'),
        ('G03', 'G03 - Gastos en genera'),
        ('I01', 'I01 - Construcciones'),
        ('I02', 'I02 - Mobilario y equipo de oficina por inversiones'),
        ('I03', 'I03 - Equipo de transporte'),
        ('I04', 'I04 - Equipo de computo y accesorios'),
        ('I05', 'I05 - Dados, troqueles, moldes, matrices y herramienta'),
        ('I06', 'I06 - Comunicaciones telefónicas'),
        ('I07', 'I07 - Comunicaciones satelitales'),
        ('I08', 'I08 - Otra maquinaria y equipo'),
        ('D01', 'D01 - Honorarios médicos, dentales y gastos hospitalarios.'),
        ('D02', 'D02 - Gastos médicos por incapacidad o discapacidad'),
        ('D03', 'D03 - Gastos funerales'),
        ('D04', 'D04 - Donativos'),
        ('D05', 'D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
        ('D06', 'D06 - Aportaciones voluntarias al SAR'),
        ('D07', 'D07 - Primas por seguros de gastos médicos'),
        ('D08', 'D08 - Gastos de transportación escolar obligatoria'),
        ('D09', 'D09 - Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
        ('D10', 'D10 - Pagos por servicios educativos (colegiaturas)'),
        ('P01', 'P01 - Por definir'),
    ], 'Uso CFDI', default='P01')



class AccountInvoice(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # OVERRIDE
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.partner_id:
        	self.l10n_mx_edi_usage = self.partner_id.l10n_mx_edi_usage

        return res
