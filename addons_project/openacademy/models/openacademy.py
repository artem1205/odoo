# -*- coding: utf-8 -*-


from datetime import datetime
from odoo import fields, models


class OpenacademyCourse(models.Model):
    _name = "openacademy.course"

    name = fields.Char(reqired=True)
    description = fields.Text
    responsible_id = fields.Many2one('openacademy.partner')
    session_ids = fields.One2many('openacademy.session')
    level = fields.Selection([('easy', 'Easy'),
                              ('medium', 'Medium'),
                              ('hard', 'Hard')])


class OpenacademySession(models.Model):
    _name = "openacademy.session"

    name = fields.Char(reqired=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done')],
                             default='draft')
    start_date = fields.Date(default = datetime.today())
    end_date = fields.Date(default=datetime.today())
    duration = fields.Float(default = 1)
    instruction_id = fields.Many2one('openacademy.partner')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete="cascade")
    attendee_ids = fields.Many2many('openacademy.partner')
    active = fields.Boolean('Active', default=True)


class OpenacademyPartner(models.Model):
    _name = "openacademy.partner"

    name = fields.Char('Name')
    instructor = fields.Boolean('Instructor')
    session_id = fields.Many2many('openacademy.session',
                                  readonly=True)