const bootEl = document.getElementById("boot");
const bootText = document.getElementById("boot-text");
const sessionEl = document.getElementById("session");
const psiLabel = document.getElementById("psi-label");
const seedLabel = document.getElementById("seed-label");
const playBtn = document.getElementById("play-btn");
const newBtn = document.getElementById("new-btn");
const orbs = document.querySelectorAll(".orb");

const engine = new window.SineSuperpositionEngine();
let currentSession = null;

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

function setOrbStates(soloId = null) {
  orbs.forEach((orb) => {
    const id = orb.dataset.layer;
    orb.classList.remove("solo", "dim");
    if (soloId && soloId !== id) orb.classList.add("dim");
    if (soloId === id) orb.classList.add("solo");
  });
}

async function bootSequence() {
  bootEl.classList.remove("hidden");
  sessionEl.classList.add("hidden");

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
}

orbs.forEach((orb) => {
  orb.addEventListener("click", () => {
    const layerId = orb.dataset.layer;
    engine.setSolo(layerId);
    setOrbStates(engine.soloLayer);
  });
});

playBtn.addEventListener("click", async () => {
  if (engine.playing) {
    engine.stop();
    playBtn.textContent = "◌ listen";
    playBtn.classList.remove("active");
    return;
  }
  await engine.play();
  playBtn.textContent = "◉ listening";
  playBtn.classList.add("active");
});

newBtn.addEventListener("click", async () => {
  engine.stop();
  setOrbStates(null);
  await bootSequence();
});

bootSequence().catch((err) => {
  bootText.textContent = err.message || "The room went quiet. Try again.";
});
