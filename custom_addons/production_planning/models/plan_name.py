from odoo import models, fields,api
from datetime import datetime

class ProductionPlanningName(models.Model):
    _name = 'production.planning.name'
    _description = 'Production Planning Name'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Plan Name', required=True, tracking=True,ondelete="cascade")
    plant_id = fields.Many2one('plant.management', string="Plant Name", required=True)
    # active = fields.Boolean('Active', default=True)
    # Related Production Planning records
    planning_ids = fields.One2many('production.planning', 'planning_name_id', string='Production Plans', ondelete='cascade')
    month = fields.Selection(
        [(str(i), datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        string='Month',
        required=True,
        tracking = True
    )
    year = fields.Char(
        string='Year',
        required=True,
        default=datetime.now().year,
        tracking=True
    )
    working_days = fields.Integer(string="No of Working Days")
    loaded_volume = fields.Float(string="Loaded Volume", compute="_compute_loaded_volume", store=True)
    sale_value_inr = fields.Float(string="Sale Value in INR", compute="_compute_sale_value_inr", store=True)
    plant_line_id = fields.Many2one('plant.line', string='Plant Line', ondelete='cascade')

    def action_approve(self):
        # Redirect to the specified URL
        return {
            'type': 'ir.actions.act_url',
            'url': 'http://localhost:8079/odoo/action-863#menu_id=546',
            'target': 'new',  # Opens in a new tab
        }

    def open_machine_analysis_graph(self):
        return {
            'name': 'Machine Analysis Graph',
            'type': 'ir.actions.act_window',
            'res_model': 'production.planning',  # Ensure this matches your model!
            'view_mode': 'graph',
            'views': [(self.env.ref('production_planning.view_machine_analysis_graph').id, 'graph')],
            'target': 'new',  # Open in a popup/modal
            'context': {
                'default_planning_name_id': self.id,
                'default_plant_id': self.plant_id.id
            },
        }


    @api.depends("plant_line_id")
    def _compute_loaded_volume(self):
        """Compute Loaded Volume as the sum of total demand from all parts in part.master"""
        for record in self:
            part_records = self.env["part.master"].search([])  # Fetch all part.master records
            record.loaded_volume = sum(part_records.mapped("total_demand"))  # Sum total_demand from all parts

    @api.depends("plant_line_id")
    def _compute_sale_value_inr(self):
        """Compute Sale Value in INR as the sum of sale value from all parts in part.master"""
        for record in self:
            part_records = self.env["part.master"].search([])  # Fetch all part.master records
            record.sale_value_inr = sum(part_records.mapped("sale_value"))  # Sum sale_value from all parts

    @api.model
    def default_get(self, fields_list):
        """Auto-populate planning_ids with machines and their associated parts"""
        res = super(ProductionPlanningName, self).default_get(fields_list)

        part_records = self.env["part.master"].search([])  # Fetch all part.master records

        planning_details = []
        total_loaded_volume = 0
        total_sale_value = 0

        for part in part_records:
            planning_details.append((0, 0, {
                "part_master_id": part.id,
                "total_demand": part.total_demand,
                "sale_value": part.sale_value
            }))
            total_loaded_volume += part.total_demand
            total_sale_value += part.sale_value

        res["planning_ids"] = planning_details
        res["loaded_volume"] = total_loaded_volume
        res["sale_value_inr"] = total_sale_value
        return res

    @api.onchange("plant_line_id")
    def _onchange_plant_line_id(self):
        """Dynamically update planning_ids with all machines"""
        if self.plant_line_id:
            machine_records = self.env["machine.master"].search([])  # Ensure we filter by plant line
            # Remove empty rows (entries with no machine_id)
            self.planning_ids = [(2, rec.id, 0) for rec in self.planning_ids if not rec.machine_id]

            planning_details = []
            for machine in machine_records:
                if not any(planning.machine_id.id == machine.id for planning in self.planning_ids):
                    planning_details.append((0, 0, {
                        "machine_id": machine.id
                    }))
                else:
                    # If the machine is already added, show a warning message
                    self.env.user.notify_info(f"Machine '{machine.name}' has already been added.")

            # Correcting this line to ensure proper IDs are used
            self.planning_ids = [(6, 0, [rec.id for rec in self.planning_ids])] + planning_details


    def action_open_machine_part_master(self):
        """Opens the Machine-Part Master List View when the button is clicked"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Machine-Part Master',
            'res_model': 'machine.part.master',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'},  # ✅ Open Form View in Edit Mode

        }

    def action_open_production_planning(self):
        """ Open the Production Planning form with auto-populated plant name """
        self.ensure_one()  # Ensure the action is performed on a single record

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'production.planning',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_plant_id': self.plant_id.id,  # Auto-populate Plant Name
                'default_planning_name_id': self.id,  # Link to Production Planning Name
            },
        }
