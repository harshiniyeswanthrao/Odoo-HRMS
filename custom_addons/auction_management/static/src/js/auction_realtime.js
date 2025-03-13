odoo.define('auction_management.auction_realtime', function (require) {
    "use strict";

    $(document).ready(function () {
        const socket = new WebSocket("ws://localhost:8765"); // Update with your WebSocket server URL

        // Handle incoming messages
        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.event === 'new_bid') {
                const auctionId = data.data.auction_id;
                const newBidAmount = data.data.bid_amount;

                // Update the highest bid in the auction card
                const auctionCard = $(`#auction-${auctionId}`);
                if (auctionCard.length) {
                    auctionCard.find('.highest-bid').text(newBidAmount);
                }
            }
        };

        // Handle countdown timer
        $('.countdown-timer').each(function () {
            const endDate = new Date($(this).data('auction-end'));
            const countdownElem = $(this).find('.countdown-time');

            function updateCountdown() {
                const now = new Date();
                const timeLeft = endDate - now;

                if (timeLeft > 0) {
                    const hours = Math.floor(timeLeft / (1000 * 60 * 60));
                    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

                    countdownElem.text(`${hours}h ${minutes}m ${seconds}s`);
                } else {
                    countdownElem.text("Auction Ended");
                }
            }

            // Update countdown every second
            setInterval(updateCountdown, 1000);
        });

        // Handle WebSocket errors
        socket.onerror = function (error) {
            console.error("WebSocket Error:", error);
        };

        // Handle WebSocket close
        socket.onclose = function () {
            console.warn("WebSocket connection closed.");
        };
    });
});
