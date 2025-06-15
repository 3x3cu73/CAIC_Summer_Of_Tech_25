#!/usr/bin/env python3
import numpy as np
import wave
import struct

# Morse code mapping
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '{': '-.--.',  '}': '-.--.-', '_': '..--.-'
}

def create_morse_signal(t, message, freq, dot_duration=0.05, dash_duration=0.15, start_time=0.5):
    """Create a Morse code signal at specified frequency"""
    signal = np.zeros(len(t))
    current_time = start_time
    
    for char in message:
        if char in MORSE_CODE:
            morse = MORSE_CODE[char]
            for symbol in morse:
                start_idx = int(current_time * len(t) / t[-1])
                symbol_duration = dot_duration if symbol == '.' else dash_duration
                end_idx = int((current_time + symbol_duration) * len(t) / t[-1])
                
                if start_idx < len(t) and end_idx <= len(t):
                    t_segment = t[start_idx:end_idx]
                    morse_signal = np.sin(2 * np.pi * freq * t_segment)
                    signal[start_idx:end_idx] = morse_signal
                
                current_time += symbol_duration + dot_duration
            current_time += dash_duration
    
    return signal

def create_audio_with_morse_message():
    """Create audio file with both audible and hidden Morse code messages"""
    # Audio parameters
    sample_rate = 44100
    duration = 10  # 8 seconds
    
    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create base music
    base_audio = (
        0.3 * np.sin(2 * np.pi * 440 * t) +   # A4 note
        0.2 * np.sin(2 * np.pi * 880 * t) +   # A5 note
        0.15 * np.sin(2 * np.pi * 1320 * t)   # E6 note
    )
    
    # Create wide-spectrum background noise
    background_noise = np.random.normal(0, 0.3, len(t))
    for freq in [1000, 2000, 3000, 4000, 5000]:
        noise_band = np.random.normal(0, 0.1, len(t))
        carrier = np.sin(2 * np.pi * freq * t)
        background_noise += noise_band * carrier * 0.1
    
    # Create audible decoy Morse code (800 Hz)
    decoy_morse = create_morse_signal(t, "DECOY", 800, 0.15, 0.45)
    
    # Create hidden Morse code (18 kHz)
    hidden_morse = create_morse_signal(t, "R34LFL4G", 18000, 0.05, 0.15, 0.75)
    
    # Mix all channels
    final_audio = (
        base_audio * 0.5 +              # Musical base
        background_noise * 0.2 +        # Background noise
        decoy_morse * 0.3 +            # Audible Morse (decoy)
        hidden_morse * 0.4             # Hidden Morse (real flag)
    )
    
    # Add some masking noise around hidden morse frequency
    mask_noise = np.random.normal(0, 0.2, len(t))
    mask_carrier = np.sin(2 * np.pi * 17500 * t)  # Slightly below hidden frequency
    final_audio += mask_noise * mask_carrier * 0.15
    
    # Normalize audio
    final_audio = final_audio / np.max(np.abs(final_audio)) * 0.8
    
    # Convert to 16-bit integers
    audio_data = (final_audio * 32767).astype(np.int16)
    
    return audio_data, sample_rate

def save_wav_file(audio_data, sample_rate, filename):
    """Save audio data as WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        for sample in audio_data:
            wav_file.writeframes(struct.pack('<h', sample))

def main():
    print("Generating audio spectrogram challenge...")
    
    # Create audio with hidden Morse message
    audio_data, sample_rate = create_audio_with_morse_message()
    
    # Save to file
    save_wav_file(audio_data, sample_rate, "mysterious_audio.wav")
    print("Created audio file: mysterious_audio.wav")
    

if __name__ == "__main__":
    main()