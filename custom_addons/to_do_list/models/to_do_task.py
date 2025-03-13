from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ToDoTask(models.Model):
    _name = "to_do.task"
    _description = "To-Do Task"

    name = fields.Char("Task Name", required=True)
    description = fields.Text("Description")
    is_done = fields.Boolean("Done", default=False)
    priority = fields.Selection(
        [("low", "Low"), ("medium", "Medium"), ("high", "High")],
        "Priority",
        default="medium",
    )
    deadline = fields.Date("Deadline")
    assigned_to = fields.Many2one("res.users", "Assigned To")
    tags = fields.Many2many("to_do.tag", string="Tags")
    estimated_time = fields.Float("Estimated Time (hours)")
    progress = fields.Float("Progress (%)", default=0.0)
    attachments = fields.Many2many("ir.attachment", string="Attachments")
    is_recurring = fields.Boolean("Recurring Task", default=False)
    recurrence_interval = fields.Integer("Recurrence Interval (days)", default=7)

    @api.constrains('deadline')
    def _check_deadline(self):
        for record in self:
            if record.deadline and record.deadline < fields.Date.today():
                raise ValidationError("Deadline must be in the future.")

    @api.constrains('priority', 'deadline')
    def _check_priority_deadline(self):
        for record in self:
            if record.priority == "high" and not record.deadline:
                raise ValidationError("High-priority tasks must have a deadline.")

