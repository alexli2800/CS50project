// star rating

 // Select all elements with the "i" tag and store them in a NodeList called "stars"
 const stars = document.querySelectorAll(".stars i");
 // Loop through the "stars" NodeList
 stars.forEach((star, index1) => {
   // Add an event listener that runs a function when the "click" event is triggered
   star.addEventListener("click", () => {
     // Loop through the "stars" NodeList Again
     stars.forEach((star, index2) => {
       // Add the "active" class to the clicked star and any stars with a lower index
       // and remove the "active" class from any stars with a higher index
       index1 >= index2 ? star.classList.add("active") : star.classList.remove("active");
     });
   });
 });

/* redirect user to home page after submit */

        function redirectToHome() {
            // Perform any form processing here if needed
            // e.g., sending data to a server using AJAX

            // Redirect to home.html
            window.location.href = "home.html";
            return false; // Prevent the form from submitting in the traditional way
        }
