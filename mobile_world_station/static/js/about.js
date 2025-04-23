document.addEventListener("DOMContentLoaded", function () {
    // Animate statistics counting
    const statNumbers = document.querySelectorAll(".stat-number");

    const animateCount = (element) => {
      const target = parseInt(element.dataset.count);
      const duration = 2000; // 2 seconds
      const step = target / (duration / 16); // 60fps

      let current = 0;
      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          clearInterval(timer);
          element.textContent = target;
        } else {
          element.textContent = Math.floor(current);
        }
      }, 16);
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );

    statNumbers.forEach((stat) => observer.observe(stat));

    // Testimonial slider
    const testimonials = document.querySelectorAll(".testimonial");
    const dots = document.querySelectorAll(".dot");
    let currentIndex = 0;

    function showTestimonial(index) {
      testimonials.forEach((testimonial) =>
        testimonial.classList.remove("active")
      );
      dots.forEach((dot) => dot.classList.remove("active"));

      testimonials[index].classList.add("active");
      dots[index].classList.add("active");
      currentIndex = index;
    }

    document.querySelector(".next-btn").addEventListener("click", () => {
      let nextIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(nextIndex);
    });

    document.querySelector(".prev-btn").addEventListener("click", () => {
      let prevIndex =
        (currentIndex - 1 + testimonials.length) % testimonials.length;
      showTestimonial(prevIndex);
    });

    dots.forEach((dot, index) => {
      dot.addEventListener("click", () => showTestimonial(index));
    });

    // Auto-rotate testimonials
    setInterval(() => {
      let nextIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(nextIndex);
    }, 5000);
  });