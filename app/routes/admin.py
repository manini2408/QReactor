from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.models.qr_code import QRCode
from app.models.user import User
from app.models.feedback import Feedback
from app.utils.decorators import admin_required
from werkzeug.security import generate_password_hash
import csv
import io
from datetime import datetime
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get counts for dashboard
    user_count = User.query.filter_by(is_admin=False).count()
    qr_count = QRCode.query.count()
    feedback_count = Feedback.query.count()
    
    # Get recent activity
    recent_users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(5).all()
    recent_qr_codes = QRCode.query.order_by(QRCode.created_at.desc()).limit(5).all()
    recent_feedback = Feedback.query.order_by(Feedback.submitted_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html', 
        title='Admin Dashboard',
        user_count=user_count,
        qr_count=qr_count,
        feedback_count=feedback_count,
        recent_users=recent_users,
        recent_qr_codes=recent_qr_codes,
        recent_feedback=recent_feedback
    )

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', title='User Management', users=users)

@admin.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    from app.forms.user import UserForm
    
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            is_admin=form.is_admin.data,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        flash('User has been created!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/create_user.html', title='Create User', form=form)

@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    from app.forms.user import UserEditForm
    
    user = User.query.get_or_404(user_id)
    form = UserEditForm()
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
            
        db.session.commit()
        flash('User has been updated!', 'success')
        return redirect(url_for('admin.users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.is_admin.data = user.is_admin
    
    return render_template('admin/edit_user.html', title='Edit User', form=form, user=user)

@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/feedback')
@login_required
@admin_required
def feedback():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    sort = request.args.get('sort', 'date_desc')
    
    # Build query
    query = Feedback.query
    
    # Apply search filter
    if search:
        query = query.filter(
            Feedback.subject.ilike(f'%{search}%') | 
            Feedback.message.ilike(f'%{search}%') | 
            Feedback.email.ilike(f'%{search}%') |
            Feedback.name.ilike(f'%{search}%')
        )
    
    # Apply status filter
    if status:
        query = query.filter(Feedback.status == status)
    
    # Apply sorting
    if sort == 'date_asc':
        query = query.order_by(Feedback.submitted_at.asc())
    else:  # default: date_desc
        query = query.order_by(Feedback.submitted_at.desc())
    
    # Paginate the results
    per_page = 5
    feedback_items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'admin/feedback.html', 
        title='Feedback Management',
        feedback_items=feedback_items
    )

@admin.route('/feedback/delete/<int:feedback_id>', methods=['POST'])
@login_required
@admin_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback has been deleted!', 'success')
    return redirect(url_for('admin.feedback'))

@admin.route('/feedback/mark/<int:feedback_id>/<string:status>', methods=['POST'])
@login_required
@admin_required
def mark_feedback(feedback_id, status):
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if status in ['new', 'read', 'responded']:
        feedback.status = status
        db.session.commit()
        status_text = status.capitalize()
        flash(f'Feedback has been marked as {status_text}!', 'success')
    
    return redirect(url_for('admin.feedback'))

@admin.route('/qr-codes')
@login_required
@admin_required
def qr_codes():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    user_id = request.args.get('user', '')
    sort = request.args.get('sort', 'created_desc')
    
    # Build query
    query = QRCode.query
    
    # Apply search filter
    if search:
        query = query.filter(QRCode.data.ilike(f'%{search}%'))
    
    # Apply user filter
    if user_id:
        query = query.filter(QRCode.user_id == user_id)
    
    # Apply sorting
    if sort == 'created_asc':
        query = query.order_by(QRCode.created_at.asc())
    elif sort == 'created_desc':
        query = query.order_by(QRCode.created_at.desc())
    elif sort == 'downloads_asc':
        query = query.order_by(QRCode.downloads.asc())
    elif sort == 'downloads_desc':
        query = query.order_by(QRCode.downloads.desc())
    else:
        query = query.order_by(QRCode.created_at.desc())
    
    # Get users for dropdown
    users = User.query.order_by(User.username).all()
    
    # Paginate the results
    per_page = 10
    qr_codes = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'admin/qr_codes.html', 
        title='QR Code Management', 
        qr_codes=qr_codes,
        users=users
    )

@admin.route('/qr-codes/delete/<int:qr_id>', methods=['POST'])
@login_required
@admin_required
def delete_qr_code(qr_id):
    qr_code = QRCode.query.get_or_404(qr_id)
    
    # Delete the QR code file if it exists
    if qr_code.file_path and os.path.exists(qr_code.file_path):
        try:
            os.remove(qr_code.file_path)
        except:
            pass
    
    db.session.delete(qr_code)
    db.session.commit()
    flash('QR code has been deleted!', 'success')
    return redirect(url_for('admin.qr_codes'))

@admin.route('/export')
@login_required
@admin_required
def export():
    export_type = request.args.get('type', 'users')
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    if export_type == 'users':
        users = User.query.all()
        writer.writerow(['ID', 'Username', 'Email', 'Is Admin', 'Created At', 'Last Login'])
        
        for user in users:
            writer.writerow([
                user.id, 
                user.username, 
                user.email, 
                user.is_admin, 
                user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '', 
                user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else ''
            ])
        filename = f'users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
    elif export_type == 'qr_codes':
        qr_codes = QRCode.query.all()
        writer.writerow(['ID', 'User ID', 'Content', 'QR Type', 'Created At', 'Size', 'Color'])
        
        for qr in qr_codes:
            writer.writerow([
                qr.id, 
                qr.user_id, 
                qr.content, 
                qr.qr_type, 
                qr.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                qr.size,
                qr.color
            ])
        filename = f'qr_codes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
    elif export_type == 'feedback':
        feedback_list = Feedback.query.all()
        writer.writerow(['ID', 'Name', 'Email', 'Subject', 'Message', 'Submitted At'])
        
        for feedback in feedback_list:
            writer.writerow([
                feedback.id, 
                feedback.name, 
                feedback.email, 
                feedback.subject, 
                feedback.message, 
                feedback.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        filename = f'feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    else:
        return jsonify({'error': 'Invalid export type'}), 400
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@admin.route('/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def profile():
    from app.forms.profile import ProfileForm
    
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.theme = form.theme.data
        
        if form.new_password.data:
            current_user.password = generate_password_hash(form.new_password.data)
            
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('admin.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.theme.data = current_user.theme
    
    return render_template('admin/profile.html', title='Admin Profile', form=form)

@admin.route('/change-theme', methods=['POST'])
@login_required
@admin_required
def change_theme():
    theme = request.form.get('theme')
    redirect_url = request.form.get('redirect_url') or request.referrer or url_for('admin.profile')
    
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