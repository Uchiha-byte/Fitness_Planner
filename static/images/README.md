# Images Directory Structure

This directory contains all images used in the ZFIT application. Images are organized into subdirectories based on their purpose.

## Directory Structure

```
images/
├── features/          # Images for feature illustrations
├── exercises/         # Exercise demonstration images
├── backgrounds/       # Background images and patterns
├── icons/            # UI icons and small graphics
└── uploads/          # Temporary storage for user uploads
```

## Image Guidelines

1. **Format Requirements**
   - Use WebP format for best performance when possible
   - Fallback to optimized JPG/PNG when WebP is not suitable
   - Keep file sizes under 200KB for optimal loading

2. **Naming Convention**
   - Use lowercase letters
   - Separate words with hyphens
   - Include dimensions in filename (e.g., hero-banner-1920x1080.webp)

3. **Optimization**
   - Compress all images before adding
   - Maintain appropriate aspect ratios
   - Provide multiple sizes for responsive design

4. **Categories**
   - features/: Main feature illustrations and screenshots
   - exercises/: Exercise demonstration images and gifs
   - backgrounds/: Hero images and section backgrounds
   - icons/: Navigation and UI icons
   - uploads/: Temporary user uploaded images (auto-cleaned) 