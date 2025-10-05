# Audio File Saving to Outputs Folder

## Overview

Both the regular TTS endpoint (`/tts`) and the SRT TTS endpoint (`/tts/srt`) now automatically save generated audio files to the `outputs/` folder in addition to streaming them to the client.

## What Changed

### Before
- Audio was only streamed to the client as a download
- No persistent copy was saved on the server
- Outputs folder remained empty

### After
- Audio is both streamed **and** saved to `outputs/` folder
- Files persist on the server for later access
- Can be accessed via `/outputs/{filename}` URL

## File Naming Convention

### Regular TTS Endpoint
```
tts_output_YYYYMMDD_HHMMSS.{format}
```

**Example:**
```
tts_output_20251005_143025.wav
tts_output_20251005_143026.mp3
```

### SRT TTS Endpoint
```
tts_srt_{srt_filename}_{timestamp}.{format}
```

**Example:**
```
tts_srt_viture_20251005_143530.wav
tts_srt_subtitles_20251005_143600.mp3
```

## Location

All files are saved to:
```
/app/outputs/              # Inside Docker container
./outputs/                 # On host (if volume mounted)
```

## Accessing Saved Files

### Via File System
```bash
# List all generated files
ls -lh outputs/

# Play a file
mpv outputs/tts_srt_viture_20251005_143530.wav
```

### Via HTTP (If server is running)
```
http://localhost:8000/outputs/tts_srt_viture_20251005_143530.wav
```

### Via UI
The web UI automatically receives the file as a download, but you can also access it from the outputs folder.

## Logging

### Successful Save
```
INFO: Saved generated audio to: /app/outputs/tts_srt_viture_20251005_143530.wav
INFO: Successfully generated audio from SRT: tts_srt_viture_20251005_143530.wav, 2458624 bytes, 25 subtitles processed.
```

### Failed Save (Non-Fatal)
```
WARNING: Failed to save audio to outputs folder: [error details]
```

If saving fails, the audio will still be streamed to the user - the save operation is best-effort and won't interrupt generation.

## Storage Considerations

### Automatic Cleanup
Currently, there is **no automatic cleanup** of old files. Files will accumulate in the outputs folder.

### Manual Cleanup
```bash
# Remove files older than 7 days
find outputs/ -type f -mtime +7 -delete

# Remove all files
rm outputs/*

# Keep only the 10 most recent files
ls -t outputs/* | tail -n +11 | xargs rm --
```

### Disk Space Monitoring
```bash
# Check outputs folder size
du -sh outputs/

# Check available disk space
df -h /app/outputs/
```

## Configuration

The outputs directory is configured in `config.py`:

```python
def get_output_path(ensure_absolute=False):
    """Get the path to the outputs directory."""
    # Returns Path object to outputs folder
```

## Docker Volume Mounting

In `docker-compose-rocm.yml`, ensure outputs is mounted:

```yaml
volumes:
  - ./outputs:/app/outputs
```

This allows you to access generated files from the host machine.

## Use Cases

### 1. Archiving Generated Audio
Keep a history of all generated audio for later reference or re-use.

### 2. Batch Processing
Generate multiple audio files and process them later.

### 3. Debugging
Listen to generated files to debug issues with timing, speed, or quality.

### 4. Integration with Other Tools
Access generated files from other applications or scripts.

### 5. Sharing
Share generated audio files with others via direct file access.

## Implementation Details

### Code Location
- **Regular TTS**: `server.py` ~line 883
- **SRT TTS**: `server.py` ~line 1223

### Save Logic
```python
try:
    outputs_dir = get_output_path(ensure_absolute=True)
    output_file_path = outputs_dir / download_filename
    
    with open(output_file_path, 'wb') as f:
        f.write(encoded_audio_bytes)
    
    logger.info(f"Saved generated audio to: {output_file_path}")
except Exception as e_save:
    logger.warning(f"Failed to save audio to outputs folder: {e_save}")
    # Continue anyway - file will still be streamed to user
```

### Error Handling
- Save operation is wrapped in try-except
- Failures are logged as warnings, not errors
- Generation continues even if save fails
- User still receives the audio stream

## Testing

### 1. Generate Regular TTS Audio
```bash
curl -X POST "http://localhost:8000/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voice_mode": "predefined",
    "predefined_voice_id": "Gianna.wav"
  }' \
  -o test.wav

# Check outputs folder
ls -lh outputs/tts_output_*.wav
```

### 2. Generate SRT Audio
```bash
curl -X POST "http://localhost:8000/tts/srt" \
  -F "srt_file=@viture.srt" \
  -F "voice_mode=predefined" \
  -F "predefined_voice_id=Gianna.wav"

# Check outputs folder
ls -lh outputs/tts_srt_viture_*.wav
```

### 3. Verify via UI
1. Generate audio via web UI
2. Check `outputs/` folder
3. File should appear with timestamp
4. Access file via browser: `http://localhost:8000/outputs/{filename}`

## Troubleshooting

### Issue: Files not appearing in outputs folder
**Check:**
1. Docker volume is mounted correctly
2. Permissions on outputs folder (should be writable)
3. Check logs for save warnings
4. Ensure server restarted after code changes

**Solution:**
```bash
# Restart Docker container
docker-compose -f docker-compose-rocm.yml restart

# Check logs
docker-compose -f docker-compose-rocm.yml logs | grep "Saved generated"

# Fix permissions
chmod 755 outputs/
```

### Issue: Permission denied when saving
**Cause:** Outputs folder not writable by container

**Solution:**
```bash
# Make folder writable
chmod 777 outputs/

# Or fix ownership
sudo chown -R 1000:1000 outputs/
```

### Issue: Disk full
**Cause:** Too many generated files

**Solution:**
```bash
# Clean old files
find outputs/ -type f -mtime +1 -delete

# Check disk space
df -h
```

## Future Enhancements

Potential improvements:
1. **Automatic cleanup**: Delete files older than X days
2. **Configurable save location**: Per-user or per-session folders
3. **Database tracking**: Keep record of all generated files
4. **API to list files**: Endpoint to query available outputs
5. **Compression**: Automatically compress old files
6. **Cloud storage**: Option to save to S3/Azure/GCS

## Summary

✅ **Regular TTS**: Saves to `outputs/tts_output_{timestamp}.{format}`
✅ **SRT TTS**: Saves to `outputs/tts_srt_{srt_name}_{timestamp}.{format}`
✅ **Non-blocking**: Save failures don't interrupt generation
✅ **Persistent**: Files remain until manually deleted
✅ **Accessible**: Via file system or HTTP

Now all your generated audio files will be automatically saved to the outputs folder for easy access! 🎉
