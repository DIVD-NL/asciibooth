function three() {
	document.getElementById("overlay3").classList.remove("hidden");
	setTimeout(two, 1000);
}

function two() {
	document.getElementById("overlay3").classList.add("hidden");
	document.getElementById("overlay2").classList.remove("hidden");
	setTimeout(one, 1000);
}

function one() {
	document.getElementById("overlay2").classList.add("hidden");
	document.getElementById("overlay1").classList.remove("hidden");
	setTimeout(go, 500);
}

function go() {
	document.getElementById("capture-frm").submit();
}


// Get the button by its ID
var button = document.getElementById('capture-btn');

// Add a click event listener to the button
button.addEventListener('click', function(event) {
	// Prevent the default action (if any)
	event.preventDefault();

	// Custom logic for the button click
	console.log('Button clicked, default event prevented.');

	three();

});


