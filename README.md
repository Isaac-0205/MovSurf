# MovSurf - Movie Booking System

A comprehensive Django-based movie booking and management system that allows users to browse movies, book tickets, manage watchlists, and write reviews.

## Features

### For Users
- **Movie Browsing**: Browse through a collection of movies with detailed information
- **Advanced Search**: Search movies by title, director, genre, rating, year, and duration
- **Movie Booking**: Book movie tickets with seat selection
- **Watchlist Management**: Add/remove movies to/from personal watchlist
- **Reviews & Ratings**: Write and manage movie reviews with ratings
- **User Profiles**: Manage personal profile with profile pictures
- **Booking History**: View past and current bookings
- **Responsive Design**: Mobile-friendly interface

### For Staff/Admins
- **Movie Management**: Add, edit, and delete movies
- **Theater Management**: Manage theaters, screens, and seats
- **Showtime Management**: Create and manage movie showtimes
- **User Management**: Manage user accounts and permissions

## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local file system for media files
- **API**: Django REST Framework for API endpoints

## Project Structure

```
movsurf/
├── movies/                 # Main app for movie-related functionality
│   ├── models.py          # Database models
│   ├── views.py           # View functions and API viewsets
│   ├── forms.py           # Django forms
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL routing
│   └── templates/         # HTML templates
├── profiles/              # User profile management
├── movsurf/               # Project settings
├── media/                 # User uploaded files
├── static/                # Static files
└── templates/             # Base templates
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/movsurf.git
cd movsurf
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Database Models

### Core Models
- **Movie**: Stores movie information (title, description, director, etc.)
- **Genre**: Movie genres/categories
- **Theater**: Movie theaters
- **Screen**: Theater screens
- **Seat**: Individual seats with pricing
- **Showtime**: Movie screening times
- **Booking**: User ticket bookings
- **Ticket**: Individual tickets
- **Review**: User movie reviews
- **Watchlist**: User's saved movies
- **Profile**: Extended user profile information

## API Endpoints

The application provides REST API endpoints for:
- Movies: CRUD operations and search
- Genres: List and retrieve
- Reviews: Create, read, update, delete
- Watchlist: Manage user watchlist
- Theaters, Screens, Seats: Management operations
- Showtimes: Movie screening times
- Bookings: User booking management
- Tickets: Ticket information

## Usage

### For Regular Users
1. Register/Login to your account
2. Browse movies on the home page
3. Use search and filter options to find movies
4. Click on a movie to view details
5. Add movies to your watchlist
6. Write reviews and rate movies
7. Book tickets for upcoming shows
8. Manage your profile and booking history

### For Staff/Admins
1. Login with staff credentials
2. Access admin panel at `/admin/`
3. Manage movies, theaters, and showtimes
4. Monitor bookings and user activity
5. Handle user management tasks

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the development team.

## Acknowledgments

- Django community for the excellent framework
- Bootstrap for the responsive UI components
- All contributors and users of this project
