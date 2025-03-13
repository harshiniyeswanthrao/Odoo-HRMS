
from odoo import api, fields, models


class HrContract(models.Model):
    """Inherited HR Contract Model.This model extends the base 'hr.contract'
    model with an additional field 'emp_transfer' for linking to a transferred
    employee. The 'create' method is customized to handle the creation of new
    HR contract records. It also updates the state of the linked employee
    transfer record if applicable."""
    _inherit = 'hr.contract'

    emp_transfer = fields.Many2one(
        'employee.transfer', string='Transferred Employee',
        help="Employee who has been transferred")

    @api.model
    def create(self, vals):
        """Create a new HR contract record with the provided values."""
        res = super(HrContract, self).create(vals)
        if res.emp_transfer:
            res.emp_transfer.write(
                {'state': 'done'})
        return res
