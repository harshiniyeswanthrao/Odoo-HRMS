from pygments.lexer import default

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random
import logging

_logger = logging.getLogger(__name__)

class NewUser(models.Model):
    _name = "auction.user"
    _description = "User information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True)
    email = fields.Char(string='Email', required=True, unique=True)
    password = fields.Char(string='Password', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True)
    bid_id = fields.Many2one('bid.logs', string="Bid")
    emd_id=fields.Many2one('auction.emd', string="EMD")
    emd_amount_paid = fields.Boolean(string="EMD Amount Paid",default=False)
    emd_status = fields.Selection([
        ('paid','Paid'),
        ('not_paid','Not Paid'),
    ])

    def check(self):
        for record in self:
            if record.emd_amount_paid == True:
                record.emd_status = 'paid'
            if record.emd_amount_paid == False:
                record.emd_status = 'not_paid'

    # def emd_paid(self):
    #     for record in self:
    #         if record.emd_amount_paid == True:
    #             record.emd_status = 'paid'
    #
    # def emd_not_paid(self):
    #     for record in self:
    #         if record.emd_amount_paid == False:
    #             record.emd_status = 'not_paid'

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'The email must be unique.'),
    ]

    def _check_email_format(self):
        for record in self:
            if not record.email or '@' not in record.email:
                raise ValidationError(_("Please provide a valid email address"))

    def check_credentials(self, email, password):
        user = self.search([('email', '=', email), ('password', '=', password)], limit=1)
        return user

    @api.model
    def reset_password(self, email, new_password):
        user = self.search([('email', '=', email)], limit=1)
        if user:
            user.write({'password': new_password})
            return True
        return False


class UserRegisterOtp(models.Model):
    _name = "user.register.otp"
    _description = "User OTP for Registration"

    email = fields.Char(string="Email", required=True)
    otp = fields.Char(string='OTP')  # Temporary field for storing OTP
    expire_time = fields.Datetime(string="Expire Time", required=True)
    otp_verified = fields.Boolean(string='OTP Verified', default=False)

    @api.model
    def generate_otp(self, email):
        try:
            otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP

            # Set OTP expiration time (5 minutes)
            expire_time = fields.Datetime.now() + timedelta(minutes=5)

            # Create or update the OTP record for the email
            existing_otp = self.search([('email', '=', email)], limit=1)
            if existing_otp:
                existing_otp.write({'otp': otp, 'expire_time': expire_time})
            else:
                self.create({'otp': otp, 'expire_time': expire_time, 'email': email})

            # Send OTP via email
            mail_values = {
                'subject': 'Your OTP for Auction Registration/Password Reset',
                'email_to': email,
                'body_html': f"""
                    <p>Hello,</p>
                    <p>Your OTP for registration or password reset is: <strong>{otp}</strong></p>
                    <p>This OTP is valid for 5 minutes.</p>
                """,
                'email_from': 'no-reply@example.com',  # Set this to a valid sender email address
            }

            # Create and send the email
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

            _logger.info(f"OTP sent to {email}")
            return True

        except Exception as e:
            _logger.error(f"Error generating OTP for {email}: {e}")
            return False

    def verify_otp(self, email, otp):
        otp_record = self.search([('email', '=', email), ('otp', '=', otp)], limit=1)

        if not otp_record:
            return {'success': False, 'error': 'Invalid OTP.'}

        # Check if OTP has expired
        if otp_record.expire_time < fields.Datetime.now():
            return {'success': False, 'error': 'OTP has expired.'}

        # OTP is valid
        otp_record.write({'otp_verified': True})
        return {'success': True, 'message': 'OTP verified successfully.'}
