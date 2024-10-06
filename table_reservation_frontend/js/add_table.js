const API_URL_TABLE = 'http://127.0.0.1:8001';  // Change to table reservation backend URL

// Function to add a new table
async function addTable(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    // Get form values
    const restaurantName = document.getElementById('restaurant-name').value;
    const capacity = document.getElementById('capacity').value;
    const availabilityStatus = document.getElementById('availability-status').value;

    // Create table data object
    const tableData = {
        restaurant_name: restaurantName,
        capacity: parseInt(capacity),
        availability_status: availabilityStatus
    };

    try {
        // Send POST request to add the table
        const response = await fetch(`${API_URL_TABLE}/tables/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tableData)
        });

        const result = await response.json();

        if (response.status === 200 || response.status === 201) {
            document.getElementById('table-addition-result').innerHTML = `<p>Table added successfully! Table ID: ${result.id}</p>`;
        } else {
            document.getElementById('table-addition-result').innerHTML = `<p id="error">Error: ${result.detail}</p>`;
        }

    } catch (error) {
        document.getElementById('table-addition-result').innerHTML = `<p id="error">Error adding table.</p>`;
    }
}
