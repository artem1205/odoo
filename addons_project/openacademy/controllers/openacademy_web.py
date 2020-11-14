# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.tools import html2plaintext

#
# class OpenacademyWebform(http.Controller):
#     @http.route('/openacademy/courses', auth='public', website=True)
#     def courses(self, **kw):
#         Courses = http.request.env['openacademy.course']
#         return http.request.render('library.index', {
#             'books': Books.search([('book_state', '!=', 'lost')])
#         })
    # def books(self, **kw):
    #     books = request.env['library.copy'].sudo().search([])
    #     html_result = '<html><body><ul>'
    #     for book in books:
    #         html_result += "<li> %s </li>" % book.name
    #     html_result += '</ul></body></html>'
    #     return html_result
