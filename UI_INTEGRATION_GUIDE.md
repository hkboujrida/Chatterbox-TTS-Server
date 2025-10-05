# SRT to Audio - UI Integration Guide

## Overview

The SRT to Audio generation feature has been fully integrated into the Chatterbox TTS Server web UI. Users can now easily convert subtitle files to narrated audio directly through the browser interface.

## UI Changes

### 1. Input Mode Selector

A new **Input Mode** selector has been added at the top of the generation form with two options:

- **Text Input** (Default): Traditional text-to-speech generation
- **SRT File Upload**: Upload and process SRT subtitle files

### 2. SRT Upload Section

When SRT mode is selected, the UI displays:

#### File Upload Controls
- **Choose SRT File** button: Opens file browser to select `.srt` files
- **File name display**: Shows the name of the selected file
- **File info card**: Displays file details after upload:
  - Filename
  - Number of subtitle entries detected

#### Timing Information
- **Timing Preservation Info**: Blue info box explaining that audio segments will be placed at exact SRT timestamps
- **Automatic Gap Calculation**: No manual silence configuration needed

### 3. Dynamic Button Text

The generate button text changes based on the selected mode:
- **Text mode**: "Generate Speech"
- **SRT mode**: "Generate from SRT"

### 4. Conditional Controls

- Text-specific controls (Split text, Chunk size) are hidden in SRT mode
- All standard TTS parameters remain available in both modes
- Voice selection (predefined/clone) works the same in both modes

## User Workflow

### Basic SRT Generation

1. **Select SRT Mode**
   - Click on "SRT File Upload" in the Input Mode selector

2. **Upload SRT File**
   - Click "Choose SRT File" button
   - Select your `.srt` subtitle file
   - UI will display the filename and detected subtitle count

3. **Configure Voice**
   - Select voice mode (Predefined or Clone)
   - Choose a voice from the available options

4. **Adjust Parameters** (Optional)
   - Temperature, Exaggeration, CFG Weight, etc.
   - Output format (WAV, MP3, Opus)
   - **Note**: Timing is now automatic from SRT file timestamps

5. **Generate**
   - Click "Generate from SRT"
   - Wait for processing (shows progress overlay)
   - Audio player appears when complete

6. **Play/Download**
   - Use the built-in waveform player
   - Download the generated audio file

### Advanced Usage

#### Timing Control
The feature now **preserves exact SRT timing**:
- Audio segments are placed at precise timestamps from your SRT file
- Gaps between subtitles are automatically calculated
- No manual silence configuration needed
- Perfect for video dubbing and synchronization

**Example:**
```srt
1
00:00:00,000 --> 00:00:03,000
First subtitle.

2
00:00:03,500 --> 00:00:07,000
Second subtitle.
```
Results in:
- 0-3s: First audio
- 3-3.5s: Automatic 0.5s silence
- 3.5-7s: Second audio
- Total: Exactly 7 seconds

For more details, see [SRT_TIMING_GUIDE.md](./SRT_TIMING_GUIDE.md).

#### Multiple Voices
- Currently, one voice is used for all subtitles
- Future enhancement: Per-subtitle voice assignment

#### Output Formats
- **WAV**: Highest quality, largest file size
- **MP3**: Good balance of quality and size
- **Opus**: Best compression, modern format

## Features

### Validation
- File type checking (must be `.srt`)
- Voice selection validation
- Real-time subtitle count detection
- Empty file handling

### Error Handling
- Clear error messages for invalid files
- Server-side parsing errors displayed
- Network error handling
- Failed subtitle synthesis handling (replaced with silence)

### Progress Tracking
- Loading overlay with status messages
- Generation time display
- Cancellable operations

### Audio Playback
- WaveSurfer.js visualization
- Play/Pause controls
- Duration display
- Download button with correct file extension

## UI Elements Reference

### New HTML Elements

```html
<!-- Input Mode Selector -->
<input type="radio" name="input_mode" value="text" checked>
<input type="radio" name="input_mode" value="srt">

<!-- SRT Upload Section -->
<div id="srt-input-section" class="mb-5 hidden">
  <input type="file" id="srt-file-input" accept=".srt" class="hidden">
  <button id="srt-file-upload-btn">Choose SRT File</button>
  <span id="srt-file-name">No file selected</span>
  
  <!-- File Info Card -->
  <div id="srt-file-info" class="hidden">
    <span id="srt-file-display-name"></span>
    <p id="srt-subtitle-count"></p>
  </div>
  
  <!-- Silence Slider -->
  <input type="range" id="silence-between-segments" 
         min="0.0" max="5.0" step="0.1" value="0.5">
  <span id="silence-value">0.5</span>
</div>
```

### JavaScript Variables

```javascript
let selectedSRTFile = null;  // Stores the selected SRT file
const inputModeRadios = ...  // Input mode radio buttons
const srtFileInput = ...     // File input element
const silenceBetweenSegments = ...  // Silence slider
```

### Key Functions

- `submitSRTRequest()`: Handles SRT form submission
- Input mode change handler: Toggles between text/SRT sections
- File selection handler: Validates and previews SRT files
- Generate button handler: Routes to appropriate submission function

## Styling

The SRT feature uses existing Tailwind CSS classes for consistency:
- `.voice-mode-option`: For input mode selector
- `.btn-import`: For file upload button
- `.slider-base`: For silence duration slider
- Standard card and info box styles

## Tips & Tricks Section

Updated to include:
> **NEW!** Use **SRT File Upload** mode to convert subtitle files into narrated audio with proper timing.

## Browser Compatibility

- **File API**: All modern browsers
- **FormData**: Full support
- **Blob/URL handling**: Full support
- **Input[type="file"]**: Universal support

## Accessibility

- File input has `aria-label`
- Buttons have descriptive text
- Status messages use appropriate ARIA roles
- Keyboard navigation supported

## Performance Considerations

### Client-Side
- Minimal file parsing (just counting entries)
- No heavy processing in browser
- Efficient FormData upload

### Server-Side
- Progress shown via loading overlay
- Long operations cancellable
- Status messages during processing

## Testing Checklist

- [ ] Mode switching works correctly
- [ ] File upload triggers properly
- [ ] File validation prevents non-SRT files
- [ ] Subtitle count displays accurately
- [ ] Silence slider updates value display
- [ ] Generate button text changes with mode
- [ ] Voice selection works in SRT mode
- [ ] All TTS parameters are sent correctly
- [ ] Audio player appears after generation
- [ ] Download button has correct filename
- [ ] Error messages display properly
- [ ] Loading overlay appears and dismisses correctly

## Known Limitations

1. **Single Voice**: Currently, all subtitles use the same voice
2. **No Preview**: Subtitles are not displayed before generation
3. **No Editing**: Cannot edit subtitle text in UI (must edit file)
4. **No Timing Adjustment**: Original subtitle timings are approximated

## Future Enhancements

Potential improvements for future versions:

1. **Subtitle Preview**: Display subtitle entries before generation
2. **Per-Subtitle Voice**: Assign different voices to different entries
3. **Inline Editing**: Edit subtitle text in the UI
4. **Batch Upload**: Process multiple SRT files at once
5. **Progress Bar**: Show per-subtitle generation progress
6. **Timing Modes**: Options for timing preservation strategies
7. **Export Options**: Save with timestamps, create chapters
8. **SRT Editor**: Built-in subtitle editor

## Troubleshooting

### Issue: File not uploading
**Solution**: Check file has `.srt` extension, try different browser

### Issue: Subtitle count shows 0
**Solution**: Ensure SRT file format is valid, check for UTF-8 encoding

### Issue: Generation takes very long
**Solution**: Expected for large SRT files (1-2s per subtitle), wait or cancel

### Issue: Generated audio too long/short
**Solution**: Adjust "Silence Between Segments" slider

### Issue: Audio quality issues
**Solution**: Try different voices, adjust temperature/exaggeration

## API Endpoint Used

The UI calls:
```
POST /tts/srt
Content-Type: multipart/form-data
```

See `SRT_FEATURE_README.md` for complete API documentation.

## Files Modified

1. **ui/index.html**
   - Added input mode selector
   - Added SRT upload section
   - Updated tips section
   - Modified generate button structure

2. **ui/script.js**
   - Added SRT mode handling
   - Added file upload logic
   - Added `submitSRTRequest()` function
   - Modified generate button handler
   - Added mode switching logic

## Screenshots

### Text Mode (Default)
```
[Input Mode: ● Text Input  ○ SRT File Upload]
[Text area with "Enter text here..."]
[Generate Speech button]
```

### SRT Mode
```
[Input Mode: ○ Text Input  ● SRT File Upload]
[Choose SRT File button] [filename.srt]
[File info: 5 subtitle entries detected]
[Silence Between Segments: 0.5s slider]
[Generate from SRT button]
```

## Summary

The SRT to Audio feature is now fully integrated into the web UI, providing a seamless experience for converting subtitle files to narrated audio. All existing features (voice selection, parameter tuning, audio playback) work harmoniously with the new SRT mode.
