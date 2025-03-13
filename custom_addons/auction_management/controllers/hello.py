import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class AuctionController(http.Controller):
    @http.route('/auction/get_highest_bid', type='http', auth="public", methods=['GET'], csrf=False)
    def get_highest_bid(self, **kwargs):
        auction_id = kwargs.get('auction_id')
        if not auction_id:
            return request.make_response(json.dumps({'error': 'auction_id is required'}), status=400)

        try:
            auction = request.env['auction.management'].browse(int(auction_id))
        except ValueError:
            _logger.error(f"Invalid auction_id format: {auction_id}")
            return request.make_response(json.dumps({'error': 'Invalid auction_id'}), status=400)

        if auction.exists():
            return request.make_response(
                json.dumps({'new_highest_bid': auction.highest_bid}),
                headers=[('Content-Type', 'application/json')]
            )
        else:
            return request.make_response(
                json.dumps({'error': 'Auction not found'}),
                status=404,
                headers=[('Content-Type', 'application/json')]
            )
