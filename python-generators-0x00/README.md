# ALX Python Backend - Seed Generator

## Description

This script connects to a MySQL server, creates a database `ALX_prodev`, sets up a `user_data` table, and populates it using data from a CSV file (`user_data.csv`).

## Setup

1. Make sure MySQL server is running.
2. Replace the placeholder `your_password_here` in `seed.py` with your MySQL root password.
3. Place the `user_data.csv` file in the same directory.
4. Run the script via `0-main.py`.

## Example Usage

```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'Name', 'email@example.com', 45), ...]
