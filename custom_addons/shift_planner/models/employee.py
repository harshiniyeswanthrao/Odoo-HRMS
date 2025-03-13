from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'


    # Many2many field to link an employee to multiple shifts
    shift_ids = fields.Many2many(
        'shift.planner',
        string="Shifts",
        help="Shifts assigned to the employee."
    )







# from odoo import models, fields
#
# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     preferred_shift = fields.Selection(
#         string="Preferred Shift",
#         selection=[
#             ('general', 'General Shift'),
#             ('morning', '6 AM - 2 PM'),
#             ('afternoon', '2 PM - 10 PM'),
#             ('evening', '10 PM - 6 AM')
#         ],
#         tracking=True
#     )
