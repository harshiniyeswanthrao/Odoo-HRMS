from odoo import models, fields, api
from odoo.exceptions import UserError

class PartMaster(models.Model):
    _name = 'part.master'
    _description = 'Part Master'

    name = fields.Char('Part Name', required=True)
    customer_name = fields.Char(string='Customer Name')
    description = fields.Text('Description')
    item_code = fields.Char('Item Code', required=True)
    part_number = fields.Char('Part Number')
    price_per_piece = fields.Float('Price/Piece', required=True)
    quality = fields.Char('Quality')
    size = fields.Char('Size')
    pieces_per_min = fields.Float(string='Pieces per min')
    sale_value = fields.Integer(string='Sale value/month')
    operation_weight = fields.Float(string='Operation weight in kgs/1000 nos')
    total_demand = fields.Integer('Total Demand')
    # machine_id = fields.Many2one('machine.master', string='Machine', required=True,ondelete="cascade")

    total_weight = fields.Float(
        string='Total Weight (kg)',
        compute='_compute_total_weight',
        store=True
    )

    @api.depends('sale_value', 'operation_weight')
    def _compute_total_weight(self):
        for record in self:
            if record.sale_value and record.operation_weight:
                record.total_weight = (record.sale_value / 1000) * record.operation_weight
            else:
                record.total_weight = 0.0

    @api.model
    def create(self, vals):
        # Just create the part without worrying about the machine_id
        return super(PartMaster, self).create(vals)

    def write(self, vals):
        # Handle any write-related logic here
        # Ensure no recursion occurs here as well
        return super(PartMaster, self).write(vals)

    @api.model
    def unlink(self):
        for record in self:
            # Check for dependent records before allowing deletion
            dependent_records = self.env['production.planning'].search([('part_master_id', '=', record.id)])
            if dependent_records:
                raise UserError('This Part Master is being used in Production Planning. Cannot delete.')
        return super(self.__class__, self).unlink()
