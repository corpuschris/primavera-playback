function setStatus(perfId, status) {
    const container = document.querySelector(`[data-performance-id="${perfId}"]`);
    const ratingDropdown = document.getElementById(`rating-${perfId}`);
    if (!container) return;

    const buttons = container.querySelectorAll("button");
    let alreadySelected = false;

    buttons.forEach(btn => {
        const icon = btn.textContent.trim();
        if (
            (icon.includes("✅") && status === "watched" && btn.classList.contains("selected")) ||
            (icon.includes("👀") && status === "glanced" && btn.classList.contains("selected")) ||
            (icon.includes("❌") && status === "skipped" && btn.classList.contains("selected"))
        ) {
            alreadySelected = true;
        }
        btn.classList.remove("selected");
    });

    if (alreadySelected) {
        ratingDropdown.style.display = "none";
        setRating(perfId, "");
        fetch(`/api/experience/${perfId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ viewing_status: "" })
        });
        return;
    }

    const buttonToSelect = {
        watched: "✅",
        glanced: "👀",
        skipped: "❌"
    }[status];

    buttons.forEach(btn => {
        if (btn.textContent.includes(buttonToSelect)) {
            btn.classList.add("selected");
        }
    });

    if (status === "watched") {
        ratingDropdown.style.display = "inline";
    } else {
        ratingDropdown.style.display = "none";
        setRating(perfId, "");
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
    fetch(`/api/experience/${perfId}/rating`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ rating: rating })
    });
}

function applyFilters() {
    const stage = document.getElementById("stageFilter").value;
    const day = document.getElementById("dayFilter").value;
    const status = document.getElementById("statusFilter").value;

    const performances = document.querySelectorAll(".performance");
    performances.forEach(perf => {
        const perfId = perf.querySelector(".experience-buttons").dataset.performanceId;
        const data = userExperience[perfId] || {};
        const userStatus = data.status;

        const matchesStage = stage === "all" || perf.dataset.stage === stage;
        const matchesDay = day === "all" || perf.dataset.day === day;
        const matchesStatus = status === "all" || userStatus === status;

        if (matchesStage && matchesDay && matchesStatus) {
            perf.style.display = "block";
        } else {
            perf.style.display = "none";
        }
    });
}

window.onload = function () {
    for (const [perfId, data] of Object.entries(userExperience)) {
        const container = document.querySelector(`[data-performance-id="${perfId}"]`);
        if (!container) continue;

        const buttons = container.querySelectorAll("button");
        buttons.forEach(btn => {
            if (btn.textContent.includes("✅") && data.status === "watched") btn.classList.add("selected");
            if (btn.textContent.includes("👀") && data.status === "glanced") btn.classList.add("selected");
            if (btn.textContent.includes("❌") && data.status === "skipped") btn.classList.add("selected");
        });

        const ratingDropdown = document.getElementById(`rating-${perfId}`);
        if (data.status === "watched") {
            ratingDropdown.style.display = "inline";
            ratingDropdown.value = data.rating || "";
        }
    }

    document.getElementById("applyFilters").addEventListener("click", applyFilters);
};
