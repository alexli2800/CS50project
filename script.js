/* trying to prevent clicking the star buttons from scrolling back up to the top */
document.addEventListener('DOMContentLoaded', function() {
    var starInputs = document.querySelectorAll('.rate input');
    for (var i = 0; i < starInputs.length; i++) {
        starInputs[i].addEventListener('click', function(event.preventDefault()) {
            event.preventDefault(); // This will prevent the default action of the input which is to jump to the top of the page
        });
    }
    return false;
});

/* make the submit button redirect home */
function redirectToHome() {
    console.log("Redirecting to home");
    // Add any additional logic or validation here if needed

    // Redirect to the home page
    window.location.href = "/home.html"; // Replace "/" with the actual URL of your home page
    return false; // Prevent the form from submitting (if needed)
}

/* for star rating */
$(':radio').change(function() {
console.log('New star rating: ' + this.value);
});

