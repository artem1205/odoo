# -*- coding: utf-8 -*-

from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = "library.book"

    name = fields.Char('Name')
    author_ids = fields.Many2many('library.partner')
    edition_date = fields.Date('Edition Time')
    isbn = fields.Char('ISBN')
    publisher_id = fields.Many2one('library.publisher')
    rental_ids = fields.One2many('library.rental')


class LibraryRental(models.Model):
    _name = "library.rental"

    customer_id = fields.Many2one('library.partner', store=True, required=True)
    book_id = fields.Many2one('library.book', store=True)
    rental_date = fields.Date('Rental Date', store=True, required=True)
    return_date = fields.Date('Return Date', store=True, required=True)


class LibraryPartner(models.Model):
    _name = "library.rental"

    name = fields.Char('Name', required=True)
    email = fields.Char('E-mail')
    address = fields.Text('Address')
    partner_type = fields.Selection([('customer', 'Customer'),
                                     ('author', 'Author')])
    rental_ids = fields.One2many('library.rental')


class LibraryPublisher(models.Model):
    _name = "library.publisher"

    name = fields.Char('Name', required=True)
