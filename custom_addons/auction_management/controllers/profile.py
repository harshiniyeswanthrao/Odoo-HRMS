from odoo import http
from odoo.http import request

class AuctionManagement(http.Controller):
    @http.route('/profile', type='http', auth='user', website=True)
    def user_profile(self, **kwargs):
        auction_user_id = request.session.get('auction_user_id')
        if not auction_user_id:
            return request.redirect('/auction/login')

        user = request.env['auction.user'].sudo().browse(auction_user_id)
        if not user.exists():
            return request.redirect('/auction/login')

        return request.render('auction_management.user_profile', {'user': user})

    @http.route('/profile/edit', type='http', auth='user', methods=['POST'], csrf=True, website=True)
    def save_profile(self, **post):
        auction_user_id = request.session.get('auction_user_id')
        if not auction_user_id:
            return request.redirect('/auction/login')

        user = request.env['auction.user'].sudo().browse(auction_user_id)
        if not user.exists():
            return request.redirect('/auction/login')

        # Update user details
        user.write({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'address': post.get('address'),
        })

        return request.redirect('/profile')
