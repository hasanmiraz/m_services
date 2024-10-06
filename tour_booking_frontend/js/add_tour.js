const API_URL_TOUR = 'http://127.0.0.1:8002';  // Change to your tour booking backend URL

// Function to add a new tour
async function addTour(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    // Get form values
    const tourName = document.getElementById('tour-name').value;
    const tourDescription = document.getElementById('tour-description').value;
    const tourPrice = document.getElementById('tour-price').value;
    const availabilityStatus = document.getElementById('availability-status').value;

    // Create tour data object
    const tourData = {
        name: tourName,
        description: tourDescription,
        price_per_person: parseFloat(tourPrice),
        availability_status: availabilityStatus
    };

    try {
        // Send POST request to add the tour
        const response = await fetch(`${API_URL_TOUR}/tours/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tourData)
        });

        const result = await response.json();

        if (response.status === 200 || response.status === 201) {
            document.getElementById('tour-addition-result').innerHTML = `<p>Tour added successfully! Tour ID: ${result.id}</p>`;
        } else {
            document.getElementById('tour-addition-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('tour-addition-result').innerHTML = `<p id="error">Error adding tour.</p>`;
    }
}
