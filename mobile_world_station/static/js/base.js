// Mobile menu toggle
document
.getElementById("mobileMenuBtn")
.addEventListener("click", function () {
  const nav = document.getElementById("mainNav");
  nav.style.display = nav.style.display === "none" ? "block" : "none";
});

function handleLogout(event) {
event.preventDefault();
if (confirm("Are you sure you want to logout?")) {
  // Create a hidden form and submit it
  const form = document.createElement("form");
  form.method = "POST";
  form.action = '{% url "logout" %}';

  const csrf = document.createElement("input");
  csrf.type = "hidden";
  csrf.name = "csrfmiddlewaretoken";
  csrf.value = "{{ csrf_token }}";

  form.appendChild(csrf);
  document.body.appendChild(form);
  form.submit();
}
}

// Hide mobile menu if screen is resized to desktop size
window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
      document.getElementById("mainNav").style.display = "block";
      document.getElementById("mobileMenuBtn").style.display = "none";
    } else {
      document.getElementById("mainNav").style.display = "none";
      document.getElementById("mobileMenuBtn").style.display = "block";
    }
  });