from odoo import models, fields, api
from datetime import date, timedelta

class Employee(models.Model):
    _inherit = 'hr.employee'

    upcoming_anniversary = fields.Boolean(string="Upcoming Anniversary", compute="_compute_upcoming_anniversary")
    days_left = fields.Integer(string="Days Left", compute="_compute_days_left")

    @api.depends('joining_date')
    def _compute_upcoming_anniversary(self):
        today = date.today()
        for record in self:
            if record.joining_date:
                # Calculate the anniversary date
                anniversary_date = record.joining_date.replace(year=today.year)
                if today <= anniversary_date <= today + timedelta(days=30):
                    record.upcoming_anniversary = True
                else:
                    record.upcoming_anniversary = False

    @api.depends('joining_date')
    def _compute_days_left(self):
        today = date.today()
        for record in self:
            if record.joining_date:
                anniversary_date = record.joining_date.replace(year=today.year)
                record.days_left = (anniversary_date - today).days if anniversary_date >= today else 0
