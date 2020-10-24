# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OpenacademyCourse(models.Model):
    _name = "openacademy.course"

    name = fields.Char(reqired=True)
    description = fields.Text()
    responsible_id = fields.Many2one('openacademy.partner')
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Session')
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
    start_date = fields.Date(default=date.today())
    end_date = fields.Date(default=date.today())
    duration = fields.Float(default=1)
    instruction_id = fields.Many2one('openacademy.partner')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete="cascade")
    attendee_ids = fields.Many2many('openacademy.partner')
    active = fields.Boolean('Active', default=True)
    seats = fields.Integer('# of seats')
    taken_seats = fields.Float('Taken seats', compute='_onchange_seats')


    @api.onchange('attendee_ids', 'seats')
    def _onchange_seats(self):
        for i in self:
            if not i.seats:
                i.taken_seats = 0.0
            else:
                self.taken_seats = 100*len(self.attendee_ids)/self.seats
        if self.taken_seats > 100:
            raise ValidationError(_('No more seats available, available seats: %s, number of students: %s'))\
              % (self.seats, self.attendee_ids)


class OpenacademyPartner(models.Model):
    _name = "openacademy.partner"

    name = fields.Char('Name')
    instructor = fields.Boolean('Instructor')
    session_id = fields.Many2many('openacademy.session',
                                  readonly=True)
