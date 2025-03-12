from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.models.qr_code import QRCode
from app.models.user import User
from app.utils.decorators import user_required
import csv
import io
from datetime import datetime
import os

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/dashboard')
@login_required
@user_required
def dashboard():
    qr_codes = QRCode.query.filter_by(user_id=current_user.id).order_by(QRCode.created_at.desc()).all()
    return render_template('user/dashboard.html', title='User Dashboard', qr_codes=qr_codes)

@user.route('/history')
@login_required
@user_required
def history():
    qr_codes = QRCode.query.filter_by(user_id=current_user.id).order_by(QRCode.created_at.desc()).all()
    return render_template('user/history.html', title='QR Code History', qr_codes=qr_codes)

@user.route('/profile', methods=['GET', 'POST'])
@login_required
@user_required
def profile():
    from app.forms.profile import ProfileForm
    
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.theme = form.theme.data
        
        if form.new_password.data:
            from werkzeug.security import generate_password_hash
            current_user.password = generate_password_hash(form.new_password.data)
            
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.theme.data = current_user.theme
    
    return render_template('user/profile.html', title='User Profile', form=form)

@user.route('/export-history')
@login_required
@user_required
def export_history():
    qr_codes = QRCode.query.filter_by(user_id=current_user.id).order_by(QRCode.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Content', 'QR Type', 'Created At', 'Size', 'Color'])
    
    for qr in qr_codes:
        writer.writerow([
            qr.id, 
            qr.content, 
            qr.qr_type, 
            qr.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            qr.size,
            qr.color
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'qr_code_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@user.route('/change-theme', methods=['POST'])
@login_required
@user_required
def change_theme():
    theme = request.form.get('theme')
    redirect_url = request.form.get('redirect_url') or request.referrer or url_for('user.profile')
    
    if theme in ['light', 'dark', 'system']:
        current_user.theme = theme
        db.session.commit()
        
        # Set a theme cookie for consistent display across pages
        response = redirect(redirect_url)
        
        # Set system preference cookie if needed
        if theme == 'system':
            # We won't set the actual theme value here as it will be determined by JS
            response.set_cookie('theme_preference', 'system', max_age=31536000)  # 1 year
        else:
            response.set_cookie('theme_preference', theme, max_age=31536000)  # 1 year
            
        return response
    
    return redirect(redirect_url) 