"""
Audio system module for text-to-speech and audio feedback
"""

import pyttsx3
import pygame
import threading
import time
from config import TTS_CONFIG, AUDIO_CONFIG

class AudioSystem:
    def __init__(self):
        self.tts_engine = None
        self.is_speaking = False
        self.audio_queue = []
        self.queue_lock = threading.Lock()
        
        # Initialize TTS engine
        self._init_tts()
        
        # Initialize pygame for audio feedback
        pygame.mixer.init()
        
    def _init_tts(self):
        """
        Initialize text-to-speech engine
        """
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', TTS_CONFIG['rate'])
            self.tts_engine.setProperty('volume', TTS_CONFIG['volume'])
            
            # Set voice
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > TTS_CONFIG['voice_id']:
                self.tts_engine.setProperty('voice', voices[TTS_CONFIG['voice_id']].id)
            
            print("Text-to-speech engine initialized")
            
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            self.tts_engine = None
    
    def speak(self, text, priority=False):
        """
        Convert text to speech
        """
        if self.tts_engine is None:
            print(f"TTS not available: {text}")
            return
        
        try:
            if priority:
                # Interrupt current speech for high priority messages
                self.stop_speaking()
            
            # Add to queue or speak immediately
            with self.queue_lock:
                if priority or not self.is_speaking:
                    self._speak_immediately(text)
                else:
                    self.audio_queue.append(text)
                    
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
    
    def _speak_immediately(self, text):
        """
        Speak text immediately
        """
        def speak_thread():
            self.is_speaking = True
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Error speaking: {e}")
            finally:
                self.is_speaking = False
                self._process_queue()
        
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
    
    def _process_queue(self):
        """
        Process queued audio messages
        """
        with self.queue_lock:
            if self.audio_queue and not self.is_speaking:
                next_text = self.audio_queue.pop(0)
                self._speak_immediately(next_text)
    
    def stop_speaking(self):
        """
        Stop current speech
        """
        if self.tts_engine:
            self.tts_engine.stop()
        self.is_speaking = False
    
    def clear_queue(self):
        """
        Clear audio queue
        """
        with self.queue_lock:
            self.audio_queue.clear()
    
    def announce_obstacle(self, distance):
        """
        Announce obstacle detection
        """
        message = AUDIO_CONFIG['obstacle_warning'].format(int(distance))
        self.speak(message, priority=True)
    
    def announce_sign(self, sign_type, distance=None):
        """
        Announce road sign detection
        """
        if distance:
            message = f"{AUDIO_CONFIG['sign_detected'].format(sign_type)} at {int(distance)} centimeters"
        else:
            message = AUDIO_CONFIG['sign_detected'].format(sign_type)
        self.speak(message)
    
    def announce_object(self, object_type, distance=None):
        """
        Announce object detection
        """
        if distance:
            message = f"{AUDIO_CONFIG['object_detected'].format(object_type)} at {int(distance)} centimeters"
        else:
            message = AUDIO_CONFIG['object_detected'].format(object_type)
        self.speak(message)
    
    def system_ready(self):
        """
        Announce system ready
        """
        self.speak(AUDIO_CONFIG['system_ready'])
    
    def battery_low(self):
        """
        Announce low battery
        """
        self.speak(AUDIO_CONFIG['battery_low'], priority=True)
    
    def play_beep(self, frequency=1000, duration=0.1):
        """
        Play a beep sound
        """
        try:
            # Generate a simple beep using pygame
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                arr[i][0] = 32767 * np.sin(2 * np.pi * frequency * i / sample_rate)
                arr[i][1] = arr[i][0]
            
            sound = pygame.sndarray.make_sound(arr.astype(np.int16))
            sound.play()
            
        except Exception as e:
            print(f"Error playing beep: {e}")
    
    def cleanup(self):
        """
        Cleanup audio resources
        """
        self.stop_speaking()
        self.clear_queue()
        pygame.mixer.quit()
        print("Audio system cleaned up")

# Test function
if __name__ == "__main__":
    import numpy as np
    
    audio = AudioSystem()
    
    try:
        # Test basic speech
        audio.speak("Testing the audio system")
        time.sleep(2)
        
        # Test obstacle announcement
        audio.announce_obstacle(50)
        time.sleep(2)
        
        # Test sign announcement
        audio.announce_sign("stop sign", 30)
        time.sleep(2)
        
        # Test beep
        audio.play_beep()
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Stopping audio system test")
    finally:
        audio.cleanup()