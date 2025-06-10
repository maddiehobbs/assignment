document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Manual dismiss
  document.querySelectorAll('[data-dismiss="alert"]').forEach((button) => {
    button.addEventListener("click", function () {
      const alert = this.parentElement;
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    });
  });

  // Sets default tab to view
  const defaultTab = document.querySelector('a[href="#view"]');
  if (defaultTab) {
    setActive(defaultTab);
  }

  // Form for selecting a ticket to update
  const ticketSelectForm = document.getElementById("ticketSelectForm");
  if (ticketSelectForm) {
    ticketSelectForm.addEventListener("submit", handleTicketSelect);
  }

  // Form for updating a ticket information
  const updateForm = document.getElementById("updateForm");
  if (updateForm) {
    updateForm.addEventListener("submit", handleTicketUpdate);
  }
});

function setActive(element) {
  // Removes active class from all tabs
  document.querySelectorAll(".tab-link").forEach((link) => {
    link.classList.remove("active");
  });

  // Adds active class to selectd tab
  element.classList.add("active");

  // Hides all tab content
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.style.display = "none";
  });

  // Shows active tab content
  const tabId = element.getAttribute("href").substring(1);
  document.getElementById(tabId).style.display = "block";
}

function confirmDelete() {
  return confirm(
    "Are you sure you want to delete this ticket? This action cannot be undone."
  );
}

function handleTicketSelect(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);

  fetch("/tickets/update", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.text())
    .then((html) => {
      // Replaces current page content
      document.open();
      document.write(html);
      document.close();
      // Sets update tab to active
      setActive(document.querySelector('a[href="#update"]'));
    })
    .catch((error) => console.error("Error:", error));
}

function handleTicketUpdate(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);

  fetch("/tickets/update", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.text())
    .then((html) => {
      // Replaces current page content
      document.open();
      document.write(html);
      document.close();
      // Swithces to view tab to be active tab
      setTimeout(() => {
        setActive(document.querySelector('a[href="#view"]'));
      }, 100);
    })
    .catch((error) => console.error("Error:", error));
}

function cancelUpdate() {
  fetch("/tickets/update")
    .then((response) => response.text())
    .then((html) => {
      // Replaces current page content
      document.open();
      document.write(html);
      document.close();
      // Sets udate tab to active
      setActive(document.querySelector('a[href="#update"]'));
    })
    .catch((error) => console.error("Error:", error));
}
