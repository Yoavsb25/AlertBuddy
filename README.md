# AlertBuddy

![Python](https://img.shields.io/badge/Python-A78BFA?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-7C3AED?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-A78BFA?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-7C3AED?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-6B7280?style=for-the-badge)

> Real-time safety alert web app — send and receive location-aware alerts to your network.

---

## Overview

AlertBuddy is a Django-based web application that lets users send and receive real-time safety alerts within their personal network. Users manage friend connections, broadcast their safety status with GPS coordinates, and monitor the safety of people they care about — all from a mobile-friendly interface.

## Features

- Send and receive real-time safety alerts
- Friend request and connection management
- Location-aware alerts with map integration
- Mobile-friendly responsive UI
- User authentication and profile management

## Architecture

AlertBuddy follows Django's MVT (Model-View-Template) pattern:

```
Browser → URL Router → View → Model (SQLite) → Template → Browser
```

- **`SafetyProject/`** — Django project settings, root URL config, WSGI/ASGI
- **`safety_alert/`** — Core application: models, views, URL patterns, forms, templates
- **`media/`** — User-uploaded profile images
- **`staticfiles/`** — Collected static assets for production

## Data Models

| Model | Key Fields | Purpose |
|-------|-----------|---------|
| `SafetyAlert` | `user`, `status` (bool), `latitude`, `longitude`, `city`, `last_updated` | Tracks a user's current safety state and location |
| `FriendRequest` | `sender`, `receiver`, `is_pending`, `created_at` | Manages incoming/outgoing connection requests |
| `Friendship` | `user1`, `user2`, `created_at` (unique pair) | Represents an accepted mutual friendship |
| `Profile` | `user` (1:1), `first_name`, `last_name`, `profile_image` | Extended user info, auto-created via post_save signal |

> `Profile` is created automatically via a `post_save` signal on Django's built-in `User` model.

## URL Routes

| Method | URL | View | Description |
|--------|-----|------|-------------|
| GET | `/` | `home` | Dashboard — shows your status and friends' alerts |
| GET/POST | `/signup/` | `signup` | Create a new account |
| GET/POST | `/login/` | `user_login` | Authenticate |
| POST | `/logout/` | `LogoutView` | End session |
| GET | `/profile/` | `profile_view` | View own profile |
| GET/POST | `/profile/edit/` | `edit_profile` | Update name and profile image |
| POST | `/update-status/` | `update_safety_status` | Toggle safe/not-safe with location |
| GET | `/search/` | `search_users` | Find users by username |
| POST | `/add-friend/<user_id>/` | `add_friend` | Send friend request |
| POST | `/remove-friend/<user_id>/` | `remove_friend` | Unfriend a user |
| GET | `/pending-requests/` | `pending_friend_requests` | View incoming friend requests |
| POST | `/approve-request/<request_id>/` | `approve_friend_request` | Accept a friend request |
| POST | `/decline-request/<request_id>/` | `decline_friend_request` | Reject a friend request |

## Getting Started

**Prerequisites:** Python 3.x, pip

```bash
git clone https://github.com/Yoavsb25/AlertBuddy.git
cd AlertBuddy
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000

## Project Structure

```
alertbuddy/
├── SafetyProject/          # Django project settings and root URLs
├── safety_alert/
│   ├── models.py           # SafetyAlert, FriendRequest, Friendship, Profile
│   ├── views.py            # All view logic
│   ├── urls.py             # URL patterns
│   ├── forms.py            # Registration and profile forms
│   ├── backends.py         # Custom authentication backend
│   ├── context_processors.py
│   ├── admin.py
│   ├── tests.py
│   ├── templatetags/       # Custom template tags
│   └── migrations/
├── media/                  # Uploaded user content
├── staticfiles/            # Collected static assets
├── requirements.txt
└── vercel.json             # Deployment config
```

---

[![LinkedIn](https://img.shields.io/badge/Yoav_Sborovsky-LinkedIn-7C3AED?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yoav-sborovsky/)
&nbsp;
Part of [Yoav Sborovsky's GitHub portfolio](https://github.com/Yoavsb25)
