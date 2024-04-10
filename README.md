# flask-app-base
Minimal flask application with flask-classful and flask-restful in a docker container.

## Development Process
1. Clone the repository, delete the .git folder and initialize as a new git repository
2. Create the env file in /app/env/env.production<br>
   <i>Note: If the application is started with the RUN_MODE env var set, 
   the application will use the env file in /app/env/env.{RUN_MODE} instead of env.production</i>
3. Set up virtual environment and install dependencies
4. Run with: RUN_MODE=development flask run (or set it up in pycharm, and set up the env var in the run configuration)
5. Develop the application

## Page Endpoints
1. `/` - Home page
2. `/login` - Login page
3. `/logout` - Logout page
4. `/admin` - Sample admin page with admin_level restrictions
5. `/api/v1/docs` - Swagger API documentation. Specifically `$API_PATH/docs` where `$API_PATH` is the API_PATH env var

## Structure
1. `scripts/` folder contains scripts that can be run from the command line
   - `scripts/app_start.sh` is the entry point for the application in the docker container
   - `scripts/build.sh` is a sample build script for the docker container. Set up the APP_NAME env var in the file to set the name of the container
   - `scripts/deploy.sh` is a sample deploy script for the docker container. Set up the APP_NAME env var in the file to set the name of the container
   - `scripts/create_user.sh` is a sample script on how to create a user from the command line (helpful for first users of the system)
   - `scripts/reset_user_password.sh` is a sample script on how to reset a password from the command line (helpful for development and testing)
   - `scripts/run_tasks.sh` is a sample script on how to run tasks other than starting the flask application. See `app/app.py` in the `run_tasks()` function for more information.

2. `app/lib` folder contains all the DB models and helper classes for the application
3. `app/pages` folder contains all the views for the application
4. `app/api` folder contains all the API endpoints for the application

## Sample Environment File
```bash
export APP_SECRET_KEY=65a4d6c8ec2337f104658a21a02b3c83b89844214f8a3830e2b65f4e17916098
export JWT_SECRET=e1d3f8f5483c1ff565034cb9807f15cf9c9703c9525477bee4a14040114adf8a

export DB_USER=username_here
export DB_PASSWORD=password_here
export DB_DATABASE=dbname_here
export DB_HOST=hostname:3306

# Sets up logging for API errors
export LOGFILE=logs/error.log
# Set this to log all API requests. See restapi.py for more information
export DEBUG_LOGFILE=logs/debug.log

# Base path for the API and the API documentation
export API_PATH=/api/v1
# If this is set, the application will require authentication for the Swagger API documentation
export APIDOCS_REQUIRE_AUTH=True
# admin_level of the user to require for the Swagger API documentation
export APIDOCS_REQUIRE_AUTH_LEVEL=1
```

## Environment variables not in the environment file
1. `APP_NAME` - Name of the application, set inside the build and deploy scripts
2. `RUN_MODE` - Automatically set on app startup, is derived from the `DEPLOY_ENV` that is set before running the build and deploy scripts.
3. `RUN_TASKS` - Set to `True` to run tasks other than starting the flask application. See `app/app.py` in the `run_tasks()` function for more information.
4. `LISTEN_PORT` - Port on which the application listens for incoming requests. Set this in `deploy.sh`
