# -*- encoding: utf-8 -*-
##############################################################################
#
#    Part of Odoo.
#    Copyright (C) 2017 Allegro IT (<http://www.allegro.lv/>)
#                       E-mail: <info@allegro.lv>
#                       Address: <Vienibas gatve 109 LV-1058 Riga Latvia>
#                       Phone: +371 67289467
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _
from lxml import etree

class BankingExportPain(models.AbstractModel):
    _inherit = 'banking.export.pain'

    @api.model
    def generate_party_block(
            self, parent_node, party_type, order, name, iban, bic,
            eval_ctx, gen_args):
        res = super(BankingExportPain, self).generate_party_block(parent_node, party_type, order, name, iban, bic, eval_ctx, gen_args)
        addr_vals = []
        country_code = False
        if eval_ctx.get('line', False) and eval_ctx['line'].partner_id:
            p = eval_ctx['line'].partner_id
            addr_vals = [a for a in [p.street, p.street2, p.city, p.state_id and p.state_id.name or False, p.zip] if a]
            country_code = p.country_id and p.country_id.code or False
        if addr_vals or country_code:
            party_node = parent_node.find(party_type)
            if party_node is not None and party_node.find('PstlAdr') is None:
                pos = 1
                if party_node.find('Nm') is None:
                    pos = 0
                party_node.insert(pos, etree.Element('PstlAdr'))
                addr_node = party_node.find('PstlAdr')
                if country_code:
                    cc_node = etree.SubElement(addr_node, 'Ctry')
                    cc_node.text = country_code
                if addr_vals:
                    al_node = etree.SubElement(addr_node, 'AdrLine')
                    al_node.text = ", ".join(addr_vals)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: