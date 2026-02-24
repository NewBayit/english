#!/bin/bash

# Replace remaining base64 images with external paths in both HTML files

for file in "index.html" "es/index.html"; do
  echo "Processing $file..."

  # Create backup
  cp "$file" "$file.bak"

  # Replace card images by looking for specific patterns
  # Line 292 - Journey card
  sed -i 's|<img class="jcard-img" src="data:image/[^"]*"|<img class="jcard-img" src="/images/journey-card.png" loading="lazy"|' "$file"

  # Line 307 - About photo
  sed -i 's|<img class="about-img" src="data:image/[^"]*"|<img class="about-img" src="/images/about-photo.png" loading="lazy"|' "$file"

  # Line 326 - Roadmap image
  sed -i 's|<img class="roadmap-img" src="data:image/[^"]*"|<img class="roadmap-img" src="/images/roadmap-image.png" loading="lazy"|' "$file"

  # Line 360 - Services card
  sed -i 's|<img class="scard-img" src="data:image/[^"]*"|<img class="scard-img" src="/images/services-card.png" loading="lazy"|' "$file"

  # Line 409 - Contact photo
  sed -i 's|<img class="contact-circle" src="data:image/[^"]*"|<img class="contact-circle" src="/images/contact-photo.png" loading="lazy"|' "$file"

  # Generic fallback for any remaining base64 images
  sed -i 's|src="data:image/jpeg;base64,[^"]*"|src="/images/logo.jpg"|g' "$file"
  sed -i 's|src="data:image/png;base64,[^"]*"|src="/images/logo.jpg"|g' "$file"

  echo "✓ Completed $file"
done

echo "All base64 images replaced!"
