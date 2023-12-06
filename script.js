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
