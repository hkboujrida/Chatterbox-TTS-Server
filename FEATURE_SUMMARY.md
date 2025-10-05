# SRT to Audio Generation - Feature Summary

## What Was Added

I've successfully added a complete SRT (SubRip Subtitle) to audio generation feature to your Chatterbox TTS Server. This allows you to convert subtitle files into narrated audio with proper timing and voice synthesis.

## Files Modified

### 1. `requirements.txt`
- Added `pysrt` library for SRT subtitle file parsing

### 2. `utils.py`
Added three new utility functions:
- `parse_srt_file()`: Parses SRT files and extracts subtitle entries with timing information
- `merge_srt_audio_segments()`: Merges generated audio segments with proper timing and silence gaps
- Import handling for the `pysrt` library with availability checking

### 3. `models.py`
Added new Pydantic model:
- `SRTTTSRequest`: Request model for SRT-based audio generation with all TTS parameters

### 4. `server.py`
Added new API endpoint:
- `POST /tts/srt`: Main endpoint for processing SRT files and generating audio
  - Handles file upload via multipart form data
  - Validates SRT format and voice parameters
  - Synthesizes each subtitle entry separately
  - Merges audio with configurable silence gaps
  - Applies post-processing and encoding
  - Returns streaming audio response

## New Files Created

### 1. `test_sample.srt`
Sample SRT file for testing the feature with 5 subtitle entries

### 2. `test_srt_feature.py`
Python test script that demonstrates:
- How to call the `/tts/srt` endpoint
- File upload handling
- Parameter configuration
- Response handling and audio saving

### 3. `SRT_FEATURE_README.md`
Comprehensive documentation including:
- Feature overview and capabilities
- Complete API reference
- Request/response examples
- cURL and Python code examples
- SRT format specifications
- Implementation details
- Use cases and best practices
- Performance considerations

## How to Use

### 1. Install Dependencies
The `pysrt` library has already been installed in your virtual environment:
```bash
./venv/bin/pip install pysrt
```

### 2. Test the Feature

#### Option A: Use the Test Script
```bash
# Make sure your server is running, then:
python test_srt_feature.py test_sample.srt
```

#### Option B: Use cURL
```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@test_sample.srt" \
  -F "voice_mode=predefined" \
  -F "predefined_voice_id=Gianna.wav" \
  -F "output_format=wav" \
  -F "silence_between_segments=0.5" \
  --output generated_from_srt.wav
```

#### Option C: Use Python Requests
```python
import requests

files = {'srt_file': open('test_sample.srt', 'rb')}
data = {
    'voice_mode': 'predefined',
    'predefined_voice_id': 'Gianna.wav',
    'output_format': 'wav',
    'silence_between_segments': 0.5
}

response = requests.post('http://localhost:8000/tts/srt', files=files, data=data)

with open('output.wav', 'wb') as f:
    f.write(response.content)
```

### 3. API Parameters

**Required:**
- `srt_file`: The SRT subtitle file to process
- `voice_mode`: Either `predefined` or `clone`
- `predefined_voice_id` (if using predefined) OR `reference_audio_filename` (if cloning)

**Optional:**
- `output_format`: wav, opus, or mp3 (default: wav)
- `temperature`: 0.0-1.5 (controls randomness)
- `exaggeration`: 0.25-2.0 (controls expressiveness)
- `cfg_weight`: 0.2-1.0 (CFG weight)
- `seed`: Integer (for reproducibility)
- `speed_factor`: 0.25-4.0 (playback speed)
- `silence_between_segments`: 0.0-5.0 seconds (default: 0.5)

## Key Features

1. **Automatic Processing**: Upload an SRT file and get complete audio back
2. **Timing Awareness**: Each subtitle is synthesized and merged with appropriate gaps
3. **Voice Flexibility**: Use any predefined voice or clone a custom voice
4. **Multiple Formats**: Generate WAV, Opus, or MP3 output
5. **Full TTS Control**: All standard TTS parameters are supported
6. **Error Handling**: Robust handling of parsing errors, empty subtitles, and synthesis failures
7. **Performance Monitoring**: Optional tracking of processing time for each step

## How It Works

1. **Upload**: Client uploads SRT file via multipart form data
2. **Parse**: Server parses SRT file to extract subtitle entries with timing
3. **Validate**: Voice parameters and file format are validated
4. **Synthesize**: Each subtitle text is converted to speech using the TTS engine
5. **Merge**: Audio segments are concatenated with silence gaps between them
6. **Post-Process**: Optional audio processing (silence trimming, etc.)
7. **Encode**: Final audio is encoded to the requested format
8. **Stream**: Audio is returned as a streaming response
9. **Cleanup**: Temporary files are automatically removed

## Use Cases

- **Audiobook Creation**: Convert book chapters into narrated audio
- **Video Voiceover**: Generate voiceovers from subtitle tracks
- **Accessibility**: Create audio versions of text content
- **Language Learning**: Generate timed audio for practice materials
- **Content Automation**: Automate voice generation for video content

## Testing Checklist

- [x] Dependencies installed (`pysrt`)
- [x] API endpoint implemented (`/tts/srt`)
- [x] Request model created (`SRTTTSRequest`)
- [x] Utility functions added (parsing, merging)
- [x] Test script created
- [x] Sample SRT file provided
- [x] Documentation written
- [ ] Server tested with the new endpoint (ready to test when server is running)

## Next Steps

1. **Start/restart your server** to load the new code
2. **Run the test script**: `python test_srt_feature.py`
3. **Check the generated audio**: Listen to `generated_from_srt.wav`
4. **Try with your own SRT files**: Use any standard SRT subtitle file
5. **Integrate into your workflow**: Use the API in your applications

## API Documentation

The new endpoint is automatically documented in your FastAPI docs:
- Swagger UI: `http://localhost:8000/docs`
- Look for the `/tts/srt` endpoint under "TTS Generation" tag

## Notes

- The feature gracefully handles empty or invalid subtitle entries
- Long SRT files will take longer to process (linear with number of entries)
- The generated audio timing may not exactly match original subtitle timings
- All existing audio processing settings from `config.yaml` apply to the final output
- Temporary files are automatically cleaned up after processing

Enjoy your new SRT to audio generation feature! 🎉
