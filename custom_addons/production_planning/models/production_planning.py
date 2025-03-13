from odoo import models, fields, api
from datetime import datetime

class ProductionPlanning(models.Model):
    _name = 'production.planning'
    _description = 'Production Planning'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    user_id = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)

    name = fields.Many2one(
        'plant.management',
        string="Plant Name",
        required=True,
        default=lambda self: self.env['plant.management'].search([], limit=1).id,
        # Set default to the first available plant
        ondelete = 'cascade'
    )
    plant_id = fields.Many2one(
        'plant.management',
        string="Plant Name",
        required=True,
        default=lambda self: self.env['plant.management'].search([], limit=1).id,
        ondelete='cascade'
    )

    line_id = fields.Many2one('production.cell.line', string='Production Line', required=False, tracking=True)
    planning_name_id = fields.Many2one('production.planning.name', string='Planning Name', required=True, ondelete='cascade')
    part_lines = fields.One2many('production.planning.line', 'planning_id', string='Part Lines', tracking=True, ondelete='cascade')
    machine_id = fields.Many2one('machine.master', string='Machine', required=True, tracking=True)
    # Related fields to display additional machine details
    process = fields.Text(related="machine_id.process", string="Process", store=True)
    no_of_machines = fields.Integer(related="machine_id.no_of_machines", string="No. of Machines", store=True)
    oee = fields.Float(related="machine_id.oee", string="OEE (%)", store=True)

    working_days = fields.Integer(string="No of Working Days")
    part_master_id = fields.Many2one("part.master", string="Part Master")
    loaded_volume = fields.Float(
        string="Loaded Volume",
        compute="_compute_loaded_volume",
        store=True
    )
    total_demand = fields.Integer('Total Demand')
    sale_value_inr = fields.Float(string="Sale Value in INR")
    month = fields.Selection(
        [(str(i), datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)],
        string='Month',
        required=True,
        default=lambda self: str(datetime.now().month),
        # readonly=True
    )

    year = fields.Char(
        string='Year',
        required=True,
        default=lambda self: str(datetime.now().year),
        readonly=True
    )

    total_shifts = fields.Float(
        string='Total Shifts',
        compute='_compute_total_shifts',
        store=True
    )
    available_shifts = fields.Float(
        string='Available Shifts',
        compute='_compute_available_shifts',
        store=True  # Store the computed value in the database
    )
    shortage_shifts = fields.Float(
        string='Excess/Shortage Shifts',
        compute='_compute_shortage_shifts',
        store=True  # Store the computed value in the database
    )
    active = fields.Boolean('Active', default=True)
    box = fields.Char(string="Graph Description", default="x-axis: machines, y-axis: shift hours")
    loaded_volume = fields.Float(string="Loaded Volume", compute="_compute_loaded_volume", store=True)
    sale_value = fields.Float(string="Sale Value")


    @api.depends("total_demand")
    def _compute_loaded_volume(self):
        for record in self:
            # Here you calculate the loaded volume based on the total demand
            record.loaded_volume = record.total_demand  # Or any other formula

    @api.depends('part_lines.no_of_shifts')
    def _compute_total_shifts(self):
        for planning in self:
            total_shifts = sum(planning.part_lines.mapped('no_of_shifts'))
            planning.total_shifts = total_shifts

    @api.depends('machine_id')
    def _compute_available_shifts(self):
        for record in self:
            # Get the number of machines from the machine.master model
            no_of_machines = record.machine_id.no_of_machines if record.machine_id else 0
            record.available_shifts = no_of_machines * 25 * 3  # Formula: no_of_machines * 25 * 3

    @api.depends('available_shifts', 'part_lines')
    def _compute_shortage_shifts(self):
        for record in self:
            # Sum up the total shifts from the lines
            total_shifts = sum(line.no_of_shifts for line in record.part_lines)
            # Calculate shortage shifts
            record.shortage_shifts = record.available_shifts - total_shifts

    @api.onchange('machine_id')
    def _onchange_machine_id(self):
        """ Automatically update `pieces_per_min` and `oee` for all part lines when a machine is selected """
        for record in self:
            if record.machine_id:
                # Clear current part_lines before adding new ones
                record.part_lines = [(5, 0, 0)]  # This clears the existing lines

                # Update pieces_per_min and oee for each part line when machine is selected
                for part in record.machine_id.parts_ids:  # Assuming parts_ids is a field on 'machine.master'
                    line_vals = {
                        'part_master_id': part.id,
                        'total_demand': part.total_demand or 0,
                        'pieces_per_min': record.machine_id.actual_capacity or 0.0,
                        'oee': record.machine_id.oee or 0.0
                    }
                    record.part_lines = [(0, 0, line_vals)]  # This adds new lines based on the machine

    @api.onchange('production_cell_id')
    def _onchange_production_cell(self):
        """ Update the domain for the production line based on the selected production cell. """
        if self.production_cell_id:
            self.line_id = False  # Clear the previously selected line
            return {
                'domain': {
                    'line_id': [('cell_id', '=', self.production_cell_id.id)]
                }
            }

    @api.onchange('planning_name_id')
    def _onchange_planning_name_id(self):
        if self.planning_name_id:
            self.month = self.planning_name_id.month
            self.year = self.planning_name_id.year  # Set year from planning_name_id
            self.plant_id = self.planning_name_id.plant_id

    @api.model
    def create(self, vals):
        if 'year' not in vals or not vals.get('year'):
            vals['year'] = str(datetime.now().year)  # Default to current year
        return super(ProductionPlanning, self).create(vals)

    def write(self, vals):
        if 'year' in vals or not all(record.year for record in self):
            if not vals.get('year'):
                vals['year'] = str(datetime.now().year)  # Default to current year
        return super(ProductionPlanning, self).write(vals)

    @api.model
    def default_get(self, fields):
        res = super(ProductionPlanning, self).default_get(fields)
        if 'year' in fields and not res.get('year'):
            res['year'] = str(datetime.now().year)  # Default to current year
        return res



