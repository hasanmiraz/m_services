const API_URL_TABLE = 'http://127.0.0.1:8001';  // Change to your table reservation backend URL

// Load available tables when the page loads
async function loadTables() {
    const response = await fetch(`${API_URL_TABLE}/tables/`);
    const tables = await response.json();

    const tableSelect = document.getElementById('table-select');
    tables.forEach(table => {
        if (table.availability_status === 'available') {
            // Populate only available tables in the dropdown
            const option = document.createElement('option');
            option.value = table.id;
            option.text = `Table for ${table.capacity} (Available)`;
            tableSelect.appendChild(option);
        }
    });
}

// Book a table function
async function bookTable(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    const tableId = document.getElementById('table-select').value;
    const phoneNumber = document.getElementById('phone-number').value;
    const reservationTime = document.getElementById('reservation-time').value;

    // Fetch the user based on phone number
    const userResponse = await fetch(`${API_URL_TABLE}/users/phone/${phoneNumber}`);
    const user = await userResponse.json();

    if (userResponse.status === 404) {
        document.getElementById('table-booking-result').innerHTML = `
            <p id="error">User not found! Please <a href="register.html">register</a>.</p>
        `;
        return;
    }

    // Create booking data
    const bookingData = {
        user_id: user.id,
        table_id: parseInt(tableId),
        reservation_time: reservationTime
    };

    // Send POST request to book the table
    try {
        const response = await fetch(`${API_URL_TABLE}/table-reservations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });

        const result = await response.json();

        if (response.status === 200 || response.status === 201) {
            document.getElementById('table-booking-result').innerHTML = `<p>Table booked successfully! Booking ID: ${result.id}</p>`;
        } else {
            document.getElementById('table-booking-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('table-booking-result').innerHTML = `<p id="error">Error booking table.</p>`;
    }
}

// Load tables when the page loads
document.addEventListener('DOMContentLoaded', loadTables);
