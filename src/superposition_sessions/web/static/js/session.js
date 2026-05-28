const bootEl = document.getElementById("boot");
const bootText = document.getElementById("boot-text");
const sessionEl = document.getElementById("session");
const psiLabel = document.getElementById("psi-label");
const seedLabel = document.getElementById("seed-label");
const playBtn = document.getElementById("play-btn");
const measureBtn = document.getElementById("measure-btn");
const newBtn = document.getElementById("new-btn");
const orbs = document.querySelectorAll(".orb");
const collapseFlash = document.getElementById("collapse-flash");
const vignettePlaceholder = document.getElementById("vignette-placeholder");
const vignetteTitle = document.getElementById("vignette-title");
const vignetteBody = document.getElementById("vignette-body");
const canonEl = document.getElementById("canon");
const canonList = document.getElementById("canon-list");
const canonEmpty = document.getElementById("canon-empty");
const canonToggle = document.getElementById("canon-toggle");
const canonClose = document.getElementById("canon-close");

const engine = new window.SineSuperpositionEngine();
let currentSession = null;
let collapsed = false;
let measuring = false;

const bootMessages = [
  "tuning qubits...",
  "listening for parallel selves...",
  "holding three songs at once...",
];

async function fetchSession() {
  const res = await fetch("/api/session/new");
  if (!res.ok) throw new Error("The room went quiet. Try again.");
  return res.json();
}

async function fetchCanon() {
  const res = await fetch("/api/sessions");
  if (!res.ok) return [];
  const data = await res.json();
  return data.sessions || [];
}

function setOrbStates(soloId = null, winnerId = null) {
  orbs.forEach((orb) => {
    const id = orb.dataset.layer;
    orb.classList.remove("solo", "dim", "collapsed", "decayed");
    orb.disabled = collapsed;

    if (winnerId) {
      if (id === winnerId) orb.classList.add("collapsed");
      else orb.classList.add("decayed");
      return;
    }

    if (soloId && soloId !== id) orb.classList.add("dim");
    if (soloId === id) orb.classList.add("solo");
  });
}

function resetVignette() {
  vignettePlaceholder.classList.remove("is-hidden");
  vignetteTitle.classList.add("is-hidden");
  vignetteBody.classList.add("is-hidden");
  vignetteTitle.textContent = "";
  vignetteBody.textContent = "";
}

function showVignette(title, body) {
  vignettePlaceholder.classList.add("is-hidden");
  vignetteTitle.textContent = title;
  vignetteBody.textContent = body;
  vignetteTitle.classList.remove("is-hidden");
  vignetteBody.classList.remove("is-hidden");
}

function flashCollapse() {
  collapseFlash.classList.remove("is-hidden");
  collapseFlash.classList.add("active");
  setTimeout(() => {
    collapseFlash.classList.remove("active");
    setTimeout(() => collapseFlash.classList.add("is-hidden"), 400);
  }, 120);
}

async function renderCanon() {
  const sessions = await fetchCanon();
  canonList.innerHTML = "";

  if (!sessions.length) {
    canonEmpty.classList.remove("is-hidden");
    return;
  }

  canonEmpty.classList.add("is-hidden");
  for (const item of sessions) {
    const li = document.createElement("li");
    li.className = "canon-item";
    li.innerHTML = `
      <span class="canon-item-time">${item.poetic_time || ""}</span>
      <span class="canon-item-title">${item.title || "untitled collapse"}</span>
      <span class="canon-item-meta">voice ${item.winner || "?"} · ${item.seed_hash || ""}</span>
    `;
    li.addEventListener("click", async () => {
      const res = await fetch(`/api/sessions/${item.id}`);
      if (!res.ok) return;
      const detail = await res.json();
      showVignette(
        detail.vignette?.title || item.title,
        detail.vignette?.body || "the rest was lost in measurement."
      );
      canonEl.classList.add("is-hidden");
    });
    canonList.appendChild(li);
  }
}

async function bootSequence() {
  collapsed = false;
  measuring = false;
  bootEl.classList.remove("hidden");
  sessionEl.classList.add("hidden");
  resetVignette();
  measureBtn.classList.add("is-hidden");
  measureBtn.disabled = false;
  measureBtn.textContent = "◈ measure";

  let msgIdx = 0;
  bootText.textContent = bootMessages[msgIdx];
  const msgTimer = setInterval(() => {
    msgIdx = (msgIdx + 1) % bootMessages.length;
    bootText.textContent = bootMessages[msgIdx];
  }, Math.max(400, window.SESSION_BOOT_MS / bootMessages.length));

  const minBoot = window.SESSION_BOOT_MS || 900;
  const [session] = await Promise.all([
    fetchSession(),
    new Promise((r) => setTimeout(r, minBoot)),
  ]);

  clearInterval(msgTimer);
  currentSession = session;
  engine.setSession(session);

  psiLabel.textContent = session.psi_label;
  seedLabel.textContent = `seed ${session.seed_hash}`;

  bootEl.classList.add("hidden");
  sessionEl.classList.remove("hidden");
  playBtn.textContent = "◌ listen";
  playBtn.classList.remove("active");
  playBtn.disabled = false;
  setOrbStates(null);
}

orbs.forEach((orb) => {
  orb.addEventListener("click", () => {
    if (collapsed || measuring) return;
    const layerId = orb.dataset.layer;
    engine.setSolo(layerId);
    setOrbStates(engine.soloLayer);
  });
});

playBtn.addEventListener("click", async () => {
  if (collapsed) return;
  if (engine.playing) {
    engine.stopListening();
    playBtn.textContent = "◌ listen";
    playBtn.classList.remove("active");
    measureBtn.classList.add("is-hidden");
    return;
  }
  await engine.play();
  playBtn.textContent = "◉ listening";
  playBtn.classList.add("active");
  measureBtn.classList.remove("is-hidden");
});

measureBtn.addEventListener("click", async () => {
  if (!currentSession || collapsed || measuring) return;

  measuring = true;
  measureBtn.disabled = true;
  measureBtn.textContent = "measuring…";

  if (!engine.playing) await engine.play();

  const preferred = engine.soloLayer || null;

  try {
    const res = await fetch("/api/session/collapse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        seed: currentSession.seed,
        seed_hash: currentSession.seed_hash,
        psi_label: currentSession.psi_label,
        counts: currentSession.counts,
        layers: currentSession.layers,
        preferred_layer: preferred,
      }),
    });

    if (!res.ok) throw new Error("The room went quiet. Try again.");
    const result = await res.json();

    flashCollapse();
    await engine.collapse(result.winner);

    collapsed = true;
    setOrbStates(null, result.winner);
    psiLabel.textContent = result.psi_label_after;
    showVignette(result.vignette.title, result.vignette.body);

    playBtn.disabled = true;
    playBtn.classList.remove("active");
    playBtn.textContent = "◉ collapsed";
    measureBtn.textContent = "◈ measured";
    measureBtn.classList.add("measured");

    await renderCanon();
  } catch (err) {
    measureBtn.disabled = false;
    measureBtn.textContent = "◈ measure";
    measuring = false;
    vignettePlaceholder.textContent = err.message || "The room went quiet. Try again.";
  }
});

newBtn.addEventListener("click", async () => {
  engine.hardStop();
  setOrbStates(null);
  await bootSequence();
});

canonToggle.addEventListener("click", async () => {
  await renderCanon();
  canonEl.classList.remove("is-hidden");
});

canonClose.addEventListener("click", () => {
  canonEl.classList.add("is-hidden");
});

bootSequence().catch((err) => {
  bootText.textContent = err.message || "The room went quiet. Try again.";
});

renderCanon();
