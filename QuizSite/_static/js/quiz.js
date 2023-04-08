function toggleCircle(circleId, state) {
    var circle = document.getElementById(circleId);
    if (state === undefined) {
      circle.classList.toggle("active");
    } else {
      circle.classList.toggle("active", state);
    }
  }

  // Add event listeners to each circle
  var circles = document.querySelectorAll(".circle");
  circles.forEach(function(circle) {
    circle.addEventListener("click", function() {
      toggleCircle(circle.id);
    });
  });

  // Add event listeners to each toggle switch
  var toggles = document.querySelectorAll(".form-check-input");
  toggles.forEach(function(toggle) {
    toggle.addEventListener("change", function() {
      var circleId = "circle" + toggle.id.slice(-1);
      toggleCircle(circleId, toggle.checked);
    });
  });
