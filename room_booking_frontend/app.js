const API_URL = 'http://127.0.0.1:8000'; // Change to your backend URL

// Get all available rooms and display them
async function getRooms() {
    const response = await fetch(`${API_URL}/rooms/`);
    const rooms = await response.json();

    const roomsSection = document.getElementById('rooms');
    roomsSection.innerHTML = '';  // Clear previous content

    rooms.forEach(room => {
        const roomDiv = document.createElement('div');
        roomDiv.classList.add('room');
        roomDiv.innerHTML = `
            <h3>Room ${room.id}</h3>
            <p>Type: ${room.room_type}</p>
            <p>Price per night: $${room.price_per_night}</p>
            <p>Status: ${room.availability_status}</p>
        `;
        roomsSection.appendChild(roomDiv);
    });
}

// Get user info by user ID
async function getUser() {
    const userId = document.getElementById('user-id').value;

    try {
        const response = await fetch(`${API_URL}/users/${userId}`);
        const user = await response.json();

        const userInfoDiv = document.getElementById('user-info');
        userInfoDiv.innerHTML = `
            <p><strong>Name:</strong> ${user.first_name} ${user.last_name}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Phone:</strong> ${user.phone_number}</p>
        `;
    } catch (error) {
        document.getElementById('user-info').innerHTML = `<p id="error">User not found!</p>`;
    }
}

// Book a room
async function bookRoom() {
    const userId = document.getElementById('user-id-booking').value;
    const roomId = document.getElementById('room-id-booking').value;
    const checkIn = document.getElementById('check-in').value;
    const checkOut = document.getElementById('check-out').value;
    const totalPrice = document.getElementById('total-price').value;

    const bookingData = {
        user_id: userId,
        room_id: roomId,
        check_in: checkIn,
        check_out: checkOut,
        total_price: totalPrice
    };

    try {
        const response = await fetch(`${API_URL}/bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });

        const result = await response.json();

        document.getElementById('booking-result').innerHTML = `<p>Room booked successfully! Booking ID: ${result.id}</p>`;
        getRooms();  // Refresh room list
    } catch (error) {
        document.getElementById('booking-result').innerHTML = `<p id="error">Failed to book room.</p>`;
    }
}

// Load rooms on page load
document.addEventListener('DOMContentLoaded', getRooms);
