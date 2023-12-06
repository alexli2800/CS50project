/* redirect user to home page after submit */

function redirectToHome() {
    // Perform any form processing here if needed
    // e.g., sending data to a server using AJAX

    // Redirect to home.html
    window.location.href = "home.html";
    return false; // Prevent the form from submitting in the traditional way
}
