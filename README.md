# QR Code Generator Web Application

A professional QR code generation web application with user and admin dashboards, built with Flask and modern frontend technologies.

## Features

### Authentication
- User and Admin login systems
- Sign-up functionality
- Forgot password feature
- Secure password management

### QR Code Generation
- Custom QR code generation 
- Logo insertion capabilities
- Size selection options
- Color customization
- Download and sharing options

### User Dashboard
- QR code generation history
- Export to CSV functionality
- Theme customization
- User profile management

### Admin Dashboard
- User management (create, edit, delete users)
- User activity monitoring
- Feedback management
- QR code usage statistics
- Export functionality
- Theme customization

### Additional Features
- Responsive design for all devices
- About Us page
- Contact Us page with feedback form
- FAQ section
- Professional UI with modern design elements

## Tech Stack

- Backend: Python Flask
- Database: SQLAlchemy
- Frontend: HTML, CSS, JavaScript
- CSS Frameworks: Bootstrap, Tailwind CSS
- State Management: Flask session management
- QR Code Generation: qrcode & Pillow libraries

## Installation

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Setup the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. Run the application:
   ```
   flask run
   ```

## License

All rights reserved.

## Author

[Your Name] 