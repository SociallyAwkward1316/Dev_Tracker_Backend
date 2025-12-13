# DevTrack Backend
  
**Live Application:** [https://devtracker.dev](https://devtracker.dev)

Backend API for **DevTrack**, A full-stack project management application built with **Django REST Framework** and **React**, focused on backend architecture, authentication, and real-world data relationships.

This project allows users to create projects, organize them into categories, and manage tasks with authentication-protected access.

---

## Features
- ChatBase Chatbot in the project tab 
- JWT authentication using HTTP-only cookies  
- Secure login, logout, and token refresh flow  
- Shift and production tracking logic  
- Pallet return and downtime calculations  
- Custom production percentage calculations  
- CORS and CSRF configured for secure cross-origin access  
- Deployed and running in production  

---

##Tech Stack [(For Backend click to go to repository)](https://github.com/SociallyAwkward1316/DevTracker_FrontEnd/edit/main/README.md)

- Python  
- Django  
- Django REST Framework  
- SimpleJWT  
- PostgreSQL (production)  
- SQLite (development)  
- Gunicorn  
- Render

---

## Authentication

Authentication is handled using **JWT tokens stored in HTTP-only cookies**, improving security by preventing client-side JavaScript access.

- Access tokens are short-lived  
- Refresh tokens are rotated securely  
- Token refresh handled automatically by the backend  

---

## Architecture Notes

- Custom JWT authentication class for cookie-based auth  
- Clear separation of concerns between authentication and business logic  
- RESTful API design  
- Production-ready settings with CORS, CSRF, and HTTPS enforcement  

---

## Purpose

DevTrack was built to demonstrate backend engineering skills, including authentication, security, data modeling, and real-world deployment of a Django REST API.

Built by me(Alexis Fuenmayor) a backend-focused developer with hands-on experience deploying and maintaining real production Django applications.
