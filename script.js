document.querySelector('#rating1').addEventListener('click', function() {
    // update rating
});

document.querySelector('#submit').addEventListener('click', function() {
    // get text from textarea
    var review = document.querySelector('#review').value;
});

// For each radio button...rfw2
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
