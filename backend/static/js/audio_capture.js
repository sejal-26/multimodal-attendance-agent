/**
 * AudioCapture Client
 * Implements browser microphone capture and WebSocket streaming to backend
 * Aligned with Activity 3.1 & 3.2
 */
class AudioCaptureService {
  constructor(onMetricsCallback) {
    this.onMetrics = onMetricsCallback;
    this.ws = null;
    this.audioContext = null;
    this.mediaStream = null;
    this.isRecording = false;
    this.meterElement = null;
  }

  async start() {
    try {
      this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.isRecording = true;

      // Connect WebSocket
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/audio`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        try {
          const metrics = JSON.parse(event.data);
          if (this.onMetrics) this.onMetrics(metrics);
        } catch (e) {
          console.error("Audio WS message error:", e);
        }
      };

      // Set up Web Audio API analyzer
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioCtx();
      const source = this.audioContext.createMediaStreamSource(this.mediaStream);
      const analyser = this.audioContext.createAnalyser();
      analyser.fftSize = 512;
      source.connect(analyser);

      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const checkVolume = () => {
        if (!this.isRecording) return;
        analyser.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const avg = sum / bufferLength;
        // Convert to estimated dB (-60 to 0)
        const db = Math.round((avg / 255) * 60 - 60);

        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify({ audio_level: db }));
        }

        requestAnimationFrame(checkVolume);
      };

      checkVolume();
      console.log("AudioCapture: Live microphone capture initialized.");
    } catch (err) {
      console.warn("AudioCapture: Microphone permission not granted or unavailable. Using simulated acoustic cues.", err);
    }
  }

  stop() {
    this.isRecording = false;
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
    if (this.ws) {
      this.ws.close();
    }
  }
}

window.AudioCaptureService = AudioCaptureService;
