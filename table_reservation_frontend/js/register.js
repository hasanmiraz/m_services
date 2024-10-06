const API_URL = 'http://127.0.0.1:8001';  // Change to backend URL

// Function to register a new user
async function registerUser(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    // Get form values
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const phoneNumber = document.getElementById('phone-number').value;

    // Create user data object
    const userData = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        phone_number: phoneNumber
    };

    try {
        // Send POST request to create the user
        const response = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const result = await response.json();                     

        if (response.status === 200) {
            document.getElementById('registration-result').innerHTML = `<p>User registered successfully!</p>`;
        } else {
            document.getElementById('registration-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('registration-result').innerHTML = `<p id="error">Error registering user.</p>`;
    }
}
