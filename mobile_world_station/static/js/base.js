// Mobile menu toggle
document
.getElementById("mobileMenuBtn")
.addEventListener("click", function () {
  const nav = document.getElementById("mainNav");
  nav.style.display = nav.style.display === "none" ? "block" : "none";
});



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