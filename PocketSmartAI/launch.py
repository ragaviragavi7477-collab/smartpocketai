import subprocess
import sys
import os
import webbrowser

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("=" * 50)
print("  PocketSmart AI is starting...")
print("=" * 50)
print()
print("Opening browser to http://localhost:8000")
print("Press Ctrl+C to stop the server")
print()

# Open browser
webbrowser.open("http://localhost:8000")

# Start server
subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])
