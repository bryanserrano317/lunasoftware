# Web Application Documentation

## Overview
This project consists of an Express.js-based backend and EJS-based frontend templates for rendering dynamic web pages. It includes login, registration, home, and place details functionality.

---

## Frontend (`.ejs` Files)

### `home.ejs`
- Displays navigation links.
- Provides links to Google Maps Reviews and marketing materials【46†source】.

### `index.ejs`
- Uses the Google Places API to fetch and display place details.
- Displays the total ratings, rating count, and a percentage growth calculation for ratings.
- Shows the last updated timestamp【47†source】.

### `login.ejs`
- Renders a simple login form with fields for username and password.
- Sends a POST request to `/internal/login`【48†source】.

### `register.ejs`
- Contains a registration form with fields for username and password.
- Sends a POST request to `/internal/register`.
- Provides a link to the login page【49†source】.

---

## Backend (`.js` Files)

### `server.js`
- Sets up the Express.js server.
- Defines API routes for handling authentication and user management.
- Uses middleware for handling sessions and user authentication.

### `user.js`
- Defines the user model and related database operations.
- Handles user registration and authentication logic.

---

## Usage
1. Install dependencies using `npm install`.
2. Configure `.env` file for database and API keys.
3. Run the server using `node server.js`.
4. Access the web pages via the configured local server URL.

---

## License
This project is licensed under MIT License.
