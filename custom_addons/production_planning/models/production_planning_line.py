from email.policy import default

from odoo import models, fields, api


class ProductionPlanningLine(models.Model):
    _name = 'production.planning.line'
    _description = 'Production Planning Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    planning_id = fields.Many2one('production.planning', string='Production Planning', tracking=True, ondelete='cascade')
    part_master_id = fields.Many2one('part.master', string='Part', ondelete='cascade', required=True, tracking=True)
    total_demand = fields.Integer(string='Total Demand')
    sale_value = fields.Float(string="Sale Value in INR")  # ADD THIS FIELD

    # Fields for machine
    pieces_per_min = fields.Float(
        string='Pieces per Minute',
        default=0.0,
        help="This value is populated from the machine selected in Production Planning. Editable."
    )
    oee = fields.Float(
        string='OEE (%)',
        default=0.0,
        help="This value is populated from the machine selected in Production Planning. Editable."
    )

    # Computed field for no_of_shifts
    no_of_shifts = fields.Float(
        string='Shifts Needed',
        compute='_compute_no_of_shifts',
        store=True
    )

    @api.depends('total_demand', 'pieces_per_min', 'oee')
    def _compute_no_of_shifts(self):
        for line in self:
            if line.pieces_per_min and line.oee:
                line.no_of_shifts = (line.total_demand) / (
                    line.pieces_per_min * 450 * line.oee / 100)  # Adjusting OEE to percentage
            else:
                line.no_of_shifts = 0.0

    @api.onchange('part_master_id')
    def _onchange_part_master(self):
        """
        Automatically populate `total_demand` when a part is selected.
        The value can still be edited by the user.
        """
        for line in self:
            if line.part_master_id:
                line.total_demand = line.part_master_id.total_demand or 0  # Default to total demand of the part

    @api.onchange('planning_id')
    def _onchange_planning_id(self):
        """
        Populate `pieces_per_min` and `oee` from the machine selected in the parent planning record.
        """
        for line in self:
            if line.planning_id and line.planning_id.machine_id:
                machine = line.planning_id.machine_id
                line.pieces_per_min = machine.actual_capacity or 0.0
                line.oee = machine.oee or 0.0

    @api.model
    def create(self, vals):
        # Ensure that if a new part is added, the part's information is handled properly
        if 'part_master_id' in vals:
            part = self.env['part.master'].browse(vals['part_master_id'])
            # Optionally, do additional checks or modifications before creating the line
        return super(ProductionPlanningLine, self).create(vals)

