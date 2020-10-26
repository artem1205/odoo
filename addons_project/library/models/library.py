# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models, _


class LibraryBook(models.Model):
    _name = "library.book"

    name = fields.Char('Name', index=True, required=True)
    author_ids = fields.Many2many('library.partner', string='Author', index=True)
    edition_date = fields.Date('Edition Date')
    isbn = fields.Char('ISBN', index=True)
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    rental_ids = fields.One2many('library.rental', 'book_id', string='rental #')
    copy_ids = fields.One2many('library.copy', 'book_id', string='Copy #')


class LibraryCopy(models.Model):
    _name = "library.copy"
    _inherits = {'library.book': 'book_id'}

    book_id = fields.Many2one('library.book', delegate=True, required=True, ondelete="cascade")
    reference = fields.Char(string='Reference', required=True)
    rental_ids = fields.One2many('library.rental', 'book_id', string='rental #')


class LibraryRental(models.Model):
    _name = "library.rental"

    customer_id = fields.Many2one('library.partner', string='Customer',
                                  store=True, required=True)
    book_id = fields.Many2one('library.book', related='copy_id.book_id', readonly=True)
    rental_date = fields.Date(string='Rental Date', store=True, required=True)
    return_date = fields.Date(string='Return Date', store=True)
    planned_return_date = fields.Date(string='Planned Return Date', store=True, required=True)
    customer_address = fields.Text('Customer Address', related='customer_id.address')
    customer_email = fields.Char('Customer Email', related='customer_id.email')
    book_authors = fields.Char('Book authors', related='book_id.author_ids.name')
    book_edition_date = fields.Date('Edition Date', related='book_id.edition_date')
    book_publisher = fields.Char('Publisher', related='book_id.name')
    copy_id = fields.Many2one('library.copy', string='Copy #')
    reference = fields.Char('Reference', related='copy_id.reference')

class LibraryPartner(models.Model):
    _name = "library.partner"

    name = fields.Char('Name', required=True, store=True)
    email = fields.Char('E-mail', store=True)
    address = fields.Text('Address', store=True)
    partner_type = fields.Selection([('customer', 'Customer'),
                                     ('author', 'Author')])
    rental_ids = fields.One2many('library.rental', 'customer_id', string='rental #')


class LibraryPublisher(models.Model):
    _name = "library.publisher"

    name = fields.Char('Name', required=True)
