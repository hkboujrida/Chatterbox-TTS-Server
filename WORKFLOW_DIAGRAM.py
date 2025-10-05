"""
SRT to Audio Generation - Workflow Visualization
================================================

┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT UPLOADS SRT FILE                      │
│  Example: subtitles.srt with 5 subtitle entries + voice selection  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVER: PARSE SRT FILE                            │
│  Extract subtitle entries with timing information:                  │
│  - Index, Start time, End time, Duration, Text                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│              VALIDATE VOICE PARAMETERS                               │
│  Check if predefined voice or reference audio exists                │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│         SYNTHESIZE EACH SUBTITLE SEPARATELY                          │
│                                                                      │
│  Subtitle 1: "Welcome..."     → [Audio Segment 1]                   │
│  Subtitle 2: "This is..."     → [Audio Segment 2]                   │
│  Subtitle 3: "Each entry..."  → [Audio Segment 3]                   │
│  Subtitle 4: "And then..."    → [Audio Segment 4]                   │
│  Subtitle 5: "Thank you..."   → [Audio Segment 5]                   │
│                                                                      │
│  Each segment uses same voice and TTS parameters                    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│            MERGE AUDIO SEGMENTS WITH TIMING                          │
│                                                                      │
│  [Segment 1] + [Silence 0.5s] + [Segment 2] + [Silence 0.5s] +     │
│  [Segment 3] + [Silence 0.5s] + [Segment 4] + [Silence 0.5s] +     │
│  [Segment 5]                                                         │
│                                                                      │
│  = [Complete Audio Track]                                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│           APPLY POST-PROCESSING (if enabled)                         │
│  - Silence trimming (remove leading/trailing silence)               │
│  - Internal silence fix (adjust gaps in speech)                     │
│  - Unvoiced segment removal (clean up artifacts)                    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│         ENCODE TO REQUESTED FORMAT                                   │
│  WAV / Opus / MP3 at target sample rate                             │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│              RETURN AUDIO TO CLIENT                                  │
│  Streaming response with audio file                                 │
│  Cleanup temporary SRT file                                          │
└─────────────────────────────────────────────────────────────────────┘


PARAMETER FLOW
==============

Input Parameters:
  ├─ srt_file (required)
  ├─ voice_mode (predefined/clone)
  ├─ voice selection (predefined_voice_id or reference_audio_filename)
  ├─ output_format (wav/opus/mp3)
  ├─ TTS parameters (temperature, exaggeration, cfg_weight, seed, speed_factor)
  └─ silence_between_segments (0.0-5.0 seconds)

Processing:
  ├─ Each subtitle uses same voice and TTS parameters
  ├─ Speed factor applied to each segment individually
  └─ Silence gaps inserted between segments

Output:
  └─ Single audio file with filename: tts_srt_{original_name}_{timestamp}.{format}


ERROR HANDLING
==============

The system gracefully handles:
  ├─ Invalid SRT file format → 400 Bad Request
  ├─ Missing voice file → 404 Not Found
  ├─ Empty subtitle entries → Inserts silence of appropriate duration
  ├─ Individual synthesis failures → Replaces with silence
  ├─ TTS engine not loaded → 503 Service Unavailable
  └─ pysrt library not available → 503 Service Unavailable


TIMING EXAMPLE
==============

SRT Input:
  1. 00:00:00,000 --> 00:00:03,000 : "Hello world"
  2. 00:00:03,500 --> 00:00:06,000 : "This is a test"

Audio Output (with 0.5s silence between):
  [3.2s of "Hello world"] + [0.5s silence] + [2.8s of "This is a test"]
  Total: ~6.5 seconds

Note: Actual audio duration depends on TTS synthesis speed and may not
      exactly match the original subtitle timings.
"""
