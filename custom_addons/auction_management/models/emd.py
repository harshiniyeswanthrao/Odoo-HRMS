from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EMD(models.Model):
    _name = "auction.emd"
    _description = "Earnest Money Deposit"


    user_id = fields.Many2one("auction.user", string="EMD User")
    auction_id = fields.Many2one('new.auction', string="Auction", required=True, ondelete="cascade")
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], default='pending', string="Payment Status", required=True)

    # EMD default bank details
    emd_bank_name = fields.Char(string="EMD Deposit Bank Name", default="HDFC Bank", readonly=True)
    emd_account_number = fields.Char(string="EMD Deposit Bank Account Number", default="50200086849815", readonly=True)
    emd_ifsc_code = fields.Char(string="EMD Deposit Bank IFSC Code", default="HDFC0001720", readonly=True)

    # Fields to upload supporting documents
    aadhaar_card = fields.Binary(string="Aadhaar Card", attachment=True)
    pan_card = fields.Binary(string="PAN Card", attachment=True)
    blank_cheque = fields.Binary(string="Blank Cheque", attachment=True)

    _sql_constraints = [
        ('unique_user_auction', 'unique(user_id, auction_id)', "EMD payment already exists for this user and auction.")
    ]

    @api.depends('auction_id')
    def _compute_emd_amount(self):
        for rec in self:
            # Here, we calculate EMD amount if necessary. For now, set a static value for simplicity.
            rec.emd_amount = 106000.0  # You can add dynamic calculation if needed based on auction properties.

    emd_amount = fields.Float(string="EMD Amount", compute="_compute_emd_amount", store=True)
