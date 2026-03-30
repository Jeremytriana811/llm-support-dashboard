"""
seed_tickets.py — Populate the database with sample tickets.

Run this AFTER the backend is running:
  python seed_tickets.py

It calls your API to create tickets, which triggers the AI classification
and summarization just like a real user would.
"""

import requests
import time

API_URL = "http://localhost:8000"

SAMPLE_TICKETS = [
    {
        "title": "Login page crashes on mobile",
        "description": "When I try to log in on my iPhone using Safari, the page crashes and shows a white screen. I've tried clearing my cache but the issue persists. This is a critical bug blocking our mobile users."
    },
    {
        "title": "Add dark mode support",
        "description": "It would be really nice if the application supported a dark mode theme. Many users work late at night and the bright white interface is hard on the eyes. Could we add a toggle in the settings page?"
    },
    {
        "title": "How do I reset my password?",
        "description": "I forgot my password and I can't find the reset option anywhere. I looked in settings and the login page but there's no 'forgot password' link. How can I reset it? Please help me understand the process."
    },
    {
        "title": "API documentation is outdated",
        "description": "The API docs on the developer portal still reference v1 endpoints but we migrated to v2 three months ago. The examples in the README don't work anymore. We need to update the documentation and add new code examples."
    },
    {
        "title": "Database connection timeout errors",
        "description": "Getting intermittent 'connection timeout' errors when the app tries to connect to the database during peak hours. The error logs show PostgreSQL connection pool exhaustion. This bug is causing 500 errors for about 5% of requests."
    },
    {
        "title": "Request: Export data to CSV",
        "description": "We need the ability to export our ticket data to CSV format for reporting purposes. This feature would allow managers to download monthly reports and analyze trends in Excel. It should include filters by date range and category."
    },
    {
        "title": "Where can I find the user guide?",
        "description": "I'm a new team member and I can't find any documentation about how to use the dashboard. Is there a user guide or tutorial that explains the main features? I'm confused about how the ticket categories work."
    },
    {
        "title": "Search functionality is broken",
        "description": "The search bar on the tickets page returns no results even when searching for tickets that definitely exist. I tried searching by title and by ID. This is a critical bug since we have hundreds of tickets and can't find anything."
    },
]


def main():
    print(f"🚀 Seeding tickets to {API_URL}...\n")

    for i, ticket in enumerate(SAMPLE_TICKETS, 1):
        try:
            res = requests.post(f"{API_URL}/tickets", json=ticket)
            res.raise_for_status()
            data = res.json()
            print(f"  ✅ [{i}/{len(SAMPLE_TICKETS)}] '{data['title']}'")
            print(f"     Category: {data['category']}  |  Summary: {data['summary'][:60]}...")
            print()
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Could not connect to {API_URL}. Is the backend running?")
            return
        except Exception as e:
            print(f"  ❌ Error creating ticket: {e}")

        time.sleep(0.5)  # Small delay to be gentle on the API

    print(f"\n🎉 Done! Created {len(SAMPLE_TICKETS)} tickets.")
    print(f"   View them at: {API_URL}/tickets")
    print(f"   View metrics at: {API_URL}/metrics/tickets")


if __name__ == "__main__":
    main()
