import os
import sys
import webbrowser
import subprocess

def main():
    print("=" * 65)
    print("  Multimodal Attendance & Engagement Agent - Launcher")
    print("=" * 65)
    print("Choose execution mode:")
    print("  [1] Launch Core Web Application (FastAPI + Modern Web Dashboard)")
    print("  [2] Launch Streamlit Interactive Dashboard (Milestone 6 Activity 6.2)")
    print("  [3] Exit")
    print("-" * 65)

    choice = input("Enter choice [1/2/3] (default 1): ").strip() or "1"

    if choice == "1":
        print("\nStarting FastAPI Core Server on http://localhost:8000 ...")
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        sys.path.insert(0, backend_dir)
        try:
            import uvicorn
            webbrowser.open("http://localhost:8000")
            uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
        except ImportError:
            print("\nError: 'uvicorn' or 'fastapi' not installed yet.")
            print("Please run:  pip install -r backend/requirements.txt")
    elif choice == "2":
        print("\nStarting Streamlit Dashboard on http://localhost:8501 ...")
        subprocess.run(["streamlit", "run", "streamlit_app.py"])
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
