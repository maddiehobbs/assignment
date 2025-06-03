document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  document.querySelectorAll('[data-dismiss="alert"]').forEach((button) => {
    button.addEventListener("click", function () {
      const alert = this.parentElement;
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    });
  });
});
function setActive(element) {
  // Removes active class
  document.querySelectorAll(".tab-link").forEach((link) => {
    link.classList.remove("active");
  });
  // Adds active class
  element.classList.add("active");
}
function confirmDelete() {
  return confirm(
    "Are you sure you want to delete this ticket? This action cannot be undone."
  );
}
