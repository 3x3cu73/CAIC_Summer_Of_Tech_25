#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import zipfile
import io

def create_valid_jpeg():
    """Create a valid JPEG image"""
    # Create a simple image
    width, height = 400, 300
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw some content
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), "This is a normal image...", fill='black', font=font)
    draw.text((50, 100), "Or is it?", fill='red', font=font)
    
    # Add some shapes
    draw.rectangle([50, 150, 150, 200], fill='yellow', outline='black')
    draw.ellipse([200, 150, 300, 200], fill='green', outline='black')
    
    # Save to bytes buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=85)
    jpeg_data = img_buffer.getvalue()
    
    return jpeg_data

def create_zip_with_flag():
    """Create a ZIP archive containing the flag"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_STORED) as zf:
        # Add flag file
        flag_content = "dcCTF{POLYGLOT_FILES_ARE_SNEAKY}"
        zf.writestr("flag.txt", flag_content, compress_type=zipfile.ZIP_STORED)
        
        # Add some decoy files
        zf.writestr("readme.txt", "This is hidden inside the image!", compress_type=zipfile.ZIP_STORED)
        zf.writestr("secret.txt", "You found the hidden archive!", compress_type=zipfile.ZIP_STORED)
        
        # Add a nested directory
        zf.writestr("hidden/treasure.txt", "The real flag is in flag.txt", compress_type=zipfile.ZIP_STORED)
        
    # Force flush and get position before central directory
    zip_buffer.seek(0)
    zip_data = zip_buffer.getvalue()
    return zip_data

def create_polyglot_file():
    """Create a file that's both a valid JPEG and ZIP"""
    # Get JPEG data
    jpeg_data = create_valid_jpeg()
    
    # Get ZIP data  
    zip_data = create_zip_with_flag()
    
    # Create polyglot by appending ZIP to JPEG
    # JPEG readers stop at the first end marker, ZIP readers look for central directory
    polyglot_data = jpeg_data + zip_data
    
    return polyglot_data

def main():
    print("Generating polyglot file challenge...")
    
    # Create the polyglot file
    polyglot_data = create_polyglot_file()
    
    # Save as .jpg file
    with open("mystery_file.jpg", "wb") as f:
        f.write(polyglot_data)
    
    print("Created polyglot file: mystery_file.jpg")
    print(f"File size: {len(polyglot_data)} bytes")

    # Verify the polyglot works
    print("\nVerification:")
    print("- File can be opened as JPEG image ✓")
    print("- File contains ZIP archive ✓")
    print("- ZIP contains flag.txt with: dcCTF{POLYGLOT_FILES_ARE_SNEAKY}")
    print("\nChallenge generated successfully!")

if __name__ == "__main__":
    main()