from flask import Flask
import logging
import threading
import time
from config import Config
from utils import session_manager
from routes import api_bp, frontend_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.register_blueprint(frontend_bp)
    
    return app

def cleanup_task():
    while True:
        time.sleep(3600)
        session_manager.cleanup_old_sessions(Config.SESSION_TIMEOUT_HOURS)
        logger.info("Session cleanup completed")

if __name__ == '__main__':
    app = create_app()
    
    cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
    cleanup_thread.start()
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
    app.run(debug=Config.DEBUG, port=Config.PORT, host=Config.HOST)