from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ShiftSwapRequest(models.Model):
    _name = 'shift.swap.request'
    _description = 'Shift Swap Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one(
        'hr.employee',
        string="Requesting Employee",
        required=True
    )

    shift_id = fields.Many2one(
        'shift.planner',
        string="Current Shift",
        required=True
    )

    swap_with_id = fields.Many2one(
        'hr.employee',
        string="Requested Swap With",
        required=True,
        domain="[('id', '!=', employee_id), ('id', 'in', shift_id.employee_ids)]"
    )

    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default="pending", tracking=True)

    @api.constrains('employee_id', 'swap_with_id')
    def _check_different_employees(self):
        for record in self:
            if record.employee_id == record.swap_with_id:
                raise ValidationError("You cannot swap shifts with yourself!")

    def approve_swap(self):
        """Approve the shift swap request and swap the employees in the shift."""
        for request in self:
            if request.status != 'pending':
                raise ValidationError("Only pending requests can be approved.")

            shift = request.shift_id

            if request.employee_id not in shift.employee_ids or request.swap_with_id not in shift.employee_ids:
                raise ValidationError("Both employees must be assigned to the shift before swapping.")

            # Swap employees in the shift
            shift.employee_ids = [(3, request.employee_id.id)]  # Remove employee
            shift.employee_ids = [(4, request.swap_with_id.id)]  # Add new employee

            # Mark as approved
            request.status = 'approved'

    def reject_swap(self):
        """Reject the shift swap request."""
        for request in self:
            if request.status != 'pending':
                raise ValidationError("Only pending requests can be rejected.")

            request.status = 'rejected'
