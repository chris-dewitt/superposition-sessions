/**
 * Pure sine-wave superposition engine — Web Audio API
 */
class SineSuperpositionEngine {
  constructor() {
    this.ctx = null;
    this.master = null;
    this.reverbSend = null;
    this.layers = new Map();
    this.playing = false;
    this.startTime = 0;
    this.scheduledUntil = 0;
    this.scheduleTimer = null;
    this.soloLayer = null;
    this.layerGains = new Map();
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

  setSession(sessionData) {
    this.stop();
    this.layers.clear();
    this.layerGains.clear();
    this.soloLayer = null;

    for (const layer of sessionData.layers) {
      this.layers.set(layer.layer_id, layer);
    }
  }

  _centsRatio(cents) {
    return Math.pow(2, cents / 1200);
  }

  _scheduleLayer(layerId, windowStart, windowEnd) {
    const layer = this.layers.get(layerId);
    if (!layer) return;

    const loopDuration = layer.loop_duration;
    const detune = this._centsRatio(layer.detune_cents || 0);

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
        const peak = event.gain * (this.soloLayer && this.soloLayer !== layerId ? 0.08 : 1);
        gain.gain.setValueAtTime(0.0001, noteStart);
        gain.gain.exponentialRampToValueAtTime(Math.max(peak, 0.0002), noteStart + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, noteEnd);

        osc.connect(gain);
        gain.connect(this.master);

        const rev = this.ctx.createGain();
        rev.gain.value = 0.35;
        gain.connect(rev);
        rev.connect(this.reverbSend);

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
      for (const layerId of this.layers.keys()) {
        this._scheduleLayer(layerId, from - this.startTime, horizon - this.startTime);
      }
      this.scheduledUntil = horizon;
    }
  }

  async play() {
    await this.ensureContext();
    if (this.playing) return;

    this.playing = true;
    this.startTime = this.ctx.currentTime;
    this.scheduledUntil = this.startTime;
    this._tickSchedule();
    this.scheduleTimer = setInterval(() => this._tickSchedule(), 400);
  }

  stop() {
    this.playing = false;
    if (this.scheduleTimer) {
      clearInterval(this.scheduleTimer);
      this.scheduleTimer = null;
    }
    if (this.ctx) {
      this.ctx.close().catch(() => {});
      this.ctx = null;
      this.master = null;
      this.reverbSend = null;
    }
  }

  setSolo(layerId) {
    if (this.soloLayer === layerId) {
      this.soloLayer = null;
    } else {
      this.soloLayer = layerId;
    }
  }
}

window.SineSuperpositionEngine = SineSuperpositionEngine;
