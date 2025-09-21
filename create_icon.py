"""
Create a simple icon for the application
"""

from PIL import Image, ImageDraw
import os

def create_icon():
    """Create a simple application icon"""
    # Create a 256x256 image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a gradient background circle
    center = size // 2
    radius = size // 2 - 20
    
    # Draw outer circle (dark blue)
    draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                fill=(25, 50, 100, 255), outline=(100, 150, 255, 255), width=4)
    
    # Draw inner circle (blue gradient effect)
    inner_radius = radius - 30
    draw.ellipse([center-inner_radius, center-inner_radius, center+inner_radius, center+inner_radius], 
                fill=(50, 100, 200, 255))
    
    # Draw "G" for GameBoost
    font_size = size // 3
    # Simple geometric G shape
    g_width = font_size
    g_height = font_size
    g_x = center - g_width // 2
    g_y = center - g_height // 2
    
    # Draw G outline
    draw.rectangle([g_x, g_y, g_x + g_width, g_y + 20], fill=(255, 255, 255, 255))  # Top
    draw.rectangle([g_x, g_y, g_x + 20, g_y + g_height], fill=(255, 255, 255, 255))  # Left
    draw.rectangle([g_x, g_y + g_height - 20, g_x + g_width, g_y + g_height], fill=(255, 255, 255, 255))  # Bottom
    draw.rectangle([g_x + g_width - 20, g_y + g_height // 2, g_x + g_width, g_y + g_height], fill=(255, 255, 255, 255))  # Right bottom
    draw.rectangle([g_x + g_width // 2, g_y + g_height // 2, g_x + g_width, g_y + g_height // 2 + 20], fill=(255, 255, 255, 255))  # Middle
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Save as PNG
    img.save('assets/icon.png', 'PNG')
    
    # Save as ICO (Windows icon)
    # Create multiple sizes for ICO
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    
    for icon_size in sizes:
        resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Save as ICO file
    icons[0].save('assets/icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    
    print("Icon created successfully!")
    print("- PNG: assets/icon.png")
    print("- ICO: assets/icon.ico")

if __name__ == "__main__":
    create_icon()