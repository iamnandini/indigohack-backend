# IndigoHack Backend

## Overview

This repository contains the backend for the Flight Status and Notifications system, developed as part of the Hack to Hire 2024 event. The backend is built using Flask and integrates with RabbitMQ and Twilio to provide real-time flight status updates and notifications to passengers.

## Features

- **Real-time Updates**: Checks for changes in live flight data compared to scheduled data.
- **Push Notifications**: Sends notifications for flight status changes via SMS using Twilio.
- **Integration with Airport Systems**: Pulls data from mock airport databases for accurate information.

## Tech Stack

- **Python**
  - Flask
  - APScheduler
  - pika
  - pymongo
  - python-dotenv
- **MongoDB**
- **RabbitMQ**
- **Twilio**

## Installation and Setup

### Prerequisites

- MongoDB
- RabbitMQ
- Python 3.x

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/indigohack-backend.git
    cd indigohack-backend
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Flask app**:
    ```bash
    python app.py
    ```

## MongoDB Collections


- **Passengers Collection:**
_id: Unique identifier, id: Passenger ID, name: Passenger name, mobile: Mobile number, email: Email address, flight_id: Subscribed flight ID, date_of_flight: Date of flight, time_of_flight: Time of flight, gate: Gate number


- **Flight Live Collection:**
_id: Unique identifier, flight_id: Flight ID, time: Scheduled time, date: Scheduled date, gate: Gate number, remark: Current status (e.g., Delayed, On Time, Cancelled) 

- **Scheduled Flights Collection:**
_id: Unique identifier, flight_id: Flight ID, time: Scheduled time, date: Scheduled date, gate: Gate number, remark: Scheduled status

## Environment Variables

Ensure you have a `.env` file in the root directory with the following variables:

MONGO_URI=mongodb://localhost:27017/
RABBITMQ_HOST=localhost
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

## Link to Backend File 
[indigohack-frontend](https://github.com/iamnandini/indigohack-frontend)
