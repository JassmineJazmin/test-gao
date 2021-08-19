# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit ='res.partner'

    @api.constrains('vat')
    def _constraint_uniq_vat(self):
        for rec in self:
            if rec.is_company and rec.vat:
                if rec.vat.upper() not in ('XAXX010101000','XEXX010101000','MXXEXX010101000','MXXAXX010101000'):
                    #other_partner = self.search([('vat','=',rec.vat),('id','!=',rec.id),('is_company','=',True)])
                    cr = self.env.cr
                    cr.execute("""
                        select id from res_partner where upper(vat) = %s
                                  and id != %s and is_company=True;
                        """, (rec.vat.upper(), rec.id))
                    cr_res = cr.fetchall()
                    if cr_res and cr_res[0] and cr_res[0][0]:
                        raise UserError("Error!\nEl RFC ya existe en la Base de Datos")
                    # if other_partner:
                    #     raise UserError("Error!\nEl RFC ya existe en la Base de Datos")
