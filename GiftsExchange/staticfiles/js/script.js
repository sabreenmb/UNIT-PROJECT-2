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
