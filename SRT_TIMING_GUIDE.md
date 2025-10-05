# SRT Timing Preservation Guide

## Overview

The SRT to Audio feature now **preserves the exact timing** from your subtitle file. Each audio segment is placed at the precise start time specified in the SRT file, maintaining the original subtitle timing and synchronization.

## How It Works

### Previous Behavior (Deprecated)
- Audio segments were concatenated with a fixed silence gap
- Timing was not preserved from the SRT file
- Audio could drift out of sync with the original timing

### New Behavior (Current)
- Audio segments are placed at **exact SRT timestamps**
- Silence gaps are **automatically calculated** based on SRT timing
- Original subtitle synchronization is **perfectly preserved**

## Example

Given this SRT file:

```srt
1
00:00:00,000 --> 00:00:03,000
Welcome to the Chatterbox TTS Server.

2
00:00:03,500 --> 00:00:07,000
This is a demonstration of SRT subtitle generation.

3
00:00:07,500 --> 00:00:11,000
Each subtitle entry will be synthesized separately.
```

**Generated Audio Timeline:**
```
0.0s - 3.0s:   "Welcome to the Chatterbox TTS Server." (spoken)
3.0s - 3.5s:   SILENCE (0.5 seconds)
3.5s - 7.0s:   "This is a demonstration..." (spoken)
7.0s - 7.5s:   SILENCE (0.5 seconds)
7.5s - 11.0s:  "Each subtitle entry..." (spoken)
```

The audio will be **exactly 11 seconds long** (matching the end time of the last subtitle), with each segment placed precisely where the SRT file specifies.

## Audio Segment Handling

### Perfect Fit
If generated audio duration matches the subtitle duration perfectly:
- Audio is placed directly at the specified position
- No adjustment needed

### Audio Too Long
If generated audio is longer than the allocated SRT time slot:
1. **Time-stretching** (if librosa is available):
   - Audio is compressed to fit the exact duration
   - Pitch is preserved using librosa's time-stretch algorithm
2. **Truncation** (fallback):
   - Audio is cut to fit the time slot
   - May result in incomplete speech

### Audio Too Short
If generated audio is shorter than the allocated SRT time slot:
- Audio is placed at the start time
- Remaining space is filled with silence
- Next segment still starts at its designated time

## Configuration

### No Manual Silence Control
The `silence_between_segments` parameter has been **deprecated**. Silence is now automatically determined by the gaps in your SRT file.

### What You Control
1. **SRT Timing**: Edit your SRT file to adjust when segments play
2. **TTS Parameters**: Control speech speed, style, and quality
3. **Voice Selection**: Choose predefined voices or clone voices

## Best Practices

### 1. Accurate SRT Timing
Ensure your SRT file has realistic timing:
```srt
# Good - Reasonable timing
1
00:00:00,000 --> 00:00:03,500
Welcome to our demonstration.

# Bad - Too short for the text
2
00:00:03,500 --> 00:00:04,000
This is a very long sentence that won't fit in half a second.
```

### 2. Buffer Time
Leave small gaps between subtitles for natural pacing:
```srt
1
00:00:00,000 --> 00:00:03,000
First sentence.

2
00:00:03,500 --> 00:00:06,500    # 0.5s gap
Second sentence.
```

### 3. Speed Adjustment
If audio doesn't fit, adjust either:
- **SRT timing**: Extend the end time
- **Speed Factor**: Increase the TTS speed (1.0 - 2.0)
- **Text content**: Shorten the subtitle text

### 4. Synchronization
For video dubbing:
- Match SRT timing to video cuts and scene changes
- Consider natural speech pauses
- Test with the video to verify sync

## Technical Details

### Timeline Construction
1. Parse SRT file to extract all subtitle entries with timing
2. Calculate total duration from last subtitle's end time
3. Create audio buffer of exact duration (filled with silence)
4. Generate audio for each subtitle text
5. Place each audio segment at its start timestamp
6. Handle overlapping or mismatched segments

### Sample Rate
All calculations use the engine's output sample rate (typically 24000 Hz):
```
start_sample = start_time_seconds × sample_rate
end_sample = end_time_seconds × sample_rate
```

### Edge Cases

#### Overlapping Subtitles
```srt
1
00:00:00,000 --> 00:00:05,000
First subtitle.

2
00:00:03,000 --> 00:00:08,000    # Overlaps with #1
Second subtitle.
```
**Result**: Second audio will overwrite the last 2 seconds of first audio.

#### Gap After Last Subtitle
```srt
1
00:00:00,000 --> 00:00:03,000
Only subtitle.
```
**Result**: Audio file is exactly 3 seconds (no trailing silence).

#### Zero-Duration Subtitle
```srt
1
00:00:05,000 --> 00:00:05,000    # Same start and end
Point in time marker.
```
**Result**: Audio is placed at 5 seconds but may extend beyond if needed.

## Migration Guide

### Updating Existing SRT Files

If you used the old version with fixed silence gaps:

**Old approach** (0.5s between all segments):
```srt
1
00:00:00,000 --> 00:00:03,000
First.

2
00:00:03,500 --> 00:00:06,500
Second.
```

**New approach** (timing already correct):
No changes needed! The feature now respects these timings automatically.

### API Changes

**Before:**
```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@subtitles.srt" \
  -F "silence_between_segments=0.5"  # Used to control gaps
```

**After:**
```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@subtitles.srt"
  # Timing is now automatic from SRT file
```

### UI Changes

**Before:**
- Silence duration slider (0.0 - 5.0s)
- Manual control over gaps

**After:**
- Timing preservation info box
- Automatic gap calculation
- Cleaner, simpler interface

## Troubleshooting

### Issue: Audio segments are cut off
**Cause**: Generated audio is too long for the SRT time slot
**Solutions**:
1. Increase subtitle duration in SRT file
2. Reduce TTS speed with `speed_factor` parameter
3. Shorten subtitle text
4. Ensure librosa is installed for time-stretching

### Issue: Large gaps between segments
**Cause**: SRT file has wide time gaps between entries
**Solution**: Edit SRT file to reduce gaps between end and next start time

### Issue: Audio duration doesn't match video
**Cause**: SRT timing doesn't match video length
**Solution**: Use subtitle editing software to sync SRT to video first

### Issue: Overlapping audio
**Cause**: SRT has overlapping subtitle timestamps
**Solution**: Adjust SRT so subtitles don't overlap

## Tools for SRT Editing

Recommended software for adjusting SRT timing:

1. **Subtitle Edit** (Windows, free)
   - Visual timeline editor
   - Audio waveform display
   - Auto-sync features

2. **Aegisub** (Cross-platform, free)
   - Professional subtitle editor
   - Precise timing controls
   - Karaoke timing support

3. **DaVinci Resolve** (Cross-platform, free/paid)
   - Video editing with subtitle support
   - Perfect for video dubbing projects

4. **Online Editors**:
   - Subtitle Tools (web-based)
   - Kapwing (web-based with video preview)

## Performance Notes

- **Memory Usage**: Creates full-duration audio buffer in memory
- **Processing Time**: Same as before (~1-2s per subtitle)
- **File Size**: May be larger if SRT has long gaps (filled with silence)

## Example Code

### Check Generated Audio Duration

```python
import soundfile as sf

# After generation
audio, sr = sf.read('generated_from_srt.wav')
duration = len(audio) / sr

print(f"Audio duration: {duration:.2f}s")
# Should match the last subtitle's end time in your SRT
```

### Validate SRT Timing

```python
import pysrt

subs = pysrt.open('subtitles.srt')
for i, sub in enumerate(subs[:-1]):
    next_sub = subs[i + 1]
    gap = (next_sub.start - sub.end).total_seconds()
    
    if gap < 0:
        print(f"⚠️  Overlap at subtitle {sub.index}: {gap:.2f}s")
    elif gap < 0.1:
        print(f"⚠️  Very tight timing at subtitle {sub.index}: {gap:.2f}s")
    else:
        print(f"✓ Subtitle {sub.index}: {gap:.2f}s gap")
```

## Summary

The new timing preservation system:
- ✅ **Respects SRT timestamps exactly**
- ✅ **Maintains synchronization** with videos
- ✅ **Handles variable gaps** automatically
- ✅ **Simpler to use** (no manual silence control)
- ✅ **Professional quality** dubbing and narration

Edit your SRT file to control timing, and let the TTS engine handle the rest!
