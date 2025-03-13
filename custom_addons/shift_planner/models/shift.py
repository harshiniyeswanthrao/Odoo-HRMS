from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ShiftPlanner(models.Model):
    _name = 'shift.planner'
    _description = 'Shift Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Selection(
        string="Shift Name",
        selection=[
            ('general', 'General Shift'),
            ('morning', '6 AM - 2 PM'),
            ('afternoon', '2 PM - 10 PM'),
            ('evening', '10 PM - 6 AM')
        ],
        required=True,
        tracking=True
    )

    shift_type = fields.Selection([
        ('regular', 'Regular'),
        ('overtime', 'Overtime'),
        ('night', 'Night Shift'),
    ],
        string="Shift Type",
        required=True
    )

    start_datetime = fields.Datetime(string="Start Time", required=True, tracking=True)
    end_datetime = fields.Datetime(string="End Time", required=True, tracking=True)
    employee_ids = fields.Many2many('hr.employee', string="Employees", tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    working_hours = fields.Float(string="Working Hours", compute="_compute_working_hours", store=True)

    shift_employee_count = fields.Integer(
        string="Employee Count",
        compute="_compute_shift_employee_count",
        store=True
    )

    def action_swap_shift(self):
        """Open Shift Swap Request Form"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Shift Swap Request',
            'res_model': 'shift.swap.request',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.depends('start_datetime', 'end_datetime')
    def _compute_working_hours(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                duration = (record.end_datetime - record.start_datetime).total_seconds() / 3600.0
                record.working_hours = round(duration, 2)
            else:
                record.working_hours = 0

    @api.depends('employee_ids')
    def _compute_shift_employee_count(self):
        """Compute the count of employees assigned to a shift."""
        for record in self:
            record.shift_employee_count = len(record.employee_ids)

    @api.constrains('shift_employee_count', 'start_datetime', 'end_datetime')
    def _check_shift_overlap(self):
        for record in self:
            print(
                f"🔍 Checking shift for: {record.employee_ids.mapped('name')} from {record.start_datetime} to {record.end_datetime}")

            for employee in record.employee_ids:
                overlapping_shifts = self.env['shift.planner'].search([
                    ('id', '!=', record.id),  # Ignore the current record
                    ('employee_ids', 'in', employee.id),
                    ('start_datetime', '<', record.end_datetime),
                    ('end_datetime', '>', record.start_datetime)
                ])

                if overlapping_shifts:
                    print(f"❌ Overlap found for {employee.name} with shift IDs: {overlapping_shifts.mapped('id')}")
                    raise ValidationError(
                        f" Employee {employee.name} is already assigned to another shift during this time."
                    )

            print("✅ No overlapping shifts found")
