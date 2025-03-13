from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class ForgotPasswordController(http.Controller):

    # Route for displaying the Forgot Password page
    @http.route('/auction/forgot_password', type='http', auth='public', website=True)
    def forgot_password(self, **kwargs):
        # Render the Forgot Password page (initial state with email input only)
        return request.render('auction_management.forgot_password_template', {'email_exists': False, 'email_not_found': False})

    # Route for submitting email and checking if the email exists
    @http.route('/auction/forgot_password/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def check_email(self, **kwargs):
        email = kwargs.get('email')

        # Check if the email exists in the system
        user = request.env['auction.user'].sudo().search([('email', '=', email)], limit=1)

        if user:
            # Email exists, render the page with the password reset form
            return request.render('auction_management.forgot_password_template', {
                'email_exists': True,
                'email': email
            })
        else:
            # Email not found, show error message
            return request.render('auction_management.forgot_password_template', {
                'email_not_found': True,
                'email_exists': False
            })

    # Route for submitting the new password
    @http.route('/auction/reset_password/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def reset_password(self, **kwargs):
        email = kwargs.get('email')  # The email is passed in the form
        new_password = kwargs.get('new_password')
        confirm_new_password = kwargs.get('confirm_new_password')

        # Validate password confirmation
        if new_password != confirm_new_password:
            return request.render('auction_management.forgot_password_template', {
                'error': 'Passwords do not match.',
                'email_exists': True,
                'email': email
            })

        # Update the password for the user
        user = request.env['auction.user'].sudo().search([('email', '=', email)], limit=1)

        if user:
            user.write({'password': new_password})
            return request.redirect('/auction/login')
        else:
            return request.render('auction_management.forgot_password_template', {
                'error': 'Email not found. Please register first.',
                'email_exists': False,
                'email_not_found': True
            })
