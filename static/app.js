const REFRESH_MS = 3000;

function severityBadge(sev) {
  return `<span class="sev ${sev}"><span class="sev-dot"></span>${sev}</span>`;
}

async function refreshEvents() {
  try {
    const res = await fetch("/api/events");
    const events = await res.json();

    const body = document.getElementById("event-body");

    if (events.length === 0) {
      body.innerHTML = `<tr><td colspan="6" class="empty-state">هنوز رویدادی ثبت نشده — سیستم در حال دیده‌بانیه.</td></tr>`;
    } else {
      body.innerHTML = events.map(e => `
        <tr>
          <td class="mono muted">${e.timestamp}</td>
          <td>${e.source}</td>
          <td class="mono">${e.event_type}</td>
          <td class="mono">${e.src_ip ?? "—"}</td>
          <td>${severityBadge(e.severity)}</td>
          <td class="muted">${e.details ?? ""}</td>
        </tr>
      `).join("");
    }

    document.getElementById("last-updated").textContent =
      "به‌روزرسانی شده: " + new Date().toLocaleTimeString();

  } catch (err) {
    document.getElementById("last-updated").textContent = "قطع اتصال به سرور";
  }
}

async function refreshStats() {
  try {
    const res = await fetch("/api/stats");
    const stats = await res.json();
    document.getElementById("stat-total").textContent = stats.total;
    document.getElementById("stat-high").textContent = stats.high;
    document.getElementById("stat-sources").textContent = stats.sources;
  } catch (err) {
    // بی‌خیال، دور بعدی دوباره تلاش میشه
  }
}

function tick() {
  refreshEvents();
  refreshStats();
}

tick();
setInterval(tick, REFRESH_MS);
