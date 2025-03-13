from odoo import http
from odoo.http import request

class AuctionController(http.Controller):

    @http.route('/auction/table', type='http', auth='public', website=True)
    def auction_filter(self, **kwargs):
        # Fetch filter parameters
        state = kwargs.get('state')
        city = kwargs.get('city')
        property_type = kwargs.get('type')
        price_min = kwargs.get('price_min')
        price_max = kwargs.get('price_max')
        status = kwargs.get('status')
        search_query = kwargs.get('search')

        # Build domain for filtering
        domain = []

        if state:
            domain.append(('auction_property.state', '=', state))
        if city:
            domain.append(('auction_property.city', '=', city))
        if property_type:
            domain.append(('auction_property.type.name', '=', property_type))
        if price_min:
            domain.append(('reserve_price', '>=', float(price_min)))
        if price_max:
            domain.append(('reserve_price', '<=', float(price_max)))
        if status:
            domain.append(('status', '=', status))
        if search_query:
            domain.append(('auction_name', 'ilike', search_query))

        # Search auctions
        auctions = request.env['new.auction'].sudo().search(domain)

        # Prepare data for the template
        auction_data = [{
            'auction_id': auction.id,
            'auction_name': auction.auction_name,
            'asset_on_auction': auction.auction_property.name,
            'city': auction.auction_property.city,
            'state': auction.auction_property.state,
            'reserve_price': auction.reserve_price,
            'status': auction.status,
            'highest_bid': auction.highest_bid,
            'emd_amount': auction.emd_amount,
            'remaining_time': auction.remaining_time
        } for auction in auctions]

        # Get distinct values for filters
        properties = request.env['new.property'].sudo().search([])
        states = list(set(properties.mapped('state')))
        cities = list(set(properties.mapped('city')))
        types = list(set(properties.mapped('type.name')))
        statuses = request.env['new.auction']._fields['status'].selection

        # Render template
        return request.render('auction_management.auction_webpage', {
            'auctions': auction_data,
            'states': states,
            'cities': cities,
            'types': types,
            'statuses': [status[0] for status in statuses]  # Extract status keys
        })
