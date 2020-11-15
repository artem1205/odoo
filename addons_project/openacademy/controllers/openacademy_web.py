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


class OpenacademyWebform(http.Controller):
    @http.route('/openacademy/courses', auth='public', website=True)
    def courses(self, **kw):
        Courses = http.request.env['openacademy.course']
        return http.request.render('openacademy.courses', {
            'courses': Courses.search([])
        })

    @http.route('/openacademy/courses/<int:id>', auth='public', website=True)
    def course(self, id):
        course = http.request.env['openacademy.course'].search([('id', '=', id)])
        return http.request.render('openacademy.course_page', {
            'course': course
        })

    @http.route('/openacademy/sessions', auth='public', website=True)
    def courses(self, **kw):
        Sessions = http.request.env['openacademy.session']
        return http.request.render('openacademy.sessions', {
            'sessions': Sessions.search([])
        })

    @http.route('/openacademy/sessions/<int:id>', auth='public', website=True)
    def course(self, id):
        session = http.request.env['openacademy.session'].search([('id', '=', id)])
        return http.request.render('openacademy.session_page', {
            'session': session
        })
