import requests
from bs4 import BeautifulSoup
import json
import schedule
import time
import threading

class EventScraper:
    def __init__(self):
        self.events = []
        
    def scrape_eventbrite(self):
        """Scrape events from Eventbrite Sydney"""
        url = "https://www.eventbrite.com.au/d/australia--sydney/all-events/"
        try:
            # For demonstration, creating sample events instead of actual scraping
            # In a real application, you would implement actual scraping logic
            sample_events = [
                {
                    'name': 'Sydney Music Festival',
                    'date': 'June 15, 2025',
                    'venue': 'Sydney Opera House',
                    'description': 'Annual music festival featuring local artists',
                    'ticket_link': 'https://www.eventbrite.com.au/sample-event-1'
                },
                {
                    'name': 'Food & Wine Expo',
                    'date': 'May 30, 2025',
                    'venue': 'Darling Harbour',
                    'description': 'Taste the best food and wine Sydney has to offer',
                    'ticket_link': 'https://www.eventbrite.com.au/sample-event-2'
                }
            ]
            self.events.extend(sample_events)
            print("Added sample Eventbrite events")
        except Exception as e:
            print(f"Error scraping Eventbrite: {e}")
    
    def scrape_ticketmaster(self):
        """Scrape events from Ticketmaster Sydney"""
        try:
            # For demonstration, creating sample events instead of actual scraping
            sample_events = [
                {
                    'name': 'International Comedy Festival',
                    'date': 'June 5-12, 2025',
                    'venue': 'State Theatre',
                    'description': 'Featuring top comedians from around the world',
                    'ticket_link': 'https://www.ticketmaster.com.au/sample-event-1'
                },
                {
                    'name': 'Sydney Symphony Orchestra',
                    'date': 'May 25, 2025',
                    'venue': 'Sydney Opera House',
                    'description': 'Classical music performance',
                    'ticket_link': 'https://www.ticketmaster.com.au/sample-event-2'
                }
            ]
            self.events.extend(sample_events)
            print("Added sample Ticketmaster events")
        except Exception as e:
            print(f"Error scraping Ticketmaster: {e}")
    
    def scrape_all_sources(self):
        """Scrape events from multiple sources"""
        # Clear previous events
        self.events = []
        # Call individual scraping methods
        self.scrape_eventbrite()
        self.scrape_ticketmaster()
        
        # Save to file
        self.save_events()
        return self.events
        
    def save_events(self):
        """Save scraped events to a JSON file"""
        with open('sydney_events.json', 'w') as f:
            json.dump(self.events, f, indent=2)
        print(f"Saved {len(self.events)} events to file")
            
    def get_events(self):
        """Return current events"""
        return self.events

class EmailSubscription:
    def __init__(self):
        self.subscribers = []
        try:
            with open('subscribers.json', 'r') as f:
                self.subscribers = json.load(f)
        except FileNotFoundError:
            pass
    
    def add_subscriber(self, email):
        """Add email to subscribers list"""
        if email not in self.subscribers:
            self.subscribers.append(email)
            self.save_subscribers()
            print(f"Added subscriber: {email}")
            return True
        return False
    
    def save_subscribers(self):
        """Save subscribers to a file"""
        with open('subscribers.json', 'w') as f:
            json.dump(self.subscribers, f)

def periodic_scraping(scraper):
    """Run scraping periodically"""
    schedule.every(4).hours.do(scraper.scrape_all_sources)
    while True:
        schedule.run_pending()
        time.sleep(1)