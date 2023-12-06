document.addEventListener('DOMContentLoaded', function() {
    var starInputs = document.querySelectorAll('.rate input');
    for (var i = 0; i < starInputs.length; i++) {
        starInputs[i].addEventListener('click', function(event) {
            event.preventDefault(); // This will prevent the default action of the input which is to jump to the top of the page
        });
    }
});

$(':radio').change(function() {
console.log('New star rating: ' + this.value);
});

