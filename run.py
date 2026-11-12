import sys
import os

# Set UTF-8 output encoding for Windows stdout if possible
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Auto check and install missing dependencies
try:
    import flask
    import werkzeug
except ImportError:
    import subprocess
    print("Missing Flask/Werkzeug libraries. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask", "Werkzeug"])
        print("Successfully installed required packages!")
    except Exception as e:
        print(f"Could not auto-install packages: {e}")
        print("Please run manually: pip install -r requirements.txt")

# Add app directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from app import create_app
from seed import seed_database
from database import DB_PATH

if __name__ == '__main__':
    # Auto seed if database is missing or empty
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        print("Database missing or empty. Initializing and seeding demo data...")
        seed_database()

    app = create_app()
    print("==================================================")
    print("University LMS Server is running on: http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
