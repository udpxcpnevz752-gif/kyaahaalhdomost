from flask import Flask
import threading
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NexusApp")

load_dotenv()

from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Nexus Selling Bot is Online! 🚀"

@app.route('/health')
def health():
    return {"status": "ok"}, 200

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask keep-alive server on port {port}...")
    # use_reloader=False is CRITICAL when running in a thread
    app.run(host="0.0.0.0", port=port, use_reloader=False)

if __name__ == "__main__":
    # 1. Start Flask in a background daemon thread
    # This satisfies Render's port binding requirement
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 2. Run the Bot on the MAIN thread
    # This is required for asyncio and signal handling in python-telegram-bot v20+
    try:
        run_bot()
    except Exception as e:
        logger.error(f"Critical Bot Error: {e}")
