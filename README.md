# SplitShare

SplitShare is a web-based application designed for easy expense splitting among groups of people. It eliminates the need for user accounts and traditional authentication by uniquely identifying each user's browser. This allows for a frictionless experience: users can create groups, add expenses, and track balances without ever needing to sign up or log in.

## How to Run

To run this application, you need to have Docker and Docker Compose installed on your machine.

1.  Ensure you have a `.env` file in the root directory. You can copy the provided example.
2.  From the root directory of the project, run the following command to build and start the services:
    `docker-compose up --build`
3.  The frontend will be accessible at `http://localhost:5173`.
4.  The backend API will be available at `http://localhost:8000`.

The application uses hot-reloading for both the frontend and backend, so any changes you make to the code will be reflected immediately without needing to restart the containers.

The SQLite database file is stored in a named Docker volume (`db_data`) to ensure data persistence across container restarts.

### Troubleshooting

If you encounter database errors (like `no such column`) after making changes to the database models in `backend/app/models/`, you may need to reset the database. Since this project does not use a migration tool, the simplest way to do this is to remove the Docker volume that stores the database file.

1.  Stop the running containers: `docker-compose down`
2.  Remove the database volume: `docker volume rm splitshare_db_data` (The volume name is typically `<project-folder-name>_db_data`).
3.  Restart the application: `docker-compose up --build`

This will create a fresh, empty database with the latest schema.
