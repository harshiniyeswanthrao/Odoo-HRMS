from odoo import http
from odoo.http import request


class AuctionSearchController(http.Controller):
    @http.route('/auction/filters', type='http', auth='public', website=True)
    def auction_search(self, **kwargs):
        # Fetch dropdown data
        states = request.env['new.property'].sudo().search_read([], ['state'])
        districts = request.env['new.property'].sudo().search_read([], ['district'])
        cities = request.env['new.property'].sudo().search_read([], ['city'])
        types = request.env['asset.category'].sudo().search_read([], ['name'])

        # Determine price range
        min_price = 0.0
        max_price_record = request.env['new.property'].sudo().search_read([], ['price'], limit=1, order='price DESC')
        max_price = max_price_record[0]['price'] if max_price_record else 1000000.0

        # Filters
        domain = [('status', 'in', ['confirmed', 'running'])]  # Filter auctions by status

        if kwargs.get('state'):
            domain.append(('auction_property.state', '=', kwargs['state']))
        if kwargs.get('district'):
            domain.append(('auction_property.district', '=', kwargs['district']))
        if kwargs.get('city'):
            domain.append(('auction_property.city', '=', kwargs['city']))
        if kwargs.get('type'):
            domain.append(('auction_property.type.name', '=', kwargs['type']))
        if kwargs.get('min_price') and kwargs.get('max_price'):
            domain.append(('auction_property.price', '>=', float(kwargs['min_price'])))
            domain.append(('auction_property.price', '<=', float(kwargs['max_price'])))

        # New: Query-based search
        if kwargs.get('query'):
            query = kwargs['query']
            domain.append('|')
            domain.append(('auction_name', 'ilike', query))
            domain.append(('auction_property.address', 'ilike', query))

            # domain.append(('auction_property.state', 'ilike', query))
            # domain.append(('auction_property.city', 'ilike', query))
            # domain.append(('auction_property.type', 'ilike', query))

        # Fetch search results (auctions)
        auctions = request.env['new.auction'].sudo().search(domain)

        # Unique dropdown options
        unique_states = list({state['state'] for state in states if state['state']})
        unique_districts = list({district['district'] for district in districts if district['district']})
        unique_cities = list({city['city'] for city in cities if city['city']})
        property_types = [ptype['name'] for ptype in types]

        # Render template
        return request.render('auction_management.auction_search_ui', {
            'states': unique_states,
            'districts': unique_districts,
            'cities': unique_cities,
            'property_types': property_types,
            'min_price': min_price,
            'max_price': max_price,
            'search_results': auctions,  # Pass filtered results
            'selected_state': kwargs.get('state', ''),
            'selected_district': kwargs.get('district', ''),
            'selected_city': kwargs.get('city', ''),
            'selected_type': kwargs.get('type', ''),
            'selected_min_price': kwargs.get('min_price', min_price),
            'selected_max_price': kwargs.get('max_price', max_price),
            'selected_query': kwargs.get('query', ''),
        })
