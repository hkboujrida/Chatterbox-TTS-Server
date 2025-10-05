# SRT Timing Update - Change Summary

## What Changed?

The SRT to Audio feature has been updated to **preserve exact timing** from subtitle files instead of using a fixed silence gap between segments.

## Before vs After

### Before (Deprecated)
- Audio segments were concatenated with a fixed silence gap
- User controlled gap duration with a slider (0-5 seconds)
- Timing could drift from original SRT file
- Not suitable for video synchronization

### After (Current)
- Audio segments placed at **exact SRT timestamps**
- Silence gaps **automatically calculated** from SRT timing
- **Perfect preservation** of original subtitle timing
- Ideal for video dubbing and synchronization

## Visual Example

**SRT File:**
```srt
1
00:00:00,000 --> 00:00:03,000
First subtitle.

2
00:00:05,000 --> 00:00:08,000
Second subtitle.
```

**Generated Audio Timeline:**
```
0s ─────────── 3s ────────── 5s ─────────── 8s
│   First sub   │  Silence   │  Second sub  │
└──────────────┴────────────┴──────────────┘
Total: 8 seconds (matches SRT end time)
```

## Files Modified

### Backend
1. **`utils.py`**
   - `merge_srt_audio_segments()`: Complete rewrite
   - Now creates full-duration audio buffer
   - Places segments at exact timestamps
   - Handles time-stretching for long audio

2. **`models.py`**
   - `SRTTTSRequest.silence_between_segments`: Marked as deprecated
   - Parameter kept for backward compatibility but not used

### Frontend
3. **`ui/index.html`**
   - Removed: Silence slider control
   - Added: Timing preservation info box
   - Updated: Description text

4. **`ui/script.js`**
   - Removed: Silence slider event handlers
   - Removed: Silence parameter from API requests
   - Updated: Comments to reflect new behavior

### Documentation
5. **`SRT_FEATURE_README.md`**
   - Updated: Feature description
   - Marked: `silence_between_segments` as deprecated
   - Added: Timing preservation section
   - Updated: Examples

6. **`UI_INTEGRATION_GUIDE.md`**
   - Removed: Silence slider documentation
   - Added: Timing preservation explanation
   - Updated: User workflow

7. **`SRT_TIMING_GUIDE.md`** *(NEW)*
   - Complete guide to timing preservation
   - Examples and best practices
   - Troubleshooting section
   - Migration guide

8. **`SRT_TIMING_UPDATE.md`** *(THIS FILE)*
   - Quick reference for changes

## API Changes

### Request (Deprecated Parameter)
```bash
# Old (still works but ignored)
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@subtitles.srt" \
  -F "silence_between_segments=0.5"  # ← Deprecated

# New (recommended)
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@subtitles.srt"
  # Timing is automatic
```

### Response (Behavior Change)
- **Before**: Audio duration = (sum of all audio) + (fixed gaps)
- **After**: Audio duration = (last subtitle end time from SRT)

## Migration Guide

### For API Users
- **No breaking changes**: Old code still works
- **Recommendation**: Remove `silence_between_segments` parameter
- **Benefit**: Audio now matches SRT timing exactly

### For UI Users
- **No action needed**: UI automatically updated
- **Change**: Silence slider removed
- **Benefit**: Simpler interface, better results

### For SRT Files
- **No changes needed**: Existing SRT files work better
- **Tip**: Edit SRT timing to control audio gaps
- **Tools**: Use subtitle editors like Subtitle Edit or Aegisub

## Key Benefits

✅ **Perfect Synchronization**: Audio matches video timing exactly
✅ **Professional Quality**: Suitable for dubbing and narration
✅ **Automatic Gaps**: No manual silence configuration
✅ **Simpler Interface**: One less parameter to configure
✅ **Backward Compatible**: Old API calls still work
✅ **Time-Stretching**: Fits audio to SRT duration (requires librosa)

## Technical Details

### Timing Algorithm
```python
# 1. Parse SRT to get all subtitle timings
subtitles = parse_srt_file(srt_path)

# 2. Calculate total duration from last subtitle
total_duration = subtitles[-1]['end']

# 3. Create empty audio buffer
audio_buffer = zeros(total_duration * sample_rate)

# 4. Place each audio segment at its start time
for audio, timing in zip(audio_segments, subtitles):
    start_sample = timing['start'] * sample_rate
    audio_buffer[start_sample:start_sample+len(audio)] = audio
```

### Time-Stretching
When generated audio is longer than SRT duration:
```python
if len(audio) > allocated_duration:
    if librosa available:
        # Compress audio to fit, preserve pitch
        audio = librosa.effects.time_stretch(audio, rate=stretch_rate)
    else:
        # Fallback: truncate
        audio = audio[:allocated_duration]
```

## Testing

### Quick Test
```bash
# 1. Restart server
docker-compose restart

# 2. Upload test_sample.srt via UI
# 3. Generate audio
# 4. Verify duration is exactly 18 seconds (from SRT last end time)
```

### Validation Script
```python
import pysrt
import soundfile as sf

# Load SRT and audio
subs = pysrt.open('test_sample.srt')
audio, sr = sf.read('generated_from_srt.wav')

# Calculate durations
srt_duration = subs[-1].end.ordinal / 1000.0
audio_duration = len(audio) / sr

print(f"SRT duration: {srt_duration:.2f}s")
print(f"Audio duration: {audio_duration:.2f}s")
print(f"Match: {abs(srt_duration - audio_duration) < 0.1}")
```

## Troubleshooting

### Q: Audio segments are cut off
**A**: Generated audio is too long for SRT time slot
- Solution: Extend subtitle duration in SRT file
- Or: Install librosa for automatic time-stretching

### Q: Large gaps in audio
**A**: SRT has wide time gaps between subtitles
- Solution: Edit SRT to reduce gaps
- This is now intentional - respects your SRT timing

### Q: Audio shorter than expected
**A**: Check SRT file - audio duration matches last subtitle end time
- Solution: Add more subtitles or extend last subtitle

## Performance Impact

- **Memory**: May increase (creates full-duration buffer)
- **CPU**: Similar (still ~1-2s per subtitle)
- **Quality**: Improved (better synchronization)
- **File Size**: May increase (silence is stored, not implied)

## Future Enhancements

Potential improvements:
1. Sparse audio storage (don't store silence)
2. Per-subtitle voice assignment
3. Subtitle preview in UI
4. Visual timeline editor
5. Real-time subtitle sync adjustment

## Support

For questions or issues:
1. Check [SRT_TIMING_GUIDE.md](./SRT_TIMING_GUIDE.md)
2. Review [SRT_FEATURE_README.md](./SRT_FEATURE_README.md)
3. Check logs at `logs/tts_server.log`
4. Verify librosa is installed: `pip list | grep librosa`

## Rollback (If Needed)

If you need the old behavior:
```bash
# Checkout previous version
git checkout HEAD~1 utils.py models.py ui/
# Restart server
docker-compose restart
```

## Summary

The SRT timing update brings professional-grade synchronization to the Chatterbox TTS Server. Audio now matches your subtitle timing exactly, making it perfect for video dubbing, narration, and any application requiring precise timing control.

🎉 **Update complete - enjoy perfectly timed audio generation!**
