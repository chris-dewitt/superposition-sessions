/**
 * Pure sine-wave superposition engine — Web Audio API
 */
class SineSuperpositionEngine {
  constructor() {
    this.ctx = null;
    this.master = null;
    this.reverbSend = null;
    this.layers = new Map();
    this.layerBuses = new Map();
    this.playing = false;
    this.collapsed = false;
    this.collapsedWinner = null;
    this.startTime = 0;
    this.scheduledUntil = 0;
    this.scheduleTimer = null;
    this.soloLayer = null;
  }

  async ensureContext() {
    if (!this.ctx) {
      this.ctx = new AudioContext();
      this.master = this.ctx.createGain();
      this.master.gain.value = 0.85;
      this.master.connect(this.ctx.destination);

      this.reverbSend = this.ctx.createConvolver();
      this._buildReverbImpulse();
      const reverbGain = this.ctx.createGain();
      reverbGain.gain.value = 0.22;
      this.reverbSend.connect(reverbGain);
      reverbGain.connect(this.master);
    }
    if (this.ctx.state === "suspended") {
      await this.ctx.resume();
    }
  }

  _buildReverbImpulse() {
    const rate = this.ctx.sampleRate;
    const length = rate * 1.8;
    const impulse = this.ctx.createBuffer(2, length, rate);
    for (let ch = 0; ch < 2; ch++) {
      const data = impulse.getChannelData(ch);
      for (let i = 0; i < length; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2.2);
      }
    }
    this.reverbSend.buffer = impulse;
  }

  _ensureLayerBus(layerId) {
    if (!this.layerBuses.has(layerId)) {
      const bus = this.ctx.createGain();
      bus.gain.value = 1;
      bus.connect(this.master);
      const revSend = this.ctx.createGain();
      revSend.gain.value = 0.35;
      bus.connect(revSend);
      revSend.connect(this.reverbSend);
      this.layerBuses.set(layerId, bus);
    }
    return this.layerBuses.get(layerId);
  }

  setSession(sessionData) {
    this.hardStop();
    this.layers.clear();
    this.layerBuses.clear();
    this.soloLayer = null;
    this.collapsed = false;
    this.collapsedWinner = null;

    for (const layer of sessionData.layers) {
      this.layers.set(layer.layer_id, layer);
    }
  }

  _centsRatio(cents) {
    return Math.pow(2, cents / 1200);
  }

  _activeLayers() {
    if (this.collapsed && this.collapsedWinner) {
      return [this.collapsedWinner];
    }
    return [...this.layers.keys()];
  }

  _layerVolume(layerId) {
    if (this.collapsed) return layerId === this.collapsedWinner ? 1 : 0;
    if (this.soloLayer && this.soloLayer !== layerId) return 0.08;
    return 1;
  }

  _scheduleLayer(layerId, windowStart, windowEnd) {
    const layer = this.layers.get(layerId);
    if (!layer) return;

    const bus = this._ensureLayerBus(layerId);
    const loopDuration = layer.loop_duration;
    const detune = this._centsRatio(layer.detune_cents || 0);
    const vol = this._layerVolume(layerId);

    let t = windowStart;
    while (t < windowEnd) {
      for (const event of layer.events) {
        const noteStart = t + event.start;
        const noteEnd = noteStart + event.duration;
        if (noteEnd < this.ctx.currentTime) continue;
        if (noteStart > windowEnd) break;

        const osc = this.ctx.createOscillator();
        osc.type = "sine";
        osc.frequency.value = event.freq * detune;

        const gain = this.ctx.createGain();
        const peak = event.gain * vol;
        gain.gain.setValueAtTime(0.0001, noteStart);
        gain.gain.exponentialRampToValueAtTime(Math.max(peak, 0.0002), noteStart + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, noteEnd);

        osc.connect(gain);
        gain.connect(bus);

        osc.start(noteStart);
        osc.stop(noteEnd + 0.02);
      }
      t += loopDuration;
    }
  }

  _tickSchedule() {
    if (!this.playing || !this.ctx) return;

    const now = this.ctx.currentTime;
    const horizon = now + 2.5;
    if (this.scheduledUntil < horizon) {
      const from = Math.max(this.scheduledUntil, now);
      for (const layerId of this._activeLayers()) {
        this._scheduleLayer(layerId, from - this.startTime, horizon - this.startTime);
      }
      this.scheduledUntil = horizon;
    }
  }

  async play() {
    await this.ensureContext();
    if (this.playing) return;

    this.playing = true;
    if (!this.startTime) {
      this.startTime = this.ctx.currentTime;
      this.scheduledUntil = this.startTime;
    }
    this._tickSchedule();
    this.scheduleTimer = setInterval(() => this._tickSchedule(), 400);
  }

  hardStop() {
    this.playing = false;
    this.startTime = 0;
    this.scheduledUntil = 0;
    if (this.scheduleTimer) {
      clearInterval(this.scheduleTimer);
      this.scheduleTimer = null;
    }
    if (this.ctx) {
      this.ctx.close().catch(() => {});
      this.ctx = null;
      this.master = null;
      this.reverbSend = null;
      this.layerBuses.clear();
    }
  }

  stopListening() {
    this.playing = false;
    if (this.scheduleTimer) {
      clearInterval(this.scheduleTimer);
      this.scheduleTimer = null;
    }
  }

  setSolo(layerId) {
    if (this.collapsed) return;
    if (this.soloLayer === layerId) {
      this.soloLayer = null;
    } else {
      this.soloLayer = layerId;
    }
  }

  async collapse(winnerId) {
    await this.ensureContext();
    if (!this.playing) await this.play();

    const now = this.ctx.currentTime;
    const silenceEnd = now + 0.4;
    const fadeEnd = silenceEnd + 1.2;

    // silence gap
    this.master.gain.cancelScheduledValues(now);
    this.master.gain.setValueAtTime(this.master.gain.value, now);
    this.master.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);
    this.master.gain.setValueAtTime(0.0001, silenceEnd);
    this.master.gain.exponentialRampToValueAtTime(0.85, silenceEnd + 0.15);

    // high-pass sweep on collapse
    const filter = this.ctx.createBiquadFilter();
    filter.type = "highpass";
    filter.frequency.setValueAtTime(200, now);
    filter.frequency.exponentialRampToValueAtTime(8000, silenceEnd);
    this.master.disconnect();
    this.master.connect(filter);
    filter.connect(this.ctx.destination);
    setTimeout(() => {
      try {
        filter.disconnect();
        this.master.disconnect();
        this.master.connect(this.ctx.destination);
      } catch (_) {}
    }, 1600);

    // fade losers
    for (const [layerId, bus] of this.layerBuses.entries()) {
      bus.gain.cancelScheduledValues(now);
      bus.gain.setValueAtTime(bus.gain.value, now);
      if (layerId === winnerId) {
        bus.gain.setValueAtTime(1, silenceEnd);
      } else {
        bus.gain.exponentialRampToValueAtTime(0.0001, fadeEnd);
      }
    }

    await new Promise((r) => setTimeout(r, 1600));

    this.collapsed = true;
    this.collapsedWinner = winnerId;
    this.soloLayer = null;
    this.scheduledUntil = this.ctx.currentTime;
  }
}

window.SineSuperpositionEngine = SineSuperpositionEngine;
