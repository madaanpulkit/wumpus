from app.app import app, socketio
import sys

if __name__ == "__main__":
    socketio.run(app, port=sys.argv[1] if len(sys.argv) > 1 else None, debug=True)
