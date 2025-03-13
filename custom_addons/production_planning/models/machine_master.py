from odoo import api, models, fields

class MachineMaster(models.Model):
    _name = 'machine.master'
    _description = 'Machine Master'

    name = fields.Char('Machine Name', required=True)
    process = fields.Text('Process')  # Updated from "Description" to "Process"
    max_capacity = fields.Float('Maximum Capacity (Pcs/min)', required=True)  # Updated from "Capacity"
    actual_capacity = fields.Float('Actual Capacity (Pcs/min)', required=True)  # New field
    oee = fields.Float('OEE (%)',  store=True)  # New computed field
    no_of_machines = fields.Integer(string='No.of Machines', store=True)
    parts_ids = fields.Many2many('part.master', 'machine_part_rel', 'machine_id', 'part_id', string='Parts')
    plant_line_id = fields.Many2one('plant.line', string="Plant Line",ondelete="cascade")

    @api.depends('max_capacity', 'actual_capacity')
    def _compute_oee(self):
        for record in self:
            if record.max_capacity:
                record.oee = (record.actual_capacity / record.max_capacity) * 100
            else:
                record.oee = 0.0
