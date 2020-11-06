# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OpenacademyCourse(models.Model):
    _name = "openacademy.course"

    name = fields.Char(reqired=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.partner')
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Session')
    level = fields.Selection([('easy', 'Easy'),
                              ('medium', 'Medium'),
                              ('hard', 'Hard')])
    attendee_count = fields.Integer("# of Attendees", compute='_number_of_attendees_course', store=True)
    can_edit_responsible = fields.Boolean(string='Can Edit ?', store=False, compute='_compute_responsible')

    @api.multi
    @api.depends('session_ids')
    def _number_of_attendees_course(self):
        for session in self:
            self.attendee_count += self.env['res.partner'].search_count(
                [('sessions_ids.id', 'in', session.session_ids.ids)])
        #   count = 0.0
        #   for attend in session.session_ids:

    #          count += self.env['res.partner'].search_count([('sessions_ids.id', '=', [attend.id])])
    # self.attendee_count = count

    @api.multi
    def open_attendees(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'All Attendees',
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain': [('sessions_ids.id', 'in', self.session_ids.ids)],
            'context': "{'create': False}"
        }

 #   @api.onchange('self.env.user')
    def _compute_responsible(self):
        archmaesters_group = self.env['res.groups'].search([('name', '=', 'Archmmaesters')])
        print(archmaesters_group)
        print(self.env.user.id, archmaesters_group.users.ids)
        if self.env.user.id in archmaesters_group.users.ids:
            print(True)
            self.can_edit_responsible = True


class OpenacademySession(models.Model):
    _name = "openacademy.session"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(reqired=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done')],
                             default='draft', index=True)
    start_date = fields.Date(default=date.today())
    end_date = fields.Date(default=date.today())
    duration = fields.Float(default=1)
    instruction_id = fields.Many2one('res.partner')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete="cascade")
    attendee_ids = fields.Many2many('res.partner', store=True)
    attendees_count = fields.Integer(string='# of Attendees', compute='_compute_attendees', store=True)
    active = fields.Boolean('Active', default=True)
    seats = fields.Integer('# of seats')
    taken_seats = fields.Float('Taken seats', compute='_onchange_seats')
    level = fields.Selection(related='course_id.level')

    @api.multi
    @api.depends('attendee_ids', 'seats')
    def _onchange_seats(self):
        for i in self:
            if not i.seats:
                i.taken_seats = 0.0
            else:
                i.taken_seats = 100.0 * len(i.attendee_ids) / i.seats

    @api.onchange('attendee_ids', 'seats', 'taken_seats')
    def _verify_seats(self):
        if self.taken_seats > 100:
            raise ValidationError('No more seats available, available seats: %s, number of students: %s' %
                                  (self.seats, len(self.attendee_ids)))

    def print_message_session(self):
        body = "Session: %s <br> Course: %s <br> State: %s" % (self.name, self.course_id.name, self.state)
        self.message_post(body=body)

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})
        self.print_message_session()

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        self.print_message_session()

    @api.multi
    def action_mark_done(self):
        self.write({'state': 'done'})
        self.print_message_session()

    @api.multi
    @api.onchange('taken_seats', 'state')
    def _autochange(self):
        for record in self:
            if record.taken_seats >= 50 and record.state == 'draft':
                record.state = 'confirmed'

    @api.model
    @api.multi
    def create(self, vals):
        result = super(OpenacademySession, self).create(vals)
        result.message_subscribe([result.instruction_id.id])
        return result

    @api.multi
    def write(self, vals):
        result = super(OpenacademySession, self).write(vals)
        for i in self:
            i.message_subscribe([i.instruction_id.id])
        return result

    @api.depends('attendee_ids')
    def _compute_attendees(self):
        for record in self:
            self.attendees_count = len(record.attendee_ids)


# class OpenacademyPartner(models.Model):
#    _name = "openacademy.partner"
#
#    name = fields.Char('Name')
#    instructor = fields.Boolean('Instructor')
#    session_id = fields.Many2many('openacademy.session',
#                                  readonly=True)


class OpenResPartner(models.Model):
    _inherit = "res.partner"

    instructor = fields.Boolean("Instructor", default=False)
    sessions_ids = fields.Many2many('openacademy.session', readonly=True, string="Sessions", store=True)
    level = fields.Integer(string="Level")

class SessionAddAttendees(models.TransientModel):
    _name = 'openacademy.session.add_attendees'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _get_default_attendees(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))

    session_id = fields.Many2one('openacademy.session', string='Sessions', required=True)
    attendee_ids = fields.Many2many('res.partner', string='Attendees', default=_get_default_attendees)

    def subscribe(self):
        for session in self.session_id:
            session.attendee_ids |= self.attendee_ids
        return {}
