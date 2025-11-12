"""Yemen site selector prototype rendered inside Streamlit."""

from __future__ import annotations

from streamlit.components.v1 import html


def render_yemen_site_selector() -> None:
    """Render a lightweight three-panel selector for Yemen candidate sites."""

    html(
        """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Yemen Site Selector</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    />
    <script
      src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    ></script>
    <style>
      :root {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #050a16;
        color: #e2e8f0;
      }
      *, *::before, *::after {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        height: 100vh;
        overflow: hidden;
        background: radial-gradient(circle at 12% -8%, rgba(91, 99, 244, 0.35), transparent 55%);
      }
      .dashboard {
        display: grid;
        grid-template-columns: 340px minmax(560px, 1fr) 320px;
        gap: 1.5rem;
        padding: 1.5rem 1.75rem;
        height: 100%;
      }
      .panel {
        display: flex;
        flex-direction: column;
        border-radius: 22px;
        padding: 1.25rem 1.5rem;
        background: rgba(16, 24, 52, 0.9);
        backdrop-filter: blur(14px);
        box-shadow: 0 28px 40px -28px rgba(3, 7, 18, 0.72);
        min-height: 0;
      }
      .panel header h2 {
        margin: 0;
        font-size: 1.3rem;
      }
      .panel-subtitle {
        margin: 0.3rem 0 0;
        font-size: 0.9rem;
        color: #94b8ff;
      }
      .panel--list {
        background: linear-gradient(186deg, rgba(32, 49, 132, 0.95), rgba(18, 30, 90, 0.94));
        color: #f5f9ff;
        overflow-y: auto;
      }
      .panel--map {
        padding: 1.3rem;
      }
      .panel--detail {
        background: rgba(7, 11, 22, 0.94);
        overflow-y: auto;
      }
      .search {
        margin-top: 1.1rem;
      }
      .search input {
        width: 100%;
        padding: 0.6rem 0.9rem;
        font-size: 0.95rem;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.1);
        color: inherit;
        outline: none;
      }
      .site-list {
        display: grid;
        gap: 0.7rem;
        margin-top: 1.2rem;
      }
      .site-card {
        border-radius: 16px;
        padding: 0.7rem 0.85rem;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid transparent;
        transition: transform 0.15s ease, border 0.15s ease;
        cursor: pointer;
        display: grid;
        gap: 0.25rem;
      }
      .site-card[data-selected="true"] {
        border-color: rgba(255, 255, 255, 0.45);
        transform: translateY(-2px);
      }
      .site-card h3 {
        margin: 0;
        font-size: 0.98rem;
      }
      .site-card span {
        font-size: 0.82rem;
        color: rgba(226, 232, 240, 0.75);
      }
      .map-placeholder {
        flex: 1;
        position: relative;
        border-radius: 20px;
        background: radial-gradient(circle at center, rgba(26, 58, 138, 0.9), rgba(7, 10, 22, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(226, 232, 240, 0.45);
        font-size: 1rem;
        overflow: hidden;
      }
      .map-placeholder #leaflet-map {
        position: absolute;
        inset: 0;
        z-index: 0;
      }
      .map-overlay {
        position: absolute;
        left: 1.4rem;
        top: 1.4rem;
        background: rgba(8, 13, 30, 0.78);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        padding: 0.9rem 1.15rem;
        min-width: 230px;
        display: grid;
        gap: 0.35rem;
        color: #f8fafc;
      }
      .map-overlay span {
        font-size: 0.75rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: rgba(148, 163, 184, 0.85);
      }
      .map-badge {
        position: absolute;
        bottom: 1.3rem;
        left: 1.4rem;
        background: rgba(91, 99, 244, 0.18);
        border: 1px solid rgba(91, 99, 244, 0.45);
        border-radius: 12px;
        padding: 0.45rem 0.75rem;
        font-size: 0.85rem;
        color: #cbd5ff;
      }
      .map-coord {
        position: absolute;
        right: 1.4rem;
        bottom: 1.3rem;
        background: rgba(15, 23, 42, 0.88);
        border-radius: 12px;
        padding: 0.5rem 0.75rem;
        font-size: 0.82rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
        color: rgba(226, 232, 240, 0.9);
      }
      .detail-card {
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1rem;
        margin-top: 1rem;
      }
      .detail-card h3 {
        margin: 0;
        font-size: 0.92rem;
        color: rgba(186, 201, 255, 0.85);
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      .detail-card p {
        margin: 0.3rem 0 0;
        font-size: 0.95rem;
        color: rgba(226, 232, 240, 0.88);
      }
      .metrics {
        margin-top: 0.8rem;
        display: grid;
        gap: 0.55rem;
      }
      .metric {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: rgba(226, 232, 240, 0.8);
      }
      .metric span {
        color: rgba(148, 163, 184, 0.85);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.73rem;
      }
    </style>
  </head>
  <body>
    <div class="dashboard">
      <section class="panel panel--list">
        <header>
          <h2>Candidate Sites • Yemen</h2>
          <p class="panel-subtitle">
            Choose a location to update the map and context panel.
          </p>
        </header>
        <div class="search">
          <input type="text" id="search" placeholder="Filter by name or priority…" />
        </div>
        <div class="site-list" id="site-list"></div>
      </section>

      <section class="panel panel--map">
        <header>
          <div>
            <h2>Opportunity Map</h2>
            <p class="panel-subtitle">Interactive map with coordinate overlay.</p>
          </div>
          <button class="btn btn-outline" id="reset-view">Reset view</button>
        </header>
        <div class="map-placeholder">
          <div id="leaflet-map"></div>
          <div class="map-overlay" id="overlay">
            <span>Active site</span>
            <strong id="overlay-name">Sana'a Central Hospital</strong>
            <p id="overlay-note">Anchor load • Regional hospital & cold chain hub</p>
          </div>
          <div class="map-badge" id="overlay-priority">Priority • Anchor load</div>
          <div class="map-coord" id="overlay-coord">15.3694°N, 44.1910°E</div>
        </div>
      </section>

      <section class="panel panel--detail" id="detail-panel">
        <header>
          <h2 id="detail-title">Sana'a Central Hospital</h2>
          <p class="panel-subtitle" id="detail-subtitle">
            Anchor load • Critical health services
          </p>
        </header>
        <div class="detail-card">
          <h3>Context</h3>
          <p id="detail-context">
            Regional referral hospital with critical cold chain services disrupted by frequent outages and diesel shortages.
          </p>
        </div>
        <div class="detail-card">
          <h3>Key metrics</h3>
          <div class="metrics" id="detail-metrics"></div>
        </div>
        <div class="detail-card">
          <h3>Notes</h3>
          <p id="detail-notes">
            Prioritize hybrid PV + storage to secure surgical theatres and ICU operations. Coordinate with grid utility for feeder upgrades.
          </p>
        </div>
      </section>
    </div>

    <script>
      const sites = [
        {
          name: "Sana'a Central Hospital",
          governorate: "Sana'a",
          priority: "Anchor load",
          lat: 15.3694,
          lon: 44.1910,
          overview: "Anchor load • Regional hospital & cold chain hub",
          context: "Regional referral hospital with critical cold chain services disrupted by frequent outages and diesel shortages.",
          metrics: [
            { label: "Daily demand", value: "1.8 MWh" },
            { label: "Population served", value: "315,000" },
            { label: "Outage duration", value: "> 12 hrs/day" },
          ],
          notes: "Hybrid PV + 12 MWh storage recommended. Pair with feeder reinforcement phased across hospital campus.",
        },
        {
          name: "Aden Fisheries Industrial Zone",
          governorate: "Aden",
          priority: "High impact",
          lat: 12.8075,
          lon: 45.0331,
          overview: "Cold storage & desalination cluster",
          context: "Industrial port complex reliant on high-cost diesel generation for refrigeration, desalination, and processing.",
          metrics: [
            { label: "Diesel cost", value: "0.45 $/kWh" },
            { label: "Installed load", value: "6.5 MW" },
            { label: "Solar resource", value: "83 / 100" },
          ],
          notes: "Target rooftop PV + battery hybrid with demand response for cold storage loads. Investors interested in PPP structure.",
        },
        {
          name: "Mukalla Peri-urban Microgrid",
          governorate: "Hadramaut",
          priority: "Expansion",
          lat: 14.5515,
          lon: 49.1259,
          overview: "Peri-urban corridor with mini-grid",
          context: "Growing coastal settlements with mini-grid expansion potential. Strong solar resource and feasible wind pilots.",
          metrics: [
            { label: "Population within 10 km", value: "460,000" },
            { label: "Mini-grid customers", value: "18,000" },
            { label: "Solar resource", value: "79 / 100" },
          ],
          notes: "Deploy hybrid PV-wind systems with smart metering. Introduce desalination load management and storage pilots.",
        },
        {
          name: "Marib Energy Hub",
          governorate: "Marib",
          priority: "High impact",
          lat: 15.4620,
          lon: 45.3257,
          overview: "Energy node near gas infrastructure",
          context: "Strategic location to blend renewable generation with existing gas assets for flexible supply.",
          metrics: [
            { label: "Nearest gas plant", value: "12 km" },
            { label: "Solar resource", value: "81 / 100" },
            { label: "Load growth", value: "7% annually" },
          ],
          notes: "Utility-scale PV plus battery storage to shave peaks. Explore grid-forming inverters and dispatch coordination.",
        },
        {
          name: "Taiz Highland Cluster",
          governorate: "Taiz",
          priority: "Humanitarian",
          lat: 13.5795,
          lon: 44.0209,
          overview: "Highland service hub requiring resilient power",
          context: "Health and education facilities face prolonged outages; supply security is critical for humanitarian access.",
          metrics: [
            { label: "Population served", value: "2.0 M" },
            { label: "Health facilities", value: "42" },
            { label: "Elevation", value: "1,377 m" },
          ],
          notes: "Install solar + storage for hospitals and water pumping. Coordinate with humanitarian fleet for logistics support.",
        },
      ];

      const siteList = document.getElementById("site-list");
      const searchInput = document.getElementById("search");
      const overlay = document.getElementById("overlay");
      const overlayName = document.getElementById("overlay-name");
      const overlayNote = document.getElementById("overlay-note");
      const overlayPriority = document.getElementById("overlay-priority");
      const overlayCoord = document.getElementById("overlay-coord");
      const detailTitle = document.getElementById("detail-title");
      const detailSubtitle = document.getElementById("detail-subtitle");
      const detailContext = document.getElementById("detail-context");
      const detailMetrics = document.getElementById("detail-metrics");
      const detailNotes = document.getElementById("detail-notes");
      const resetBtn = document.getElementById("reset-view");
      const mapPlaceholder = document.querySelector(".map-placeholder");
      const mapElement = document.getElementById("leaflet-map");

      let map = null;
      let mapMarker = null;
      let selectedIndex = 0;

      function formatCoord(lat, lon) {
        const latDir = lat >= 0 ? "N" : "S";
        const lonDir = lon >= 0 ? "E" : "W";
        return `${Math.abs(lat).toFixed(4)}°${latDir}, ${Math.abs(lon).toFixed(4)}°${lonDir}`;
      }

      function initMap() {
        if (!mapElement || typeof L === "undefined") {
          if (mapPlaceholder && !document.getElementById("map-fallback")) {
            const fallback = document.createElement("div");
            fallback.id = "map-fallback";
            fallback.style.position = "absolute";
            fallback.style.inset = "0";
            fallback.style.display = "flex";
            fallback.style.alignItems = "center";
            fallback.style.justifyContent = "center";
            fallback.style.padding = "1rem";
            fallback.style.textAlign = "center";
            fallback.style.background = "rgba(7, 10, 22, 0.8)";
            fallback.textContent = "Leaflet failed to load. Check network access.";
            mapPlaceholder.appendChild(fallback);
          }
          return;
        }

        const site = sites[selectedIndex];
        map = L.map(mapElement, {
          zoomControl: true,
          attributionControl: true,
        }).setView([site.lat, site.lon], 6);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 18,
          attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);

        mapMarker = L.marker([site.lat, site.lon]).addTo(map);
      }

      function renderList(filterText = "") {
        const term = filterText.trim().toLowerCase();
        siteList.innerHTML = "";

        sites.forEach((site, idx) => {
          if (
            term &&
            !site.name.toLowerCase().includes(term) &&
            !site.priority.toLowerCase().includes(term)
          ) {
            return;
          }

          const card = document.createElement("div");
          card.className = "site-card";
          card.dataset.selected = idx === selectedIndex ? "true" : "false";

          const title = document.createElement("h3");
          title.textContent = site.name;
          card.appendChild(title);

          const meta = document.createElement("span");
          meta.textContent = `${site.governorate} • ${site.priority}`;
          card.appendChild(meta);

          const overview = document.createElement("span");
          overview.textContent = site.overview;
          card.appendChild(overview);

          card.addEventListener("click", () => {
            selectedIndex = idx;
            updatePanels();
            renderList(searchInput.value);
          });

          siteList.appendChild(card);
        });

        if (!siteList.children.length) {
          const placeholder = document.createElement("div");
          placeholder.className = "site-card";
          placeholder.innerHTML = `
            <h3>No sites match your filter.</h3>
            <span>Adjust the search criteria to see available opportunities.</span>
          `;
          siteList.appendChild(placeholder);
        }
      }

      function updatePanels() {
        const site = sites[selectedIndex];

        overlayName.textContent = site.name;
        overlayNote.textContent = site.overview;
        overlayPriority.textContent = `Priority • ${site.priority}`;
        overlayCoord.textContent = formatCoord(site.lat, site.lon);

        detailTitle.textContent = site.name;
        detailSubtitle.textContent = `${site.priority} • ${site.governorate}`;
        detailContext.textContent = site.context;
        detailNotes.textContent = site.notes;

        detailMetrics.innerHTML = "";
        site.metrics.forEach((metric) => {
          const row = document.createElement("div");
          row.className = "metric";
          row.innerHTML = `
            <span>${metric.label}</span>
            <strong>${metric.value}</strong>
          `;
          detailMetrics.appendChild(row);
        });

        if (map && mapMarker) {
          mapMarker.setLatLng([site.lat, site.lon]);
          map.flyTo([site.lat, site.lon], 6, { duration: 0.8 });
        }
      }

      searchInput.addEventListener("input", (event) => {
        renderList(event.target.value);
      });

      resetBtn.addEventListener("click", () => {
        selectedIndex = 0;
        searchInput.value = "";
        renderList();
        updatePanels();
        if (map && mapMarker) {
          const site = sites[selectedIndex];
          map.flyTo([site.lat, site.lon], 6, { duration: 0.8 });
        }
      });

      // Initial render
      renderList();
      initMap();
      updatePanels();
    </script>
  </body>
</html>
        """,
        height=900,
        scrolling=False,
    )

