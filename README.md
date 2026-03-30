# LLM Support Dashboard

A full-stack project for creating support tickets, storing them in a database, and showing simple analytics in a dashboard.

## Overview

This project uses a FastAPI backend, PostgreSQL database, and React frontend. Users can create tickets, view saved tickets, and see basic ticket metrics in the dashboard.

## Project Preview


![Dashboard Preview](assets/dashboard.png)

## Features

- Create support tickets
- Store tickets in PostgreSQL
- View all tickets in a dashboard
- Show ticket counts by category
- Display short ticket summaries
- Visualize ticket data with a chart

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- React
- Vite
- Chart.js
- Docker

## How It Works

The frontend sends requests to the FastAPI backend.  
The backend stores ticket data in PostgreSQL.  
The dashboard reads ticket data from the backend and shows it in a table and chart.  
The project also includes a simple ML file structure for ticket classification and summarization.

## Architecture


![Architecture](assets/Apic.png)

A simple flow is:

`React frontend -> FastAPI backend -> PostgreSQL database`

## Project Structure

```text
llm-support-dashboard/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── ml.py
│   ├── seed_tickets.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md