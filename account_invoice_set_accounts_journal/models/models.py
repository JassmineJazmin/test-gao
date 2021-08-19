# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit ='account.move'

    @api.onchange('journal_id')
    def _onchange_journal_change_account(self):
        _logger.info("\n########### _onchange_journal_change_account >>>> ")
        if self.journal_id and self.journal_id:
            journal_br = False
            type = self.type
            if self.journal_id:
                journal_br = self.journal_id
            account_selected = False
            if type == 'out_invoice':
                account_selected = journal_br.default_debit_account_id if journal_br.default_debit_account_id else False
                _logger.info("\n:::::::::::: account_selected out_invoice >>>>>>>>>> %s " % account_selected)
            else:
                account_selected = journal_br.default_credit_account_id if journal_br.default_credit_account_id else False
                _logger.info("\n:::::::::::: account_selected out_refund >>>>>>>>>> %s " % account_selected)
            if account_selected:
                for line in self.invoice_line_ids:
                    line.account_id = account_selected.id
            
class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'

    def _get_computed_account(self):
        self.ensure_one()
        if self.move_id and self.move_id.type in ('out_invoice', 'out_refund'):
            journal_br = False
            type = self.move_id.type
            if self.move_id.journal_id:
                journal_br = self.move_id.journal_id
            account_selected = False
            if type == 'out_invoice':
                account_selected = journal_br.default_debit_account_id if journal_br.default_debit_account_id else False
                _logger.info("\n:::::::::::: account_selected out_invoice >>>>>>>>>> %s " % account_selected)
            else:
                account_selected = journal_br.default_credit_account_id if journal_br.default_credit_account_id else False
                _logger.info("\n:::::::::::: account_selected out_refund >>>>>>>>>> %s " % account_selected)
            if not account_selected:
                return super(AccountMoveLine, self)._get_computed_account()
            else:
                return account_selected
        else:
            return super(AccountMoveLine, self)._get_computed_account()


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        moves = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id

        # Create default values.
        default_values_list = []
        for move in moves:
            default_values_list.append({
                'ref': _('Reversal of: %s, %s') % (move.name, self.reason) if self.reason else _('Reversal of: %s') % (move.name),
                'date': self.date or move.date,
                'invoice_date': move.is_invoice(include_receipts=True) and (self.date or move.date) or False,
                'journal_id': self.journal_id and self.journal_id.id or move.journal_id.id,
                'invoice_payment_term_id': None,
                'auto_post': True if self.date > fields.Date.context_today(self) else False,
            })

        # Handle reverse method.
        if self.refund_method == 'cancel':
            if any([vals.get('auto_post', False) for vals in default_values_list]):
                new_moves = moves._reverse_moves(default_values_list)
            else:
                new_moves = moves._reverse_moves(default_values_list, cancel=True)
        elif self.refund_method == 'modify':
            moves._reverse_moves(default_values_list, cancel=True)
            moves_vals_list = []
            for move in moves.with_context(include_business_fields=True):
                moves_vals_list.append(move.copy_data({
                    'invoice_payment_ref': move.name,
                    'date': self.date or move.date,
                })[0])
            new_moves = self.env['account.move'].create(moves_vals_list)
        elif self.refund_method == 'refund':
            new_moves = moves._reverse_moves(default_values_list)
        else:
            return

        if new_moves:
            for invoice in new_moves:
                journal_br = False
                type = invoice.type
                if invoice.journal_id:
                    journal_br = invoice.journal_id
                account_selected = False
                if type == 'out_invoice':
                    account_selected = journal_br.default_debit_account_id if journal_br.default_debit_account_id else False
                    _logger.info("\n:::::::::::: account_selected out_invoice >>>>>>>>>> %s " % account_selected)
                else:
                    account_selected = journal_br.default_credit_account_id if journal_br.default_credit_account_id else False
                    _logger.info("\n:::::::::::: account_selected out_refund >>>>>>>>>> %s " % account_selected)
                for line in invoice.invoice_line_ids:
                    line.account_id = account_selected.id
        # Create action.
        action = {
            'name': _('Movimientos Reversión'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(new_moves) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': new_moves.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', new_moves.ids)],
            })
        return action
