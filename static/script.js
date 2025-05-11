function setStatus(perfId, status) {
    console.log("Set status for", perfId, status);

    // Show rating dropdown only if "watched"
    const ratingDropdown = document.getElementById(`rating-${perfId}`);
    if (status === "watched") {
        ratingDropdown.style.display = "inline";
    } else {
        ratingDropdown.style.display = "none";
        setRating(perfId, ""); // Clear rating if not watched
    }

    fetch(`/api/experience/${perfId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ viewing_status: status })
    });
}

function setRating(perfId, rating) {
    console.log("Set rating for", perfId, rating);

    fetch(`/api/experience/${perfId}/rating`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ rating: rating })
    });
}
