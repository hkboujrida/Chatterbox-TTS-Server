#!/usr/bin/env python3
"""
Advanced SRT to Audio Generation Examples
==========================================

This script demonstrates various use cases and advanced features
of the SRT to Audio generation endpoint.
"""

import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any


class SRTAudioGenerator:
    """Client class for interacting with the SRT to Audio API."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.endpoint = f"{server_url}/tts/srt"
    
    def generate_audio(
        self,
        srt_file_path: str,
        voice_mode: str = "predefined",
        predefined_voice_id: Optional[str] = "Gianna.wav",
        reference_audio_filename: Optional[str] = None,
        output_format: str = "wav",
        output_file: Optional[str] = None,
        temperature: Optional[float] = None,
        exaggeration: Optional[float] = None,
        cfg_weight: Optional[float] = None,
        seed: Optional[int] = None,
        speed_factor: Optional[float] = None,
        language: Optional[str] = None,
        silence_between_segments: float = 0.5
    ) -> Dict[str, Any]:
        """
        Generate audio from an SRT file.
        
        Returns:
            Dictionary with 'success' boolean and either 'output_file' or 'error' message.
        """
        srt_path = Path(srt_file_path)
        
        if not srt_path.exists():
            return {"success": False, "error": f"SRT file not found: {srt_file_path}"}
        
        # Prepare files
        files = {
            'srt_file': (srt_path.name, open(srt_path, 'rb'), 'application/x-subrip')
        }
        
        # Prepare form data
        data = {
            'voice_mode': voice_mode,
            'output_format': output_format,
            'silence_between_segments': silence_between_segments,
        }
        
        # Add voice selection
        if voice_mode == 'predefined':
            if not predefined_voice_id:
                return {"success": False, "error": "predefined_voice_id required for predefined mode"}
            data['predefined_voice_id'] = predefined_voice_id
        elif voice_mode == 'clone':
            if not reference_audio_filename:
                return {"success": False, "error": "reference_audio_filename required for clone mode"}
            data['reference_audio_filename'] = reference_audio_filename
        
        # Add optional TTS parameters
        if temperature is not None:
            data['temperature'] = temperature
        if exaggeration is not None:
            data['exaggeration'] = exaggeration
        if cfg_weight is not None:
            data['cfg_weight'] = cfg_weight
        if seed is not None:
            data['seed'] = seed
        if speed_factor is not None:
            data['speed_factor'] = speed_factor
        if language is not None:
            data['language'] = language
        
        # Determine output file
        if output_file is None:
            output_file = f"generated_{srt_path.stem}.{output_format}"
        
        try:
            # Send request
            response = requests.post(self.endpoint, files=files, data=data, stream=True)
            
            if response.status_code == 200:
                # Save audio file
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = Path(output_file).stat().st_size
                return {
                    "success": True,
                    "output_file": output_file,
                    "file_size_kb": file_size / 1024,
                    "format": output_format
                }
            else:
                error_msg = response.text
                try:
                    error_json = response.json()
                    error_msg = error_json.get('detail', error_msg)
                except:
                    pass
                return {
                    "success": False,
                    "error": f"Server error {response.status_code}: {error_msg}"
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Could not connect to server at {self.server_url}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            files['srt_file'][1].close()


# ==================== USAGE EXAMPLES ====================

def example_1_basic():
    """Example 1: Basic usage with default settings."""
    print("\n" + "="*60)
    print("Example 1: Basic Audio Generation")
    print("="*60)
    
    generator = SRTAudioGenerator()
    result = generator.generate_audio(
        srt_file_path="test_sample.srt",
        voice_mode="predefined",
        predefined_voice_id="Gianna.wav",
        output_format="wav"
    )
    
    if result['success']:
        print(f"✓ Success! Generated: {result['output_file']}")
        print(f"  File size: {result['file_size_kb']:.2f} KB")
    else:
        print(f"✗ Failed: {result['error']}")


def example_2_multiple_formats():
    """Example 2: Generate audio in multiple formats."""
    print("\n" + "="*60)
    print("Example 2: Multiple Output Formats")
    print("="*60)
    
    generator = SRTAudioGenerator()
    formats = ['wav', 'opus', 'mp3']
    
    for fmt in formats:
        print(f"\nGenerating {fmt.upper()} format...")
        result = generator.generate_audio(
            srt_file_path="test_sample.srt",
            voice_mode="predefined",
            predefined_voice_id="Gianna.wav",
            output_format=fmt,
            output_file=f"output_sample.{fmt}"
        )
        
        if result['success']:
            print(f"  ✓ {result['output_file']} ({result['file_size_kb']:.2f} KB)")
        else:
            print(f"  ✗ Failed: {result['error']}")


def example_3_custom_voice_clone():
    """Example 3: Using voice cloning with reference audio."""
    print("\n" + "="*60)
    print("Example 3: Voice Cloning Mode")
    print("="*60)
    
    generator = SRTAudioGenerator()
    result = generator.generate_audio(
        srt_file_path="test_sample.srt",
        voice_mode="clone",
        reference_audio_filename="Robert.wav",  # Must exist in reference_audio folder
        output_format="wav",
        silence_between_segments=0.8  # Longer pauses
    )
    
    if result['success']:
        print(f"✓ Cloned voice audio: {result['output_file']}")
        print(f"  File size: {result['file_size_kb']:.2f} KB")
    else:
        print(f"✗ Failed: {result['error']}")


def example_4_fine_tuned_parameters():
    """Example 4: Fine-tuned TTS parameters for specific style."""
    print("\n" + "="*60)
    print("Example 4: Fine-Tuned TTS Parameters")
    print("="*60)
    
    generator = SRTAudioGenerator()
    
    # Configuration for dramatic audiobook narration
    result = generator.generate_audio(
        srt_file_path="test_sample.srt",
        voice_mode="predefined",
        predefined_voice_id="Henry.wav",
        output_format="wav",
        temperature=0.8,        # More expressive
        exaggeration=1.5,       # Increased expressiveness
        cfg_weight=0.7,         # Balanced guidance
        speed_factor=0.9,       # Slightly slower for clarity
        silence_between_segments=1.0  # Dramatic pauses
    )
    
    if result['success']:
        print(f"✓ Dramatic narration: {result['output_file']}")
        print(f"  File size: {result['file_size_kb']:.2f} KB")
        print(f"  Style: Expressive, slower pace with dramatic pauses")
    else:
        print(f"✗ Failed: {result['error']}")


def example_5_fast_news_style():
    """Example 5: Fast-paced news reading style."""
    print("\n" + "="*60)
    print("Example 5: Fast News Reading Style")
    print("="*60)
    
    generator = SRTAudioGenerator()
    
    result = generator.generate_audio(
        srt_file_path="test_sample.srt",
        voice_mode="predefined",
        predefined_voice_id="Emily.wav",
        output_format="mp3",
        temperature=0.3,        # More consistent/stable
        exaggeration=0.5,       # Less expressive
        speed_factor=1.3,       # Faster delivery
        silence_between_segments=0.2  # Minimal pauses
    )
    
    if result['success']:
        print(f"✓ News style audio: {result['output_file']}")
        print(f"  File size: {result['file_size_kb']:.2f} KB")
        print(f"  Style: Fast, consistent, minimal pauses")
    else:
        print(f"✗ Failed: {result['error']}")


def example_6_reproducible_generation():
    """Example 6: Reproducible generation with seed."""
    print("\n" + "="*60)
    print("Example 6: Reproducible Generation")
    print("="*60)
    
    generator = SRTAudioGenerator()
    seed = 42
    
    print(f"Generating with seed={seed} (should be identical each time)")
    
    for i in range(2):
        print(f"\nAttempt {i+1}:")
        result = generator.generate_audio(
            srt_file_path="test_sample.srt",
            voice_mode="predefined",
            predefined_voice_id="Olivia.wav",
            output_format="wav",
            seed=seed,
            output_file=f"reproducible_attempt_{i+1}.wav"
        )
        
        if result['success']:
            print(f"  ✓ {result['output_file']} ({result['file_size_kb']:.2f} KB)")
        else:
            print(f"  ✗ Failed: {result['error']}")


def example_7_batch_processing():
    """Example 7: Batch processing multiple SRT files."""
    print("\n" + "="*60)
    print("Example 7: Batch Processing")
    print("="*60)
    
    generator = SRTAudioGenerator()
    
    # List of SRT files to process (create these first)
    srt_files = [
        "test_sample.srt",
        # Add more SRT files here
    ]
    
    voices = ["Gianna.wav", "Henry.wav", "Emily.wav"]
    
    results = []
    for i, srt_file in enumerate(srt_files):
        voice = voices[i % len(voices)]  # Rotate through voices
        
        print(f"\nProcessing: {srt_file} with voice {voice}")
        result = generator.generate_audio(
            srt_file_path=srt_file,
            voice_mode="predefined",
            predefined_voice_id=voice,
            output_format="mp3",
            output_file=f"batch_output_{i+1}.mp3"
        )
        
        results.append(result)
        
        if result['success']:
            print(f"  ✓ Generated: {result['output_file']}")
        else:
            print(f"  ✗ Failed: {result['error']}")
    
    # Summary
    success_count = sum(1 for r in results if r['success'])
    print(f"\n{'='*60}")
    print(f"Batch Summary: {success_count}/{len(results)} successful")


if __name__ == "__main__":
    print("SRT to Audio Generation - Advanced Examples")
    print("="*60)
    print("\nMake sure the server is running at http://localhost:8000")
    print("and that test_sample.srt exists in the current directory.")
    
    try:
        # Run examples
        example_1_basic()
        # example_2_multiple_formats()
        # example_3_custom_voice_clone()
        # example_4_fine_tuned_parameters()
        # example_5_fast_news_style()
        # example_6_reproducible_generation()
        # example_7_batch_processing()
        
        print("\n" + "="*60)
        print("Examples completed!")
        print("\nUncomment other examples in main() to try them.")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
