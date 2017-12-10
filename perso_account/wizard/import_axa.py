# -*- coding: utf-8 -*-
'''
    Created on 06 Juillet 2017

    @author: Thibault Francois
'''
import base64
import hashlib
from odoo import models, fields


class ImportAxa(models.TransientModel):

    _inherit = "perso.account.import_fortis"
    _name = "perso.account.import_axa"

    name = fields.Char(default="Import CSV exported from Axa")
    bank = fields.Char()

    _date_format = "%Y-%m-%d"

    _thousand_sep = "."
    _decimal_sep = ","
    _csv_delimiter = ";"
    _csv_quote = '"'
    _header_length = 15
    _encoding = 'iso-8859-1'

    _cash_flow_mapping = {
        0: "reference",
        1: "transaction_date",
        2: "value_date",
        4: 'amount',
        5: 'balance',
        12: 'com1',
        13: 'com2',
        14: "name",
    }

    def _import_rec(self, rec):
        rec['bank_id'] = self.bank
        rec['name'] += '\n%s\n%s' % (rec['com1'], rec['com2'])
        rec['name'] = rec['name'].strip()
        amount = float(rec['amount'].replace(self._thousand_sep, '').replace(self._decimal_sep, '.'))
        ref_str = '%s%s%s' % (amount, rec['transaction_date'], len(rec['name']))
        ref_hash = hashlib.sha1(ref_str.encode('utf-8')).hexdigest()[:4]
        rec['reference'] = '%s-%s' % (rec['reference'], ref_hash)
        del rec['com1']; del rec['com2']; del rec['balance']
        return super(ImportAxa, self)._import_rec(rec)

    def _read_header(self, data):
        print(next(data)) #remove first line
        #second line contains the bank account number
        self.bank = ''.join(next(data)[0].split(' ')[1:])
        super(ImportAxa, self)._read_header(data)
