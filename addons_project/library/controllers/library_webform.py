# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime

from odoo import http, fields
from odoo.http import request


class Library(http.Controller):
    @http.route('/library/', auth='user', website=True)
    def index(self, **kw):
        Books = http.request.env['library.copy']
        return http.request.render('library.copy_list', {
            'books': Books.search([('book_state', '!=', 'lost')])
        })

    @http.route('/library/<int:id>', auth='user', website=True)
    def book_check_info(self, id):
        book = http.request.env['library.copy'].search([('id', '=', id)])
        if book.book_state != 'available':
            return request.render('library.rental_decline', {'book': book})
        else:
            return http.request.render('library.book_page', {
                'book': book
            })

    @http.route('/library/rent/<int:id>', auth='user', website=True)
    def rent(self, id):
        partner = http.request.env.user.partner_id
        copy = http.request.env['library.copy'].search([('id', '=', id)])
        rental = http.request.env['library.rental'].create({
            'copy_id': copy.id,
            'customer_id': partner.id,
            'rental_date': datetime.date.today(),
            'planned_return_date': datetime.date.today() + datetime.timedelta(days=30),
            'return_date': datetime.date.today() + datetime.timedelta(days=30),
        })
        rental.action_confirm()
        return request.render('/library/success', {})
