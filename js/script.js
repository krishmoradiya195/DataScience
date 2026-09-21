// --- Contact form ---
const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = Object.fromEntries(new FormData(form).entries());
    status.textContent = "Sending...";
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      status.textContent = data.message || "Sent.";
      if (res.ok) form.reset();
    } catch (err) {
      status.textContent = "Something went wrong. Please try again.";
    }
  });
}

// --- Anonymous per-visitor page-view tracking ---
// Generates a stable id per browser (stored in localStorage) so that,
// once Supabase is configured on the backend, you can see usage broken
// down by individual visitor rather than just total page views.
(function track() {
  try {
    let visitorId = localStorage.getItem("ds_visitor_id");
    if (!visitorId) {
      visitorId = crypto.randomUUID();
      localStorage.setItem("ds_visitor_id", visitorId);
    }
    fetch("/api/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ visitor_id: visitorId, page: window.location.pathname }),
      keepalive: true,
    }).catch(() => {});
  } catch (e) {
    // localStorage may be unavailable (private browsing, etc.) - fail silently
  }
})();
