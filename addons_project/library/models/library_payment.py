# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models, _


class LibraryPrice(models.Model):
    _name = "library.price"

    name = fields.Char(string='Name')
    duration = fields.Float(string='Duration')
    price = fields.Float(string='Price')
    type = fields.Selection([('time', 'Time'),
                             ('one', 'One')])


class LibraryPayment(models.Model):
    _name = "library.payment"

    date = fields.Date(string='Name', required=True, default=date.today())
    amount = fields.Float(string='Amount')
    customer_id = fields.Many2one('res.partner', string='Customer', store=True, required=True,
                                  domain="[('partner_type', '=', 'customer')]")
