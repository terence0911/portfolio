(function () {
  const yearEl = document.getElementById("year");
  const clockEl = document.getElementById("clock");

  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  function updateClock() {
    if (!clockEl) return;
    const now = new Date();
    const h = String(now.getHours()).padStart(2, "0");
    const m = String(now.getMinutes()).padStart(2, "0");
    const s = String(now.getSeconds()).padStart(2, "0");
    clockEl.textContent = `${h}:${m}:${s}`;
  }

  updateClock();
  setInterval(updateClock, 1000);
})();
