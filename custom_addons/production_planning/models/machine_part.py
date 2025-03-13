from odoo import models, fields, api


class MachinePartMaster(models.Model):
    _name = "machine.part.master"
    _description = "Combined Machine and Part Master Data"

    # Machine Master Fields
    machine_id = fields.Many2one('machine.master', string="Machine")
    machine_name = fields.Char(related="machine_id.name", string="Machine Name", store=True)
    process = fields.Text(related="machine_id.process", string="Process")
    max_capacity = fields.Float(related="machine_id.max_capacity", string="Max Capacity (Pcs/min)")
    actual_capacity = fields.Float(related="machine_id.actual_capacity", string="Actual Capacity (Pcs/min)")
    oee = fields.Float(related="machine_id.oee", string="OEE (%)")
    no_of_machines = fields.Integer(related="machine_id.no_of_machines", string="No. of Machines")

    # Part Master Fields
    part_id = fields.Many2one('part.master', string="Part")
    part_name = fields.Char(related="part_id.name", string="Part Name", store=True)
    item_code = fields.Char(related="part_id.item_code", string="Item Code")
    part_number = fields.Char(related="part_id.part_number", string="Part Number")
    total_demand = fields.Integer(related="part_id.total_demand", string="Total Demand")
    price_per_piece = fields.Float(related="part_id.price_per_piece", string="Price/Piece")
    sale_value = fields.Integer(related="part_id.sale_value", string="Sale Value/Month")
    quality = fields.Char(related="part_id.quality", string="Quality")
    size = fields.Char(related="part_id.size", string="Size")
    operation_weight = fields.Float(related="part_id.operation_weight", string="Operation Weight (Kg/1000 nos)")
    total_weight = fields.Float(related="part_id.total_weight", string="Total Weight (Kg)")
    total_demand_sum = fields.Integer(string="Total Demand (Sum)", compute="_compute_total_demand")
    total_sale_value_sum = fields.Integer(string="Total Sale Value (Sum)", compute="_compute_totals", store=True)
    total_weight_sum = fields.Float(string="Total Weight (Sum)", compute="_compute_totals", store=True)

    @api.depends('total_demand', 'sale_value', 'total_weight')
    def _compute_totals(self):
        total_demand = sum(self.search([]).mapped('total_demand'))
        total_sale_value = sum(self.search([]).mapped('sale_value'))
        total_weight = sum(self.search([]).mapped('total_weight'))

        for record in self:
            record.total_demand_sum = total_demand
            record.total_sale_value_sum = total_sale_value
            record.total_weight_sum = total_weight

    @api.model
    def create(self, vals):
        # Ensure vals does not already contain a recursive call to create()
        if "machine_id" in vals and "part_id" in vals:
            return super(MachinePartMaster, self).create(vals)

        # Fetch only necessary data
        machine_records = self.env["machine.master"].search([])
        part_records = self.env["part.master"].search([])

        new_records = []
        for machine in machine_records:
            for part in part_records:
                new_records.append({
                    "machine_id": machine.id,
                    "part_id": part.id
                })

        # Bulk create records
        if new_records:
            self.env["machine.part.master"].create(new_records)

        return super(MachinePartMaster, self).create(vals)
