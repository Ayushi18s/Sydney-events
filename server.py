from flask import Flask, jsonify, request, send_from_directory
from scraper import EventScraper, EmailSubscription
import threading
import os

app = Flask(__name__)
scraper = EventScraper()
email_manager = EmailSubscription()

# Enable CORS (Cross-Origin Resource Sharing)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Run initial scraping
def start_scraping():
    threading.Thread(target=scraper.scrape_all_sources).start()

# Serve events
@app.route('/events')
def get_events():
    events = scraper.get_events()
    if not events:
        # If no events have been scraped yet, do it now
        events = scraper.scrape_all_sources()
    return jsonify(events)

# Handle email subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email') if data else None
    
    if email:
        success = email_manager.add_subscriber(email)
        return jsonify({"success": success})
    return jsonify({"success": False, "error": "No email provided"})

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    print("Starting Sydney Events Server...")
    print("Visit http://localhost:5000 in your browser to view the site")
    # Run initial scraping before starting the server
    start_scraping()
    app.run(debug=True)