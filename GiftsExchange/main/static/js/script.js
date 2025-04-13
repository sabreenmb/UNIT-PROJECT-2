// Function to show all alerts in sequence
function showAlerts() {
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length === 0) return; // Exit if no alerts exist

    let currentAlertIndex = 0;

    function displayNextAlert() {
        // Hide all alerts
        alerts.forEach(alert => alert.style.display = 'none');

        if (currentAlertIndex < alerts.length) {
            // Show the current alert
            alerts[currentAlertIndex].style.display = 'block';

            // Automatically hide the alert after 4 seconds
            setTimeout(() => {
                hideAlert(alerts[currentAlertIndex]); // Hide the current alert
                currentAlertIndex++; // Move to the next alert
                displayNextAlert(); // Show the next alert
            }, 4000); // Adjust the duration as needed
        }
    }

    displayNextAlert(); // Start displaying alerts
}

function hideAlert(alert) {
    alert.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    // Call the function to show alerts when the page loads
    showAlerts(); 
});


function validateBudgetAndDate(event) {
    // Get the values of the min and max budget inputs
    const minBudget = parseFloat(document.getElementById('event_min_budget').value);
    const maxBudget = parseFloat(document.getElementById('event_max_budget').value);

    // Check if min budget is greater than max budget
    if (minBudget > maxBudget) {
        event.preventDefault(); 
        alert("Minimum Budget cannot be greater than Maximum Budget.");
        return; 
    }

    // Get the selected event date
    const selectedDate = new Date(document.getElementById('event_date').value);
    const today = new Date();
    
    today.setHours(0, 0, 0, 0);
    
    // Check if the selected date is in the past
    if (selectedDate < today) {
        event.preventDefault(); 
        alert("The selected date cannot be in the past.");
    }
}
