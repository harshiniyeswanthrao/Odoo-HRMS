// Function to fetch the updated auction data (including highest bid) for all auctions
function fetchAuctionList() {
    return fetch('/auction/real_time_auction_list')  // The new Odoo route to get the latest auction data
        .then(response => response.json())
        .then(data => data.auctions);  // Assuming the response is like { auctions: [ ... ] }
}

// Function to update the DOM with the latest auction data
function updateAuctionList(auctions) {
    auctions.forEach(auction => {
        // Update the highest bid for each auction
        const currentBidElement = document.getElementById(`currentBid_${auction.id}`);
        if (currentBidElement) {
            currentBidElement.textContent = auction.highest_bid;
        }
    });
}

// Function to refresh the auction list every millisecond
function refreshAuctionListEveryMillisecond() {
    setInterval(function () {
        fetchAuctionList().then(auctions => {
            updateAuctionList(auctions);
        }).catch(error => {
            console.error("Error fetching auction data:", error);
        });
    }, 1);  // Refresh every 1 millisecond
}

// Call this function on page load to start the refresh process
document.addEventListener("DOMContentLoaded", function () {
    refreshAuctionListEveryMillisecond();
});
