const SECRET_TOKEN = "mysecrettoken"; // Same token as Event Bus
const agentName = "DevOpsAgent"; // You can change based on agent

async function fetchEvents() {
    try {
        const response = await fetch(`http://localhost:5000/get_events/${agentName}`, {
            method: 'GET',
            headers: {
                "Authorization": SECRET_TOKEN
            }
        });

        if (!response.ok) {
            console.error("Failed to fetch events");
            return;
        }

        const events = await response.json();
        updateTable(events);

    } catch (error) {
        console.error("Error fetching events:", error);
    }
}

function updateTable(events) {
    const tableBody = document.querySelector("#eventsTable tbody");
    tableBody.innerHTML = ""; // Clear previous rows

    events.forEach(event => {
        const row = document.createElement("tr");

        const fromCell = document.createElement("td");
        fromCell.textContent = event.from;
        row.appendChild(fromCell);

        const toCell = document.createElement("td");
        toCell.textContent = event.to;
        row.appendChild(toCell);

        const messageCell = document.createElement("td");
        messageCell.textContent = event.message;
        row.appendChild(messageCell);

        tableBody.appendChild(row);
    });
}

// Fetch events every 5 seconds
setInterval(fetchEvents, 5000);

// Initial load
fetchEvents();
