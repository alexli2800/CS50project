/* trying to prevent clicking the star buttons from scrolling back up to the top */
document.addEventListener('DOMContentLoaded', function() {
    var starInputs = document.querySelectorAll('.rate input');
    for (var i = 0; i < starInputs.length; i++) {
        starInputs[i].addEventListener('click', function(event.preventDefault()) {
            event.preventDefault(); // This will prevent jump to the top of the page
        });
    }
    return false;
});

/* make the submit button redirect home */
function redirectToHome() {
    console.log("Redirecting to home");

    // Redirect to the home page
    window.location.href = "/home.html";
    return false;
}

/* for star rating */
$(':radio').change(function() {
    console.log('New star rating: ' + this.value);
});
