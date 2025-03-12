from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.models.qr_code import QRCode
from app.utils.qr_generator import generate_qr_code, generate_qr_with_logo
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
import base64
import io

qr = Blueprint('qr', __name__, url_prefix='/qr')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@qr.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    if request.method == 'POST':
        content = request.form.get('content')
        size = request.form.get('size', '200x200')
        color = request.form.get('color', '#000000')
        logo = request.files.get('logo')
        
        if not content:
            flash('Please provide content for the QR code.', 'warning')
            return redirect(url_for('qr.generator'))
        
        qr_uuid = str(uuid.uuid4())
        qr_filename = f"{qr_uuid}.png"
        qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], qr_filename)
        
        # Process logo if it exists
        logo_path = None
        if logo and logo.filename and allowed_file(logo.filename):
            logo_filename = secure_filename(f"{qr_uuid}_logo.{logo.filename.rsplit('.', 1)[1].lower()}")
            logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename)
            logo.save(logo_path)
            
            # Generate QR with logo
            qr_image = generate_qr_with_logo(content, logo_path, color, tuple(map(int, size.split('x'))))
        else:
            # Generate simple QR code
            qr_image = generate_qr_code(content, color, tuple(map(int, size.split('x'))))
        
        # Save QR code
        qr_image.save(qr_path)
        
        # Save QR code to database
        new_qr = QRCode(
            user_id=current_user.id,
            content=content,
            qr_type='standard' if logo_path is None else 'logo',
            file_path=qr_filename,
            created_at=datetime.utcnow(),
            size=size,
            color=color,
            logo_path=os.path.basename(logo_path) if logo_path else None
        )
        db.session.add(new_qr)
        db.session.commit()
        
        flash('QR code has been generated successfully!', 'success')
        return redirect(url_for('qr.view', qr_id=new_qr.id))
    
    return render_template('qr/generator.html', title='QR Code Generator')

@qr.route('/view/<int:qr_id>')
@login_required
def view(qr_id):
    qr_code = QRCode.query.get_or_404(qr_id)
    
    # Ensure the QR code belongs to the current user or user is admin
    if qr_code.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this QR code.', 'danger')
        return redirect(url_for('user.dashboard' if not current_user.is_admin else 'admin.dashboard'))
    
    qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], qr_code.file_path)
    
    # Convert QR code to base64 for display
    with open(qr_path, 'rb') as qr_file:
        encoded_qr = base64.b64encode(qr_file.read()).decode('utf-8')
    
    return render_template('qr/view.html', title='View QR Code', qr_code=qr_code, encoded_qr=encoded_qr)

@qr.route('/download/<int:qr_id>')
@login_required
def download(qr_id):
    qr_code = QRCode.query.get_or_404(qr_id)
    
    # Ensure the QR code belongs to the current user or user is admin
    if qr_code.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to download this QR code.', 'danger')
        return redirect(url_for('user.dashboard' if not current_user.is_admin else 'admin.dashboard'))
    
    qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], qr_code.file_path)
    
    if not os.path.exists(qr_path):
        flash('QR code file not found.', 'danger')
        return redirect(url_for('qr.view', qr_id=qr_id))
    
    return send_file(qr_path, as_attachment=True, download_name=f'qrcode_{qr_id}.png')

@qr.route('/delete/<int:qr_id>', methods=['POST'])
@login_required
def delete(qr_id):
    qr_code = QRCode.query.get_or_404(qr_id)
    
    # Ensure the QR code belongs to the current user or user is admin
    if qr_code.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this QR code.', 'danger')
        return redirect(url_for('user.dashboard' if not current_user.is_admin else 'admin.dashboard'))
    
    # Delete the files
    qr_path = os.path.join(current_app.config['UPLOAD_FOLDER'], qr_code.file_path)
    if os.path.exists(qr_path):
        os.remove(qr_path)
    
    if qr_code.logo_path:
        logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], qr_code.logo_path)
        if os.path.exists(logo_path):
            os.remove(logo_path)
    
    # Delete from database
    db.session.delete(qr_code)
    db.session.commit()
    
    flash('QR code has been deleted!', 'success')
    if current_user.is_admin:
        return redirect(url_for('admin.qr_codes'))
    return redirect(url_for('user.history'))

@qr.route('/preview', methods=['POST'])
def preview():
    """Generate a QR code preview and return it as a base64 encoded image."""
    try:
        content = request.form.get('content')
        size = request.form.get('size', '200x200')
        color = request.form.get('color', '#000000')
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        # Generate QR code
        qr_image = generate_qr_code(content, color, tuple(map(int, size.split('x'))))
        
        # Convert to base64
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({'image': f'data:image/png;base64,{img_str}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 