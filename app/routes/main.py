from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.feedback import Feedback
from app.forms.contact import ContactForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html', title='Home')

@main.route('/about')
def about():
    return render_template('main/about.html', title='About Us')

@main.route('/faq')
def faq():
    return render_template('main/faq.html', title='Frequently Asked Questions')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            submitted_at=datetime.utcnow()
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback has been submitted. Thank you!', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('main/contact.html', title='Contact Us', form=form) 