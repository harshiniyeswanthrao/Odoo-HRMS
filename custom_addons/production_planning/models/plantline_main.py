from odoo import models, fields, api
from datetime import datetime

class PlantLine(models.Model):
    _name = 'plant.line'
    _description = 'Plant Line'
    _inherit = ['mail.thread']


    name = fields.Char(string='Line Name', required=True)
    plant_id = fields.Many2one('plant.management', string='Plant Name', required=True, ondelete='cascade')

    def action_open_planning_name(self):
        """ Open existing Production Planning Name if available, otherwise open a new form """
        self.ensure_one()  # Ensure the action is performed on a single record

        existing_planning = self.env['production.planning.name'].search([('plant_line_id', '=', self.id)], limit=1)

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'production.planning.name',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_plant_line_id': self.id,  # Auto-populate Line Name
                'default_plant_id': self.plant_id.id  # Auto-populate Plant Name
            },
        }

        if existing_planning:
            action['res_id'] = existing_planning.id  # Open existing record

        return action

