"""
Run script for QR Code Generator application.
This script helps start the application and initialize the database.
"""

import sys

def main():
    """Main function to run the application."""
    if len(sys.argv) < 2:
        print("Usage: python run.py [init|run|all|shell]")
        print("  init  - Initialize the database only")
        print("  run   - Run the Flask application")
        print("  all   - Initialize the database and run the application")
        print("  shell - Open a Python shell with the application context")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'init' or command == 'all':
        print("Initializing database...")
        from init_db import init_db
        init_db()
    
    if command == 'run' or command == 'all':
        print("Starting Flask application...")
        from app import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    if command == 'shell':
        print("Opening Python shell with application context...")
        from app import create_app
        app = create_app()
        with app.app_context():
            import code
            code.interact(local=locals())

if __name__ == '__main__':
    main() 