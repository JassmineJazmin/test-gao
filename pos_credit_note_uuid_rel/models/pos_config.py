# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosOrder(models.Model):
    _name = 'pos.order'
    _inherit ='pos.order'

    cfdi_refund_id = fields.Many2one('account.move', 'Nota de Credito')
    cfdi_origin_id = fields.Many2one('account.move', 'Factura Origen')
    is_refund_order = fields.Boolean('Es una devolución')
    uuid_invoice_origin = fields.Char('UUID Origen', size=64)

    def refund(self):
        res = super(PosOrder, self).refund()
        if 'res_id' in res:
            for rec in self:
                invoice_order = rec.account_move
                if invoice_order:
                    refund_id = res['res_id']
                    order_refund_br = self.browse(refund_id)
                    order_refund_br.is_refund_order = True
                    order_refund_br.uuid_invoice_origin = invoice_order.l10n_mx_edi_cfdi_uuid
                    order_refund_br.cfdi_origin_id = invoice_order.id

        return res

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
                'invoice_date': fields.Date.context_today(self),
                'fiscal_position_id': order.fiscal_position_id.id,
                'invoice_line_ids': [(0, None, order._prepare_invoice_line(line)) for line in order.lines],
                'l10n_mx_edi_usage': order.partner_id.l10n_mx_edi_usage,
            }
            if order.amount_total <= 0:
                move_vals.update({
                                    'l10n_mx_edi_origin': '01|'+order.uuid_invoice_origin,
                                })
            new_move = moves.sudo()\
                            .with_context(default_type=move_vals['type'], force_company=order.company_id.id)\
                            .create(move_vals)
            message = _("Esta Factura fue creada desde el punto de venta en la sesión: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
            new_move.message_post(body=message)
            order.write({'account_move': new_move.id, 'state': 'invoiced'})
            if order.amount_total <= 0:
                order.write({
                                    'cfdi_refund_id': new_move.id,
                                })
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
