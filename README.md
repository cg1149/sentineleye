# SentinelEye - AI-Powered Screen Security Monitor

## What is it?
SentinelEye watches your screen using Claude AI and alerts you when it detects threats like exposed passwords, API keys, phishing websites, or sensitive data.

## How it works
1. Takes a screenshot every 10 seconds (only when screen changes)
2. Sends it to Claude Vision API for analysis
3. Saves results to a SQLite database
4. Fires a desktop alert if threat is HIGH or MEDIUM
5. Shows everything in a Streamlit dashboard

## Tech Stack
- Python 3.11
- Anthropic Claude Vision API
- pyautogui, SQLite, plyer, Streamlit

## Run the app
python3 main.py

## Run the dashboard
streamlit run dashboard.py

## Built by
Chakrith Gadupudi - ITI Student, Rutgers University
