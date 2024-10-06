const API_URL = 'http://127.0.0.1:8000';  // Change to backend URL

let roomsData = {};  // To store room information with prices

// Load available rooms when the page loads
async function loadRooms() {
    const response = await fetch(`${API_URL}/rooms/`);
    const rooms = await response.json();

    const roomSelect = document.getElementById('room-select');
    rooms.forEach(room => {
        // Store room price with the room ID for later use
        roomsData[room.id] = room.price_per_night;

        // Populate the room dropdown
        const option = document.createElement('option');
        option.value = room.id;
        option.text = `${room.room_type} ($${room.price_per_night})`;
        roomSelect.appendChild(option);
    });
}

// Calculate the total price based on the room price and duration
function calculateTotalPrice() {
    const roomId = document.getElementById('room-select').value;
    const checkIn = document.getElementById('check-in').value;
    const checkOut = document.getElementById('check-out').value;

    if (!roomId || !checkIn || !checkOut) {
        return;  // Exit if required fields are not selected
    }

    const pricePerNight = roomsData[roomId];

    // Calculate the number of days between check-in and check-out
    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);
    const diffTime = checkOutDate - checkInDate;
    const numberOfDays = diffTime / (1000 * 60 * 60 * 24);  // Convert time difference to days

    // Calculate the total price and update the input field
    const totalPrice = pricePerNight * numberOfDays;
    document.getElementById('total-price').value = `$${totalPrice.toFixed(2)}`;
}

// Book a room function
async function bookRoom(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    const roomId = document.getElementById('room-select').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const checkIn = document.getElementById('check-in').value;
    const checkOut = document.getElementById('check-out').value;
    const totalPrice = document.getElementById('total-price').value.replace('$', '');

    // Fetch the user based on phone number
    const userResponse = await fetch(`${API_URL}/users/phone/${phoneNumber}`);
    const user = await userResponse.json();

    if (userResponse.status === 404) {
        document.getElementById('room-booking-result').innerHTML = `
            <p id="error">User not found! Please <a href="register.html">register</a>.</p>
        `;
        return;
    }

    // Create booking data
    const bookingData = {
        user_id: user.id,
        room_id: parseInt(roomId),
        check_in: checkIn,
        check_out: checkOut,
        total_price: parseFloat(totalPrice)
    };

    // Send POST request to book the room
    try {
        const response = await fetch(`${API_URL}/bookings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });

        const result = await response.json();

        if (response.status === 200 || response.status === 201) {
            document.getElementById('room-booking-result').innerHTML = `<p>Room booked successfully! Booking ID: ${result.id}</p>`;
        } else {
            document.getElementById('room-booking-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('room-booking-result').innerHTML = `<p id="error">Error booking room.</p>`;
    }
}

// Load rooms when the page loads
document.addEventListener('DOMContentLoaded', loadRooms);
