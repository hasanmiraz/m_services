const API_URL = 'http://127.0.0.1:8000';  // Change to your backend URL

// Function to add a new room
async function addRoom(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    // Get form values
    const roomType = document.getElementById('room-type').value;
    const pricePerNight = document.getElementById('price-per-night').value;
    const availabilityStatus = document.getElementById('availability-status').value;

    // Create room data object
    const roomData = {
        room_type: roomType,
        price_per_night: parseFloat(pricePerNight),
        availability_status: availabilityStatus
    };

    try {
        // Send POST request to add the room
        const response = await fetch(`${API_URL}/rooms/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(roomData)
        });

        const result = await response.json();

        if (response.status === 200 || response.status === 201) {
            document.getElementById('room-addition-result').innerHTML = `<p>Room added successfully!</p>`;
        } else {
            document.getElementById('room-addition-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('room-addition-result').innerHTML = `<p id="error">Error adding room.</p>`;
    }
}
