# Bug Fix: SRT Mode Not Working

## Issue
When "SRT File Upload" mode was selected and "Generate from SRT" button was clicked, the system was generating audio from the text in the "Text Input" tab instead of using the uploaded SRT file.

## Root Cause
There were **two event listeners** attached to the generate button:
1. **Original handler** (line ~678): Didn't know about SRT mode, always processed text input
2. **SRT handler** (line ~1135): Added later for SRT support, but ran second

Both handlers were executing, but the original one ran first and prevented the SRT handler from being reached.

## Solution
Integrated SRT mode detection into the **main/original event listener** at line ~678:

### Changes Made

**File: `ui/script.js`**

1. **Updated main generate button handler** (~line 678):
   ```javascript
   // Added input mode detection
   const inputModeRadio = document.querySelector('input[name="input_mode"]:checked');
   const currentInputMode = inputModeRadio ? inputModeRadio.value : 'text';
   
   // Handle SRT mode first
   if (currentInputMode === 'srt') {
       // Validate SRT file and voice selection
       // Call submitSRTRequest()
       return;
   }
   
   // Original text mode logic continues...
   ```

2. **Removed duplicate event listener** (~line 1160):
   - Deleted the second `generateBtn.addEventListener()` block
   - Kept only the `submitSRTRequest()` function

3. **Added debug logging**:
   ```javascript
   console.log('Input mode:', currentInputMode);
   console.log('SRT mode detected, selectedSRTFile:', selectedSRTFile);
   ```

## Testing
1. Refresh the browser (Ctrl+F5 / Cmd+Shift+R)
2. Select "SRT File Upload" mode
3. Upload an SRT file (e.g., `test_sample.srt`)
4. Select a voice
5. Click "Generate from SRT"
6. **Expected**: SRT file should be processed, not text input
7. **Verify**: Check browser console for "Input mode: srt" log

## Verification
- ✅ No syntax errors in script.js
- ✅ Single event listener on generate button
- ✅ Mode detection logic at start of handler
- ✅ Early return for SRT mode
- ✅ Debug logging added

## Files Modified
- `ui/script.js`: Consolidated event handlers, added mode detection

## No Server Restart Required
This is a client-side JavaScript fix. Simply **refresh the browser** to load the updated script.

---

**Status**: Fixed ✅
**Date**: October 4, 2025
