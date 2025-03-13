from odoo import models, fields

class PlantManagement(models.Model):
    _name = 'plant.management'
    _description = 'Plant Management'
    _rec_name = 'name'

    name = fields.Char(string='Plant Name', required=True, ondelete='cascade')
    location = fields.Char(string='Location')
    description = fields.Text(string='Description')
    plant_lines = fields.One2many('plant.line', 'plant_id', string='Plant Lines',ondelete='cascade')

    def action_open_production_planning(self):
        """ Open Production Planning Name form with selected Plant """
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'production.planning.name',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_plant_id': self.id,  # Pass the selected Plant ID
            }
        }
