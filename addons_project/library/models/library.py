# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models, _


class LibraryBook(models.Model):

    _inherit = "product.product"

#    name = fields.Char('Name', index=True, required=True)
    author_ids = fields.Many2many('res.partner', string='Author',
                                  index=True, domain="[('partner_type', '=', 'author')]")
    edition_date = fields.Date('Edition Date')
    isbn = fields.Char('ISBN', index=True, store=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher',
                                   domain="[('partner_type', '=', 'publisher')]")
    rental_ids = fields.One2many('library.rental', 'book_id', string='rental #')
    copy_ids = fields.One2many('library.copy', 'book_id', string='Copy #')
    is_book = fields.Boolean(string='Book', store=True, default=True)

    _sql_constrains = [
        ('isbn_uniq', 'unique(isbn)', ' Please enter Unique ISBN.')
                       ]


class LibraryCopy(models.Model):
    _name = "library.copy"
    _inherits = {'product.product': 'book_id'}

    book_id = fields.Many2one('product.product', delegate=True, required=True, ondelete="cascade",
                              domain="[('is_book', '=', 'True')]")
    reference = fields.Char(string='Reference', required=True)
    rental_ids = fields.One2many('library.rental', 'book_id', string='rental #')
    book_state = fields.Selection([('available', 'Available'),
                                   ('rented', 'Rented'),
                                   ('lost', 'Lost')], default='available')


class LibraryRental(models.Model):
    _name = "library.rental"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    customer_id = fields.Many2one('res.partner', string='Customer',
                                  store=True, required=True,
                                  domain="[('partner_type', '=', 'customer')]")
    book_id = fields.Many2one('product.product', related='copy_id.book_id', readonly=True,
                              domain="[('is_book', '=', 'True')]")
    rental_date = fields.Date(string='Rental Date', store=True, required=True)
    return_date = fields.Date(string='Return Date', store=True)
    planned_return_date = fields.Date(string='Planned Return Date', store=True, required=True)
    customer_address = fields.Char('Customer Address', related='customer_id.street')
    customer_email = fields.Char('Customer Email', related='customer_id.email')
    book_authors = fields.Char('Book authors', related='book_id.author_ids.name')
    book_edition_date = fields.Date('Edition Date', related='book_id.edition_date')
    book_publisher = fields.Char('Publisher', related='book_id.name')
    copy_id = fields.Many2one('library.copy', string='Copy #')
    reference = fields.Char('Reference', related='copy_id.reference')
    state = fields.Selection([('draft', 'draft'),
                              ('rented', 'Rented'),
                              ('returned', 'Returned'),
                              ('lost', 'Lost')], default='draft')

    @api.multi
    def _add_fee(self, type):
        if type == 'time':
            day_of_rental = (self.return_date - self.rental_date)
            sum = day_of_rental.days * self.env.ref('library.price_rent').price / self.env.ref(
                'library.price_rent').duration
        elif type == 'loss':
            sum = self.env.ref('library.price_loss').price
        self.env['library.payment'].create({'date': self.rental_date,
                                            'amount': sum,
                                            'customer_id': self.customer_id.id})

#       action buttons
    @api.multi
    def action_confirm(self):
        self.write({'state': 'rented'})
        for book in self.copy_id:
            book.write({'book_state': 'rented'})
        self._add_fee(type='time')

    @api.multi
    def action_return(self):
        self.write({'state': 'returned'})
        for book in self.copy_id:
            book.write({'book_state': 'available'})

    @api.multi
    def action_lost(self):
        self.write({'state': 'lost'})
        for book in self.copy_id:
            book.write({'book_state': 'lost',
                        'active': False})
        self._add_fee(type='loss')

# Cron for email reminder
    @api.one
    def search_for_debtors(self):
        for debtors in self:
            if debtors.state == 'rented' and date.today() > debtors.return_date:
                print('!!!!!!!!!!!!sending email !!!!!!!!!!!')
                template_id = debtors.env.ref('library.debtor_remainder_mail_template').id
                self.env['mail.template'].browse(template_id).send_mail(debtors.id, force_send=True)
#        for email in self.customer_email:
#            listdebtor = email.env['library.rental'].search([('return_date', '<', date.today())])



class Partner(models.Model):
    _inherit = "res.partner"

#    name = fields.Char('Name', required=True, store=True)
#    email = fields.Char('E-mail', store=True)
#    address = fields.Text('Address', store=True)
    partner_type = fields.Selection([('customer', 'Customer'),
                                     ('author', 'Author'),
                                     ('publisher', 'Publisher')])
    rental_ids = fields.One2many('library.rental', 'customer_id', string='rental #')
    payment_ids = fields.One2many('library.payment', 'customer_id', string='Payments')
    amount_owed = fields.Float(string="Amount Owed", compute='_compute_amount_owed')

    @api.depends('payment_ids')
    def _compute_amount_owed(self):
        for payment in self.payment_ids:
            self.amount_owed += payment.amount

# class LibraryPublisher(models.Model):
#    _name = "library.publisher"
#
#    name = fields.Char('Name', required=True)
