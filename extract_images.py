#!/usr/bin/env python3
import re
import base64
import os

# Read the HTML file
html_file = "/tmp/cc-agent/64068117/project/newbayit_final (4).html"
output_dir = "/tmp/cc-agent/64068117/project/images/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read HTML content
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find all base64 image data URLs
pattern = r'data:image/(png|jpg|jpeg|gif|webp);base64,([A-Za-z0-9+/=]+)'
matches = re.findall(pattern, html_content)

print(f"Found {len(matches)} base64-encoded images")
print()

# Descriptive names for the 7 images (in order of appearance)
image_names = [
    "logo.jpg",
    "journey-card.png",
    "about-photo.png",
    "roadmap-image.png",
    "services-card.png",
    "contact-photo.png",
    "footer-logo.png"
]

total_base64_size = 0
total_file_size = 0
extracted_images = []

for i, (img_format, base64_data) in enumerate(matches):
    if i >= len(image_names):
        print(f"Warning: Found more images than expected ({len(matches)} vs {len(image_names)})")
        break

    # Calculate base64 size
    base64_size = len(base64_data)
    total_base64_size += base64_size

    # Decode base64 data
    try:
        image_data = base64.b64decode(base64_data)

        # Use the descriptive name
        output_filename = image_names[i]
        output_path = os.path.join(output_dir, output_filename)

        # Write image file
        with open(output_path, 'wb') as img_file:
            img_file.write(image_data)

        file_size = len(image_data)
        total_file_size += file_size

        extracted_images.append({
            'name': output_filename,
            'base64_size': base64_size,
            'file_size': file_size,
            'format': img_format
        })

        print(f"Extracted: {output_filename}")
        print(f"  Format: {img_format}")
        print(f"  Base64 size: {base64_size:,} bytes ({base64_size/1024:.2f} KB)")
        print(f"  File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print(f"  Savings: {base64_size - file_size:,} bytes ({(base64_size - file_size)/1024:.2f} KB)")
        print()

    except Exception as e:
        print(f"Error extracting image {i+1}: {e}")
        print()

# Summary
print("=" * 60)
print("EXTRACTION SUMMARY")
print("=" * 60)
print(f"Total images extracted: {len(extracted_images)}")
print(f"Total base64 size: {total_base64_size:,} bytes ({total_base64_size/1024:.2f} KB)")
print(f"Total file size: {total_file_size:,} bytes ({total_file_size/1024:.2f} KB)")
print(f"Total savings: {total_base64_size - total_file_size:,} bytes ({(total_base64_size - total_file_size)/1024:.2f} KB)")
print(f"Compression ratio: {(total_file_size/total_base64_size)*100:.2f}%")
print()

# Verify all files exist
print("Verifying extracted files:")
all_exist = True
for img in extracted_images:
    img_path = os.path.join(output_dir, img['name'])
    exists = os.path.exists(img_path)
    status = "✓" if exists else "✗"
    print(f"  {status} {img['name']} - {os.path.getsize(img_path) if exists else 0:,} bytes")
    if not exists:
        all_exist = False

print()
if all_exist:
    print("SUCCESS: All 7 images successfully extracted!")
else:
    print("WARNING: Some images were not extracted successfully")
