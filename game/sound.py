import pygame
import numpy as np


class SoundManager:
    def __init__(self):
        """Initialize sound manager."""
        pygame.mixer.init()
        
        # Create sounds
        self.egg_collect_sound = self._create_yum_sound()  # "Yum" sound
        self.death_sound = self._create_beep_sound(220, 500)  # A3 note, 500ms
        self.tick_sound = self._create_white_noise_sound(100)  # 100ms white noise
        
        # Reduce the volume of the yum sound to make it much quieter
        self.egg_collect_sound.set_volume(0.1)  # Reduced from 0.2 to 0.1
    
    def _create_beep_sound(self, frequency, duration):
        """Create a beep sound with the given frequency and duration."""
        sample_rate = 44100  # CD quality
        samples = int(duration * sample_rate / 1000)  # Convert ms to samples
        
        # Generate sine wave
        buf = np.sin(2 * np.pi * np.arange(samples) * frequency / sample_rate)
        
        # Convert to 16-bit signed integers
        buf = (buf * 32767).astype(np.int16)
        
        # Create sound from buffer
        sound = pygame.mixer.Sound(buf)
        return sound
    
    def _create_white_noise_sound(self, duration):
        """Create a white noise sound with the given duration."""
        sample_rate = 44100  # CD quality
        samples = int(duration * sample_rate / 1000)  # Convert ms to samples
        
        # Generate white noise
        buf = np.random.uniform(-1, 1, samples)
        
        # Convert to 16-bit signed integers
        buf = (buf * 32767).astype(np.int16)
        
        # Create sound from buffer
        sound = pygame.mixer.Sound(buf)
        return sound
    
    def _create_yum_sound(self):
        """Create a 'yum' sound effect."""
        sample_rate = 44100  # CD quality
        duration = 300  # 300ms
        samples = int(duration * sample_rate / 1000)
        
        # Create a buffer for our sound
        buf = np.zeros(samples, dtype=np.float32)
        
        # First part: rising tone (Y)
        y_duration = int(samples * 0.3)  # 30% of the sound
        y_freq_start = 75  # 300/4
        y_freq_end = 150   # 600/4
        for i in range(y_duration):
            # Linear frequency increase
            freq = y_freq_start + (y_freq_end - y_freq_start) * i / y_duration
            buf[i] = np.sin(2 * np.pi * freq * i / sample_rate)
        
        # Second part: falling tone (U)
        u_duration = int(samples * 0.4)  # 40% of the sound
        u_freq_start = 150  # 600/4
        u_freq_end = 100    # 400/4
        for i in range(u_duration):
            # Linear frequency decrease
            freq = u_freq_start + (u_freq_end - u_freq_start) * i / u_duration
            buf[y_duration + i] = np.sin(2 * np.pi * freq * i / sample_rate)
        
        # Third part: humming (M)
        m_duration = int(samples * 0.3)  # 30% of the sound
        m_freq = 100  # 400/4
        for i in range(m_duration):
            # Constant frequency with decreasing amplitude
            amplitude = 1.0 - 0.8 * i / m_duration
            buf[y_duration + u_duration + i] = amplitude * np.sin(2 * np.pi * m_freq * i / sample_rate)
        
        # Apply envelope to smooth the sound
        envelope = np.ones(samples)
        attack = int(samples * 0.1)
        release = int(samples * 0.2)
        
        # Attack (fade in)
        envelope[:attack] = np.linspace(0, 1, attack)
        # Release (fade out)
        envelope[-release:] = np.linspace(1, 0, release)
        
        # Apply envelope
        buf = buf * envelope
        
        # Convert to 16-bit signed integers
        buf = (buf * 32767).astype(np.int16)
        
        # Create sound from buffer
        sound = pygame.mixer.Sound(buf)
        return sound
    
    def play_tick(self):
        """Play the tick sound."""
        self.tick_sound.play()
    
    def play_egg_collect(self):
        """Play the egg collect sound."""
        self.egg_collect_sound.play()
    
    def play_death(self):
        """Play the death sound."""
        self.death_sound.play() 