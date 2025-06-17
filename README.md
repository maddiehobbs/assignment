# Tickets R Us

A web-based ticket management system for teams to track and manage support tickets efficiently

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Existing Credentials](#existing-credentials)
- [Admin/Regular Roles](#adminregular-roles)
- [Features](#features)
- [Validation](#validation)
- [Database](#database)
- [Installation](#installation)

## Overview

Tickets R Us enables teams to have a central system for tracking support tickets. Users can create, view, and update tickets, while adminsitrators have an additional action of being able to delete tickets.

## Getting Started

- Visit [link] to access the application
- Register a new user or log into an existing account, already created credentials are found in [# Existing credentials](#existing-credentials)
- Use the application to manage tickets, including creating, deleting (admin only), and updating records.

## Existing credentials

**Regular User:**

- Username: `username1` through `username9`
- Password: `password1` through `password9`

**Administrator:**

- Username: `adminuser`
- Password: `adminpassword1?`

_Note: Pre-existing usernames cannot be re-registered_

### Admin/Regular Roles

**Regular users can:**

- Create new tickets
- View existing tickets
- Update ticket information

**Admin users can:**
All regular user permission, plus:

- Delete any tickets

## Features

- **Registration and Login:** Users can register an account or log in with existing credentials to access the application.
- **View Tickets:** Users can view a list of tickets.
- **Create Tickets:** Users can create new tickets to add to the database.
- **Delete Tickets (admin only):** Admin users can delete tickets.
- **Update Tickets:** Users can update information on existing tickets.

## Validation

- Validation is implemented for user registration to ensure usernames and passwords meet specified criteria.
  - Username:
    - Minimum length of 6 characters
    - Username cannot already exist
  - Password:
    - Minimum length of 8 characters
    - Must contain at least 1 numbers
- Input data is also validated to ensure data integrity.
  - Input:
    - Date cannot be in the future
    - Ticket ID and severity must be numerical
    - Ticket severity must be between 1-5, in increments on 0.5
    - Ticket status and assigned must be one of the pre-defined values
- Validation error and success messages are implemented to inform the user of their correct or incorrec tinputs
- Confirmation messages are implemented when deleting tickets to ask the user to confirm their actions before the database is updated.

### Database

- The application uses SQLite, the database schema includes a `tickets` tabl for storing ticket related information and a `users` table for storing user credentials.
- SQLite uses a local file (`database.db`) for data storage.

## Installation

1. Clone this repository to your local machine.
2. Create and activate a virtual environment or the project
3. You will need the following dependencies, you can get these through running `pip install -r requirements.txt`
4. Run the application through running `python main.py` from the root directory.
