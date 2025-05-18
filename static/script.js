// script.js

function setStatus(performanceId, status) {
    fetch(`/api/experience/${performanceId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ viewing_status: status })
    })
    .then(response => response.json())
    .then(() => {
        updateBubbleUI(performanceId, status, experienceData[performanceId]?.rating || null);
        experienceData[performanceId] = experienceData[performanceId] || {};
        experienceData[performanceId].status = status;
        if (status !== "watched") {
            experienceData[performanceId].rating = null;
        }
    });
}

function setRating(performanceId, rating) {
    fetch(`/api/experience/${performanceId}/rating`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(() => {
        updateBubbleUI(performanceId, "watched", rating);
        experienceData[performanceId] = experienceData[performanceId] || {};
        experienceData[performanceId].rating = rating;
    });
}

function updateBubbleUI(performanceId, status, rating) {
    const bubble = document.querySelector(`[data-performance-id='${performanceId}']`);
    if (!bubble) return;

    bubble.classList.remove("bright", "purple", "red", "good", "meh", "default", "tiny", "small", "medium", "large", "huge");

    let size = "tiny";
    let color = "default";

    if (status === "watched") {
        size = "medium";
        color = "bright";
        bubble.querySelector("select").style.display = "block";

        if (rating === "good") {
            bubble.classList.add("huge", "good");
        } else if (rating === "okay") {
            bubble.classList.add("medium");
        } else if (rating === "bad") {
            bubble.classList.add("medium", "meh");
        }
    } else if (status === "glanced") {
        size = "small";
        color = "purple";
        bubble.querySelector("select").style.display = "none";
    } else if (status === "skipped") {
        size = "tiny";
        color = "red";
        bubble.querySelector("select").style.display = "none";
    } else {
        bubble.querySelector("select").style.display = "none";
    }

    bubble.classList.add(color, size);

    // Highlight the selected button
    bubble.querySelectorAll("button").forEach(button => {
        button.classList.remove("selected");
        if (button.dataset.status === status) {
            button.classList.add("selected");
        }
    });

    if (rating) {
        const select = bubble.querySelector("select");
        if (select) {
            select.value = rating;
        }
    }
}

function clearAllStatuses(year) {
    fetch(`/api/clear_all/${year}`, {
        method: "POST"
    })
    .then(response => response.json())
    .then(() => {
        document.querySelectorAll(".artist-bubble").forEach(bubble => {
            const id = bubble.dataset.performanceId;
            bubble.classList.remove("bright", "purple", "red", "good", "meh", "default", "tiny", "small", "medium", "large", "huge");
            bubble.classList.add("default", "tiny");
            const select = bubble.querySelector("select");
            if (select) {
                select.style.display = "none";
                select.value = "";
            }
            bubble.querySelectorAll("button").forEach(btn => btn.classList.remove("selected"));
            delete experienceData[id];
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // Apply initial experience data
    Object.entries(experienceData).forEach(([id, exp]) => {
        updateBubbleUI(id, exp.status, exp.rating);
    });

    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase();
            document.querySelectorAll(".artist-bubble").forEach(bubble => {
                const name = bubble.dataset.artist;
                bubble.style.display = name.includes(query) ? "flex" : "none";
            });
        });
    }

    const clearBtn = document.getElementById("clearAllBtn");
    if (clearBtn) {
        const year = clearBtn.dataset.year;
        clearBtn.addEventListener("click", () => clearAllStatuses(year));
    }
});
