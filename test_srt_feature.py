#!/usr/bin/env python3
"""
Test script for the SRT to Audio generation feature.
This script demonstrates how to use the /tts/srt endpoint.
"""

import requests
import sys
from pathlib import Path

# Configuration
SERVER_URL = "http://localhost:8000"
SRT_ENDPOINT = f"{SERVER_URL}/tts/srt"

def test_srt_to_audio(
    srt_file_path: str,
    voice_mode: str = "predefined",
    predefined_voice_id: str = "Gianna.wav",
    output_format: str = "wav",
    output_file: str = None
):
    """
    Test the SRT to audio generation endpoint.
    
    Args:
        srt_file_path: Path to the SRT subtitle file
        voice_mode: 'predefined' or 'clone'
        predefined_voice_id: Voice file name (if using predefined mode)
        output_format: 'wav', 'opus', or 'mp3'
        output_file: Optional output file path (default: generated_from_srt.{format})
    """
    srt_path = Path(srt_file_path)
    
    if not srt_path.exists():
        print(f"Error: SRT file not found at {srt_file_path}")
        return False
    
    if output_file is None:
        output_file = f"generated_from_srt.{output_format}"
    
    print(f"Testing SRT to Audio Generation")
    print(f"================================")
    print(f"SRT File: {srt_file_path}")
    print(f"Voice Mode: {voice_mode}")
    print(f"Voice ID: {predefined_voice_id}")
    print(f"Output Format: {output_format}")
    print(f"Output File: {output_file}")
    print()
    
    # Prepare the request
    files = {
        'srt_file': (srt_path.name, open(srt_path, 'rb'), 'application/x-subrip')
    }
    
    data = {
        'voice_mode': voice_mode,
        'predefined_voice_id': predefined_voice_id,
        'output_format': output_format,
        'silence_between_segments': 0.5,
    }
    
    try:
        print("Sending request to server...")
        response = requests.post(SRT_ENDPOINT, files=files, data=data, stream=True)
        
        if response.status_code == 200:
            # Save the audio file
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Success! Audio saved to: {output_file}")
            print(f"  File size: {Path(output_file).stat().st_size / 1024:.2f} KB")
            return True
        else:
            print(f"✗ Error: Server returned status code {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to server. Is it running?")
        print(f"  Expected server at: {SERVER_URL}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        files['srt_file'][1].close()


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        srt_file = sys.argv[1]
    else:
        srt_file = "test_sample.srt"
    
    success = test_srt_to_audio(
        srt_file_path=srt_file,
        voice_mode="predefined",
        predefined_voice_id="Gianna.wav",  # Change this to any available voice
        output_format="wav"
    )
    
    sys.exit(0 if success else 1)
