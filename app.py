from flask import Flask
import threading
import os
from bot import run_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Nexus Selling Bot is Online!"

def start_bot():
    try:
        run_bot()
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    # Start the bot in a separate thread
    threading.Thread(target=start_bot, daemon=True).start()
    
    # Run Flask on the port provided by Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)