document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));
});

function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => toast("UPI link copied")).catch(() => fallbackCopy(text));
  } else fallbackCopy(text);
}
function fallbackCopy(text) {
  const input = document.createElement("textarea");
  input.value = text; input.style.position = "fixed"; input.style.opacity = "0";
  document.body.appendChild(input); input.select();
  try { document.execCommand("copy"); toast("UPI link copied"); } catch (_) { toast("Copy failed — select the link manually"); }
  input.remove();
}
function toast(message) {
  let el = document.querySelector(".toast-message");
  if (!el) { el = document.createElement("div"); el.className = "toast-message"; document.body.appendChild(el); }
  el.textContent = message; el.classList.add("toast-show");
  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(() => el.classList.remove("toast-show"), 2400);
}
window.setupInvoiceCalculator = function () {
  const subtotal = document.getElementById("subtotal");
  const gstRate = document.getElementById("gst-rate");
  const tdsRate = document.getElementById("tds-rate");
  if (!subtotal || !gstRate || !tdsRate) return;
  const fmt = value => "₹" + value.toLocaleString("en-IN", {minimumFractionDigits: 2, maximumFractionDigits: 2});
  const update = () => {
    const base = Math.max(0, Number(subtotal.value) || 0);
    const gst = base * (Number(gstRate.value) || 0) / 100;
    const tds = base * (Number(tdsRate.value) || 0) / 100;
    document.getElementById("calc-gst").textContent = fmt(gst);
    document.getElementById("calc-total").textContent = fmt(base + gst);
    document.getElementById("calc-tds").textContent = fmt(tds);
    document.getElementById("calc-net").textContent = fmt(base + gst - tds);
  };
  [subtotal, gstRate, tdsRate].forEach(el => el.addEventListener("input", update));
  update();
};
