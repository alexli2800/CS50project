// To enable popups

document.getElementById('openPopup').addEventListener('click', function() {
    document.getElementById('popup').style.display = 'block';
});

document.getElementById('closePopup').addEventListener('click', function() {
    document.getElementById('popup').style.display = 'none';
});



// to grab reviews from user

document.querySelector('#rating1').addEventListener('click', function() {
    // update rating
});

document.querySelector('#submit').addEventListener('click', function() {
    // get text from text area
    var review = document.querySelector('#review').value;
});



// For each radio button...
document.querySelectorAll('.rating-button').forEach(function(button) {
    // Add an event listener that runs a function when the button is clicked
    button.addEventListener('click', function() {var clickedValue = parseInt(button.value);
        // In the function...
        // For each radio button...
        document.querySelectorAll('.rating-button').forEach(function(btn) {
            // If the button's value is less than or equal to the clicked button's value...
            if (parseInt(btn.value) <= clickedValue) {
                // Change the appearance of the button to make it look selected
                btn.classList.add('selected');
            } else {
                // Reset the appearance for buttons with a higher value
                btn.classList.remove('selected');
            }
        });
    });
});

// For each radio button...
// Add an event listener that updates the rating when the button is clicked
document.querySelectorAll('.rating input').forEach(function(button) {
button.addEventListener('click', function() {
    var ratingValue = button.value;
    // Update rating logic goes here
    console.log('Rating Clicked:', ratingValue);
});
});

// For the submit button... Add an event listener that gets the text from the textarea when the button is clicked
document.querySelector('#submit1').addEventListener('click', function() {
// Get text from textarea
var review = document.querySelector('#review1').value;
// Submit review logic goes here
console.log('Review Submitted:', review);
});

/* redirect user to home page after submit */

        function redirectToHome() {
            // Perform any form processing here if needed
            // e.g., sending data to a server using AJAX

            // Redirect to home.html
            window.location.href = "home.html";
            return false; // Prevent the form from submitting in the traditional way
        }
