from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class PaymentController(http.Controller):
    @http.route('/payment_page', type='http', auth='public', website=True)
    def payment(self, **kwargs):
        auction_id = kwargs.get('auction_id')  # Get auction_id from the URL
        auction = request.env['new.auction'].sudo().browse(int(auction_id))

        # Get default EMD bank details
        emd_details = {
            'emd_bank_name': "HDFC Bank",
            'emd_account_number': "50200086849815",
            'emd_ifsc_code': "HDFC0001720"
        }



        if not auction.exists():
            return request.render('website.404')  # If the auction doesn't exist, show 404 page.

        # Pass auction to the template
        return request.render('auction_management.payment_template', {
            'auction': auction,
            'emd_details':emd_details
        })

    # @http.route('/payment/emd', type='http', auth='public', website=True, methods=['POST'])
    # def submit_emd(self, **kwargs):
    #     auction_id = kwargs.get('auction_id')
    #     auction = request.env['new.auction'].sudo().browse(int(auction_id))
    #
    #     if not auction.exists():
    #         return request.render('website.404')  # If the auction doesn't exist, show 404 page.
    #
    #     # Get the auction user (assuming logged-in user has auction_user_id in session)
    #     auction_user_id = request.session.get('auction_user_id')
    #
    #     # Check if all necessary fields are provided in the POST data
    #     aadhaar_card = kwargs.get('aadhaar_card')
    #     pan_card = kwargs.get('pan_card')
    #     blank_cheque = kwargs.get('blank_cheque')
    #
    #     if not (aadhaar_card and pan_card and blank_cheque):
    #         return request.render('website.404')  # Return a 404 or error page if files are not uploaded
    #
    #     # Create the EMD record in the database
    #     emd_record = request.env['auction.emd'].sudo().create({
    #         'user_id': auction_user_id,
    #         'auction_id': auction_id,
    #         'payment_status': 'pending',  # Initially set to 'pending'
    #         'aadhaar_card': aadhaar_card,
    #         'pan_card': pan_card,
    #         'blank_cheque': blank_cheque,
    #     })
    #
    #     # Once EMD is successfully submitted, redirect to the payment success page
    #     return request.redirect('/payment/success?auction_id=' + str(auction_id))

    @http.route('/payment/success', type='http', auth='public', website=True)
    def payment_success(self, **kwargs):
        # Fetch the logged-in auction user from the session
        auction_user_id = request.session.get('auction_user_id')

        # Safely fetch and parse auction_id
        auction_id = int(kwargs.get('auction_id'))

        # Ensure the auction exists
        auction = request.env['new.auction'].sudo().browse(auction_id)
        if not auction.exists():
            return request.not_found()

        # Create the EMD payment record
        request.env['auction.emd'].sudo().create({
            'user_id': auction_user_id,  # Store the custom auction user
            'auction_id': auction_id,
            'payment_status': 'paid',
        })

        return request.render('auction_management.payment_success_template', {'auction_id': auction_id})

