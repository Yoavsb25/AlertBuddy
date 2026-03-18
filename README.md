# AlertBuddy

![Python](https://img.shields.io/badge/Python-A78BFA?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-7C3AED?style=for-the-badge&logo=django&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-7C3AED?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-6B7280?style=for-the-badge)

> Real-time safety alert web app — send and receive location-aware alerts to your network.

---

## Overview

AlertBuddy is a Django-based web application that lets users send and receive real-time safety alerts to their personal network. Users can manage friend connections, trigger location-aware alerts, and stay informed about the safety of people they care about.

## Features

- Send and receive real-time safety alerts
- Friend request and connection management
- Location-aware alerts with map integration
- Mobile-friendly responsive UI
- User authentication and profiles

## Tech Stack

![Django](https://img.shields.io/badge/Django-7C3AED?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-A78BFA?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-A78BFA?style=for-the-badge&logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-6B7280?style=for-the-badge&logo=vercel&logoColor=white)

## Getting Started

**Prerequisites:**
- Python 3.x
- pip

**Installation:**
```bash
git clone https://github.com/Yoavsb25/AlertBuddy.git
cd AlertBuddy
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000

## Usage

1. Register an account and log in
2. Send friend requests to your contacts
3. Use the alert button to notify your network of your location and status
4. View incoming alerts on your dashboard

## Project Structure

```
alertbuddy/
├── SafetyProject/      # Django project settings
├── safety_alert/       # Core app — models, views, templates
├── media/              # Uploaded user content
├── staticfiles/        # Collected static assets
├── requirements.txt    # Python dependencies
└── vercel.json         # Deployment config
```

---

[![LinkedIn](https://img.shields.io/badge/Yoav_Sborovsky-LinkedIn-7C3AED?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yoav-sborovsky/)
&nbsp;
Part of [Yoav Sborovsky's GitHub portfolio](https://github.com/Yoavsb25)
