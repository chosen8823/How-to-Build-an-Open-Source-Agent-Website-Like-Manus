#!/usr/bin/env python3
"""
🎤 VRChat Voice Input Integration
Based on VRCTextboxSTT (https://github.com/I5UCC/VRCTextboxSTT)
Using Whisper for free local speech-to-text
"""

import logging
import numpy as np
import sounddevice as sd
from queue import Queue
from threading import Thread
import time

logger = logging.getLogger(__name__)

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning("faster-whisper not installed. Voice input disabled.")


class VoiceInputHandler:
    """
    Voice input handler using OpenAI's Whisper
    Free, local, no cloud API needed

    Based on VRCTextboxSTT project
    """

    def __init__(self,
                 model_size: str = "base",
                 device: str = "cpu",
                 sample_rate: int = 16000,
                 callback=None):
        """
        Initialize voice input handler

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: 'cpu' or 'cuda'
            sample_rate: Audio sample rate (16000 recommended)
            callback: Function to call with transcribed text
        """
        if not WHISPER_AVAILABLE:
            raise ImportError("faster-whisper not installed. Run: pip install faster-whisper")

        self.model_size = model_size
        self.device = device
        self.sample_rate = sample_rate
        self.callback = callback

        # Audio buffer
        self.audio_queue = Queue()
        self.is_recording = False
        self.recording_thread = None

        # Load Whisper model
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = WhisperModel(model_size, device=device)
        logger.info("✅ Whisper model loaded")

    def start_listening(self):
        """Start listening for voice input"""
        if self.is_recording:
            logger.warning("Already recording")
            return

        self.is_recording = True

        # Start recording thread
        self.recording_thread = Thread(target=self._record_audio, daemon=True)
        self.recording_thread.start()

        # Start transcription thread
        transcription_thread = Thread(target=self._transcribe_loop, daemon=True)
        transcription_thread.start()

        logger.info("🎤 Voice input started - speak now!")

    def stop_listening(self):
        """Stop listening for voice input"""
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        logger.info("🛑 Voice input stopped")

    def _record_audio(self):
        """Record audio from microphone"""
        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"Audio status: {status}")

            # Add audio to queue
            self.audio_queue.put(indata.copy())

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=audio_callback
        ):
            while self.is_recording:
                time.sleep(0.1)

    def _transcribe_loop(self):
        """Continuously transcribe audio from queue"""
        buffer = []
        silence_threshold = 0.01
        silence_duration = 0
        max_silence = 1.0  # seconds of silence before transcribing

        while self.is_recording:
            try:
                # Get audio chunk
                if not self.audio_queue.empty():
                    audio_chunk = self.audio_queue.get()
                    buffer.append(audio_chunk)

                    # Check for silence
                    if np.max(np.abs(audio_chunk)) < silence_threshold:
                        silence_duration += len(audio_chunk) / self.sample_rate
                    else:
                        silence_duration = 0

                    # If we have silence, transcribe what we have
                    if silence_duration >= max_silence and len(buffer) > 0:
                        self._transcribe_buffer(buffer)
                        buffer = []
                        silence_duration = 0
                else:
                    time.sleep(0.01)

            except Exception as e:
                logger.error(f"Transcription error: {e}")

    def _transcribe_buffer(self, buffer):
        """Transcribe audio buffer using Whisper"""
        if len(buffer) == 0:
            return

        try:
            # Concatenate audio chunks
            audio_data = np.concatenate(buffer).flatten()

            # Skip if too quiet
            if np.max(np.abs(audio_data)) < 0.01:
                return

            # Transcribe with Whisper
            segments, info = self.model.transcribe(
                audio_data,
                language="en",
                beam_size=5
            )

            # Get transcribed text
            text = ""
            for segment in segments:
                text += segment.text + " "

            text = text.strip()

            if text and len(text) > 0:
                logger.info(f"🎤 Transcribed: {text}")

                # Call callback with transcribed text
                if self.callback:
                    self.callback(text)

        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")

    def transcribe_audio_file(self, audio_file: str) -> str:
        """
        Transcribe an audio file

        Args:
            audio_file: Path to audio file

        Returns:
            Transcribed text
        """
        try:
            segments, info = self.model.transcribe(audio_file, beam_size=5)

            text = ""
            for segment in segments:
                text += segment.text + " "

            return text.strip()

        except Exception as e:
            logger.error(f"File transcription error: {e}")
            return ""


# Singleton instance
_voice_input: VoiceInputHandler = None


def get_voice_input(
    model_size: str = "base",
    device: str = "cpu",
    callback=None
) -> VoiceInputHandler:
    """Get or create voice input handler singleton"""
    global _voice_input
    if _voice_input is None:
        _voice_input = VoiceInputHandler(
            model_size=model_size,
            device=device,
            callback=callback
        )
    return _voice_input
