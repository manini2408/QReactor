import qrcode
from PIL import Image
import os
import colorsys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_qr_code(data, color='#000000', size=(200, 200)):
    """Generate a basic QR code with custom color and size."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Convert color from hex to RGB
    fill_color = hex_to_rgb(color)
    back_color = (255, 255, 255)  # White background
    
    # Create QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Resize the image if needed
    if img.size != size:
        img = img.resize(size, Image.LANCZOS)
    
    return img

def generate_qr_with_logo(data, logo_path, color='#000000', size=(200, 200)):
    """Generate a QR code with a logo in the center."""
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Convert color from hex to RGB
    fill_color = hex_to_rgb(color)
    back_color = (255, 255, 255)  # White background
    
    # Create QR code image
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_img = qr_img.convert('RGBA')
    
    # Load logo and resize
    try:
        logo = Image.open(logo_path)
        logo = logo.convert('RGBA')
        
        # Calculate logo size (25% of QR code)
        logo_size = (qr_img.size[0] // 4, qr_img.size[1] // 4)
        logo = logo.resize(logo_size, Image.LANCZOS)
        
        # Calculate position to place logo at center
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        
        # Place logo on QR code
        qr_img.paste(logo, pos, logo)
        
    except Exception as e:
        print(f"Error adding logo to QR code: {e}")
    
    # Resize final image if needed
    if qr_img.size != size:
        qr_img = qr_img.resize(size, Image.LANCZOS)
    
    return qr_img 