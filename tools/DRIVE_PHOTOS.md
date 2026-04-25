# Google Drive Photo Downloads

## Current Issue

The file IDs available are **Google Drive shortcuts**, which download as HTML redirects instead of actual image files.

## Solution: Manual Download

### Quick Option - Download from Google Drive Directly

1. Open [Google Drive](https://drive.google.com)
2. Look for the article photo folders or files
3. Right-click on each photo → Download
4. Save to the corresponding article folder:
   - `editions/2026-04-26/second-presbyterian/photo-XX.jpg`
   - `editions/2026-04-26/rush-hospital/photo-XX.jpg`

### Option 2 - Use File IDs to Access

**Second Presbyterian (Photos 1-8):**
- Photo 1: https://drive.google.com/file/d/1uqvh2-hSX8KUxK4fyFoX3gfA3Yuowti1/view
- Photo 2: https://drive.google.com/file/d/1HuvJ0eCPlt6BQTcNXh7BAAqMRPN1CaPA/view
- Photo 3: https://drive.google.com/file/d/1_y9HQmSqBm8v9p3Xq67YFo-NINksfR1i/view
- Photo 4: https://drive.google.com/file/d/1NnpZ-0VnXbB3epAB-6m9UlQtMsxTDjW0/view
- Photo 5: https://drive.google.com/file/d/1PWICyTPS6wa26pTHX5Ik8yhSy_Xpxh7L/view
- Photo 6: https://drive.google.com/file/d/1-MyKF6g8VaFF871Uwkx4tEpSoPOGLnba/view
- Photo 7: https://drive.google.com/file/d/1cHMCutMbT-Aqf7-CddEYZa2VWXHp1ADi/view
- Photo 8: https://drive.google.com/file/d/15bq3-nPv2MpKUTFiwVqkVKxdvVX4Wr3e/view

**Rush Hospital (Photos 9-12):**
- Photo 9: https://drive.google.com/file/d/1e0a60gRp-X80ZGmY_ZgM2wEl9XQOfpdM/view
- Photo 10: https://drive.google.com/file/d/13nMJ88lM7IDogXxdk8ZBC9ogL6Eb7Afj/view
- Photo 11: https://drive.google.com/file/d/1KpKKswF39lgyEIPjGYajcWTya7PtKib4/view
- Photo 12: https://drive.google.com/file/d/1HjWPFHG20B_mao33ppMHLyR6e1rwY6n9/view

For each link:
1. Click the link → Opens Google Drive
2. Click Download icon (↓) at top right
3. Save to `editions/2026-04-26/[article]/photo-XX.jpg`

### Option 3 - Request Actual Image Files

These IDs are shortcuts pointing to actual files elsewhere. To get the actual image file IDs:

1. Ask contributors: "Can you share the actual image file IDs (not shortcuts)?"
2. Or find the source folder in Google Drive where originals are stored
3. Get the real file IDs and update this document

## Running the Script

Once you have the correct file IDs (not shortcuts), update the `DRIVE_FILES` dict in `download_drive_photos.py` and run:

```bash
python3 tools/download_drive_photos.py --edition 2026-04-26
```

## Why This Happens

Google Drive shortcuts are pointers to other files. When curl tries to download a shortcut ID directly, Google redirects with an HTML page asking for authentication or showing folder view, not the actual file bytes.

**Real image file IDs** download directly as JPEG bytes without redirects.

---

*Last updated: April 25, 2026*
