# Quick Start Guide: SRT to Audio Generation

## 🚀 Getting Started in 3 Steps

### Step 1: Ensure Dependencies are Installed

The `pysrt` library has already been installed. If needed, reinstall with:

```bash
./venv/bin/pip install pysrt
```

### Step 2: Start Your Server

If not already running, start the Chatterbox TTS Server:

```bash
# Using Docker
docker-compose up

# OR using Python directly
./venv/bin/python server.py
```

### Step 3: Test the Feature

Run the test script with the provided sample SRT file:

```bash
python test_srt_feature.py
```

**Expected Output:**
```
Testing SRT to Audio Generation
================================
SRT File: test_sample.srt
Voice Mode: predefined
Voice ID: Gianna.wav
Output Format: wav
Output File: generated_from_srt.wav

Sending request to server...
✓ Success! Audio saved to: generated_from_srt.wav
  File size: 245.32 KB
```

---

## 📋 Common Use Cases

### Use Case 1: Convert Subtitles to Voiceover

```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@my_video_subtitles.srt" \
  -F "voice_mode=predefined" \
  -F "predefined_voice_id=Henry.wav" \
  -F "output_format=wav" \
  --output voiceover.wav
```

### Use Case 2: Create Audiobook Chapter

```python
import requests

with open('chapter1.srt', 'rb') as f:
    files = {'srt_file': f}
    data = {
        'voice_mode': 'predefined',
        'predefined_voice_id': 'Olivia.wav',
        'output_format': 'mp3',
        'temperature': 0.7,
        'speed_factor': 0.95,  # Slightly slower for clarity
        'silence_between_segments': 1.0  # Dramatic pauses
    }
    
    response = requests.post(
        'http://localhost:8000/tts/srt',
        files=files,
        data=data
    )
    
    with open('chapter1_audio.mp3', 'wb') as audio:
        audio.write(response.content)
```

### Use Case 3: Clone Your Own Voice

```bash
# First, upload your voice sample to reference_audio/
# Then use it:

curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@script.srt" \
  -F "voice_mode=clone" \
  -F "reference_audio_filename=my_voice.wav" \
  -F "output_format=wav" \
  --output my_voiced_script.wav
```

---

## 🎯 Available Voices

Check your `voices/` directory for predefined voices:

```bash
ls -1 voices/
```

Common voices include:
- Gianna.wav (female, warm)
- Henry.wav (male, deep)
- Emily.wav (female, clear)
- Oliver.wav (male, professional)
- And many more!

---

## ⚙️ Parameter Cheat Sheet

| Parameter | Range | Description | Use When |
|-----------|-------|-------------|----------|
| `temperature` | 0.0-1.5 | Randomness | 0.3=stable, 0.8=expressive |
| `exaggeration` | 0.25-2.0 | Expressiveness | 0.5=neutral, 1.5=dramatic |
| `speed_factor` | 0.25-4.0 | Playback speed | 0.9=slower, 1.3=faster |
| `silence_between_segments` | 0.0-5.0 | Gap between subtitles | 0.2=tight, 1.5=dramatic |

### Preset Configurations

**News Reading:**
- temperature: 0.3
- exaggeration: 0.5
- speed_factor: 1.2
- silence: 0.2

**Audiobook:**
- temperature: 0.7
- exaggeration: 1.2
- speed_factor: 0.95
- silence: 1.0

**Documentary:**
- temperature: 0.5
- exaggeration: 0.8
- speed_factor: 1.0
- silence: 0.5

---

## 🔍 Troubleshooting

### Issue: "Could not connect to server"
**Solution:** Make sure the server is running on port 8000
```bash
# Check if server is running
curl http://localhost:8000/docs
```

### Issue: "Voice file not found"
**Solution:** Check available voices
```bash
ls voices/
# Or via API
curl http://localhost:8000/api/ui/initial-data | jq '.predefinedVoices'
```

### Issue: "Failed to parse SRT file"
**Solution:** Validate your SRT format
- Check that entries are numbered sequentially
- Ensure timecodes use format: `HH:MM:SS,mmm --> HH:MM:SS,mmm`
- Verify there's a blank line between entries

### Issue: "pysrt library not found"
**Solution:** Install the dependency
```bash
./venv/bin/pip install pysrt
```

---

## 📊 Performance Tips

1. **Long SRT files:** Processing time increases with number of entries
   - ~1-2 seconds per subtitle entry (depends on text length)
   - Consider splitting very long files

2. **Output format:** Choose based on use case
   - WAV: Highest quality, largest file
   - Opus: Good quality, smaller file
   - MP3: Universal compatibility, medium file size

3. **Silence gaps:** Balance between pacing and file length
   - Shorter gaps (0.2s): Natural conversation flow
   - Medium gaps (0.5s): Standard pacing
   - Longer gaps (1.0s+): Dramatic effect, easier comprehension

---

## 📚 More Examples

See `examples_srt_advanced.py` for:
- Batch processing multiple files
- Different voice styles
- Reproducible generation with seeds
- Multiple output formats
- Custom voice cloning

Run examples:
```bash
python examples_srt_advanced.py
```

---

## 🌐 API Documentation

Full interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Look for the `/tts/srt` endpoint under "TTS Generation"

---

## 🎉 Success!

You're now ready to convert any SRT subtitle file to audio!

**Next Steps:**
1. Try with your own SRT files
2. Experiment with different voices and parameters
3. Integrate into your workflow/application
4. Check out the advanced examples

**Need Help?**
- Review `SRT_FEATURE_README.md` for detailed documentation
- Check `FEATURE_SUMMARY.md` for complete feature overview
- See `WORKFLOW_DIAGRAM.py` for visual process flow

Happy audio generation! 🎤✨
