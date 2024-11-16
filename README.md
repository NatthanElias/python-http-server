# Python HTTP Server
HTTP Server implemented in Python for Distributed Systems class

Parser
    - [Httptools](https://pypi.org/project/httptools/)

## Project Structure
- server/: Main application package.
    - __init__.py: Indicates that this directory is a Python package.
    - models/: Contains data models.
        - file.py: Your File class (renamed to follow Python naming conventions).
    - controllers/: Contains the logic for handling requests and authentication.
        - request_handler.py: Handles incoming HTTP requests.
        - authentication.py: Contains authentication-related functions.
    - server.py: Manages the server setup, socket creation, and listening for connections.
    - routes.py: Defines URL patterns and maps them to controller functions.
- tests/: Contains test cases for your application.
    - test_file.py: Tests for your File model.
    - test_server.py: Tests for your server and request handling.
- app.py: Entry point of your application, starts the server.
- README.md, requirements.txt, .gitignore: Standard project files.