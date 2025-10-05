# SRT to Audio Generation Feature

## Overview

The Chatterbox TTS Server now supports generating audio from SRT (SubRip Subtitle) files. This feature allows you to automatically convert subtitle files into spoken audio, with each subtitle entry being synthesized separately and merged together with appropriate timing.

## Features

- **Automatic SRT Parsing**: Reads and parses standard SRT subtitle files
- **Sequential Audio Generation**: Each subtitle entry is converted to speech
- **Exact Timing Preservation**: Audio segments are placed at precise SRT timestamps
- **Adaptive Speed Adjustment**: Automatically adjusts speech speed to fit subtitle duration
- **Voice Options**: Supports both predefined voices and voice cloning
- **Multiple Output Formats**: Generate audio in WAV, Opus, or MP3 format
- **Full TTS Control**: All standard TTS parameters (temperature, exaggeration, speed, etc.)
- **Intelligent Time-Stretching**: Automatically fits audio to SRT timing using librosa

## API Endpoint

### POST `/tts/srt`

Generate audio from an SRT subtitle file.

#### Request Parameters

**Form Data:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `srt_file` | File | Yes | - | The SRT subtitle file to process |
| `voice_mode` | String | Yes | - | Voice mode: `predefined` or `clone` |
| `predefined_voice_id` | String | Conditional | - | Predefined voice filename (required if `voice_mode=predefined`) |
| `reference_audio_filename` | String | Conditional | - | Reference audio filename (required if `voice_mode=clone`) |
| `output_format` | String | No | `wav` | Output format: `wav`, `opus`, or `mp3` |
| `temperature` | Float | No | Config default | Controls randomness (0.0-1.5) |
| `exaggeration` | Float | No | Config default | Controls expressiveness (0.25-2.0) |
| `cfg_weight` | Float | No | Config default | CFG weight (0.2-1.0) |
| `seed` | Integer | No | Config default | Generation seed for reproducibility |
| `speed_factor` | Float | No | 1.0 | Playback speed factor (0.25-4.0) |
| `language` | String | No | Config default | Language code |
| `silence_between_segments` | Float | No | 0.0 | **[DEPRECATED]** No longer used. Timing is now automatic from SRT file. |

#### Response

Returns the generated audio file as a streaming response with appropriate content type:
- `audio/wav` for WAV format
- `audio/opus` for Opus format  
- `audio/mp3` for MP3 format

#### Example cURL Request

```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@subtitles.srt" \
  -F "voice_mode=predefined" \
  -F "predefined_voice_id=Gianna.wav" \
  -F "output_format=wav" \
  -F "silence_between_segments=0.5" \
  --output generated_audio.wav
```

#### Example Python Request

```python
import requests

# Prepare the request
files = {
    'srt_file': ('subtitles.srt', open('subtitles.srt', 'rb'), 'application/x-subrip')
}

data = {
    'voice_mode': 'predefined',
    'predefined_voice_id': 'Gianna.wav',
    'output_format': 'wav',
    'temperature': 0.7,
    'speed_factor': 1.0
    # Note: silence_between_segments is deprecated - timing now automatic from SRT
}

# Send request
response = requests.post(
    'http://localhost:8000/tts/srt',
    files=files,
    data=data,
    stream=True
)

# Save the audio
if response.status_code == 200:
    with open('output.wav', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Audio saved successfully!")
```

## SRT File Format

The endpoint supports standard SRT subtitle files with the following format:

```srt
1
00:00:00,000 --> 00:00:03,000
This is the first subtitle.

2
00:00:03,500 --> 00:00:07,000
This is the second subtitle.

3
00:00:07,500 --> 00:00:10,000
This is the third subtitle.
```

**Format Requirements:**
- Sequential numbering of subtitle entries
- Timecodes in format: `HH:MM:SS,mmm --> HH:MM:SS,mmm`
- Text content on one or more lines after the timecode
- Empty line between entries

## Timing Preservation

**Important:** The SRT to Audio feature now **preserves exact timing** from your subtitle file.

### How It Works

Each audio segment is placed at the **precise timestamp** specified in the SRT file:

```srt
1
00:00:00,000 --> 00:00:03,000
Welcome to the demo.

2
00:00:03,500 --> 00:00:07,000
This maintains perfect timing.
```

**Generated Audio:**
- `0.0s - 3.0s`: "Welcome to the demo" (spoken)
- `3.0s - 3.5s`: Silence (automatic gap)
- `3.5s - 7.0s`: "This maintains perfect timing" (spoken)
- **Total duration**: Exactly 7.0 seconds

### Benefits

- ✅ Perfect synchronization with videos
- ✅ Maintains original subtitle timing
- ✅ Automatic gap calculation
- ✅ No manual silence configuration needed
- ✅ Professional dubbing quality

### Audio Segment Fitting

The system uses a two-stage approach to ensure audio fits within subtitle duration:

#### Stage 1: Adaptive Speed Adjustment (Pre-Generation)
Before generating audio, the system:
1. Estimates audio duration based on text length (~12 chars/second)
2. Calculates required speed adjustment if text is too long
3. Generates audio at the optimal speed (up to 2.5x faster if needed)

**Example:**
```srt
1
00:00:00,000 --> 00:00:02,000
This is a fairly long subtitle with quite a bit of text.
```
- Text: 56 characters
- Estimated: ~4.67 seconds
- Available: 2.0 seconds
- **Automatic speed**: 2.34x applied during generation
- **Result**: Audio naturally fits in 2 seconds!

#### Stage 2: Time-Stretching (Post-Generation Fallback)
If audio still doesn't fit after generation:
1. **Audio too long**: Time-stretched to fit (requires librosa)
2. **Audio too short**: Padded with silence
3. **Overlapping subtitles**: Later audio overwrites earlier audio

For details, see [Adaptive Speed Guide](./ADAPTIVE_SPEED_GUIDE.md).

For more details, see the [SRT Timing Guide](./SRT_TIMING_GUIDE.md).

## Testing

A test script is provided to verify the functionality:

```bash
# Using the default test SRT file
python test_srt_feature.py

# Using a custom SRT file
python test_srt_feature.py /path/to/your/subtitles.srt
```

## Implementation Details

### Processing Flow

1. **Upload**: SRT file is uploaded via multipart form data
2. **Validation**: File type and format are validated
3. **Parsing**: SRT entries are parsed with timing information
4. **Synthesis**: Each subtitle text is synthesized separately using the TTS engine
5. **Merging**: Audio segments are concatenated with configurable silence between them
6. **Post-processing**: Optional audio processing (silence trimming, etc.)
7. **Encoding**: Final audio is encoded to the requested format
8. **Cleanup**: Temporary files are removed

### Audio Timing

The feature generates audio with proper timing between segments:
- Each subtitle is synthesized independently
- Silence gaps are inserted between consecutive subtitles
- The `silence_between_segments` parameter controls the gap duration
- Empty subtitles are handled by inserting silence of the appropriate duration

### Error Handling

The endpoint handles various error scenarios:
- Invalid SRT file format
- Missing or invalid voice files
- TTS engine failures
- Empty subtitle entries (converted to silence)
- Individual subtitle synthesis failures (replaced with silence)

## Dependencies

The SRT processing feature requires the `pysrt` library:

```bash
pip install pysrt
```

This dependency has been added to `requirements.txt`.

## Configuration

Audio processing settings from `config.yaml` are applied to the final merged audio:
- `audio_processing.enable_silence_trimming`
- `audio_processing.enable_internal_silence_fix`
- `audio_processing.enable_unvoiced_removal`

## Performance Considerations

- Processing time increases linearly with the number of subtitle entries
- Long SRT files with many entries will take longer to process
- Consider the trade-off between `silence_between_segments` and total audio length
- Performance monitoring can be enabled in config to track processing time

## Use Cases

1. **Audiobook Creation**: Convert ebook subtitles to narrated audio
2. **Video Voiceover**: Generate voiceovers from subtitle tracks
3. **Accessibility**: Create audio versions of text content with timing
4. **Language Learning**: Generate timed audio for language practice materials
5. **Content Creation**: Automate voice generation for video content

## Limitations

- Maximum subtitle text length depends on TTS engine capabilities
- Very long subtitle texts may need to be split for optimal quality
- Timing accuracy depends on the TTS engine's output speed
- The generated audio duration may not exactly match the original subtitle timings

## Future Enhancements

Potential improvements for this feature:
- Support for multi-language SRT files
- Voice assignment per subtitle entry
- Audio stretching to match exact subtitle timings
- Batch processing of multiple SRT files
- Progress tracking for long SRT files
- Background job processing for very large files
