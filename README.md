# Python HTTP Server

This project is a simple HTTP Server implemented in Python for Distributed Systems class. With was built from scratch using Python. It handles HTTP GET and POST requests, includes basic user authentication, and manage files storage. The server is capable of handling multiple clients simultaneously through multithreading.

## Project Structure

- **app.py**: Entry point of the application.
- **server/**: Contains all server-related code.
  - **models/**: Defines data structures and storage.
    - **file.py**: Contains the `File` class representing file objects.
    - **storage.py**: Simulates in-memory file storage.
  - **utils/**: Utility functions and classes.
    - **authentication.py**: Handles user authentication and session key validation.
    - **exceptions.py**: Custom exception classes for error handling.
    - **validations.py**: Functions for input validation.
    - **response_helpers.py**: Helpers to generate HTTP responses.
    - **parse_headers.py**: Functions to parse HTTP request headers.
  - **handlers/**: Request handlers for different routes.
    - **handle_get_request.py**: Handles GET requests for individual files.
    - **handle_post_request.py**: Routes POST requests to appropriate handlers.
    - **handle_login.py**: Processes user login and returns session keys.
    - **handle_file_upload.py**: Handles file upload requests.
    - **handle_get_all_files.py**: Returns a list of all stored files.
    - **handle_not_found.py**: Handles undefined routes (404 errors).
    - **handle_server_error.py**: Handles server errors (500 errors).
  - **server.py**: Sets up the server socket, listens for connections, and delegates requests.
  - **routes.py**: Defines URL patterns and maps them to handler functions.
- **postman_collection/**: Contains the Postman collection for testing the API endpoints.
  - **HTTP_Server_Postman_Collection.json**: Postman collection file with predefined requests.

## Technologies

- **Python 3.x**: Programming language used for the server. Libs:
    - ``socket``: For handling network communications.
    - `thread`: To manage multiple client connections concurrently.
    - **[Httptools](https://pypi.org/project/httptools/)**: HTTP parser used for parsing HTTP requests.

## How to Test

You can test the server using tools like **Postman** or **Insomnia**. A Postman collection is provided in the `postman_collection/` folder to facilitate testing.

### Importing the Postman Collection

1. Open Postman.
2. Click on **Import**.
3. Choose **Import File**.
4. Navigate to the `postman_collection/` folder and select `HTTP_Server_Postman_Collection.json`.
5. Click **Open** to import the collection.

### Available Endpoints

#### **1. GET `/arquivos`**

Retrieves a list of all stored file names.

##### Parameters

None.

##### Status Codes

| Status Code                   | Description                                  |
|-------------------------------|----------------------------------------------|
| **200 OK**                    | Successfully retrieved the list of files.    |
| **500 Internal Server Error** | Server encountered an unexpected condition.  |

##### Response Examples

- **Success (200 OK)**

  **JSON:**

  {
    "arquivos": ["file1.txt", "file2.txt"]
  }

- **No Files Available**

  **JSON:**

  {
    "mensagem": "Nenhum arquivo armazenado."
  }

#### **2. GET `/arquivos/{filename}`**

Retrieves the content of the specified file.

##### Parameters

| Name       | Type   | In   | Description                                 |
|------------|--------|------|---------------------------------------------|
| `filename` | string | path | Specifies the name of the file to retrieve. |

##### Status Codes

| Status Code                   | Description                                     |
|-------------------------------|-------------------------------------------------|
| **200 OK**                    | Successfully retrieved the file content.        |
| **404 Not Found**             | The specified file does not exist.              |
| **500 Internal Server Error** | Server encountered an unexpected condition.     |

##### Response Examples

- **Success (200 OK)**

  The response body will contain the content of the file.

  This is the content of the file.

- **File Not Found (404 Not Found)**

  **JSON:**

  {
    "error": "Arquivo não encontrado"
  }

#### **3. POST `/login`**

Authenticates the user and returns a session key for authorization.

##### Request Headers

| Name           | Type   | In     | Description                 |
|----------------|--------|--------|-----------------------------|
| `Content-Type` | string | header | Must be `application/json`. |

##### Request Body

**JSON:**

{
  "username": "admin",
  "password": "senha123"
}

##### Status Codes

| Status Code                   | Description                                         |
|-------------------------------|-----------------------------------------------------|
| **200 OK**                    | Authentication successful; returns session key.     |
| **403 Forbidden**             | Authentication failed; invalid credentials.         |
| **500 Internal Server Error** | Server encountered an unexpected condition.         |

##### Response Examples

- **Success (200 OK)**

  **JSON:**

  {
    "key": "sessionkey123"
  }

- **Invalid Credentials (403 Forbidden)**

  **JSON:**

  {
    "error": "Credenciais inválidas"
  }

#### **4. POST `/arquivos`**

Uploads a new file to the server. Requires authorization.

##### Request Headers

| Name            | Type   | In     | Description                                      |
|-----------------|--------|--------|--------------------------------------------------|
| `Content-Type`  | string | header | Must be `application/json`.                      |
| `Authorization` | string | header | Session key obtained from the `/login` endpoint. |

##### Request Body

**JSON:**

{
  "nome": "newfile.txt",
  "conteudo": "This is the content of the new file.",
  "tipo": "text/plain"
}

##### Status Codes

| Status Code                     | Description                                                |
|---------------------------------|------------------------------------------------------------|
| **201 Created**                 | File successfully created or updated.                      |
| **400 Bad Request**             | Required fields are missing or invalid.                    |
| **401 Unauthorized**            | Missing or invalid session key.                            |
| **415 Unsupported Media Type**  | The specified file type is not supported.                  |
| **500 Internal Server Error**   | Server encountered an unexpected condition.                |

##### Response Examples

- **Success (201 Created)**

  **JSON:**

  {
    "message": "Arquivo criado/atualizado com sucesso"
  }

- **Missing Fields (400 Bad Request)**

  **JSON:**

  {
    "error": "Campos obrigatórios faltando no corpo da requisição"
  }

- **Unauthorized (401 Unauthorized)**

  **JSON:**

  {
    "error": "Não autorizado"
  }

- **Unsupported Media Type (415 Unsupported Media Type)**

  **JSON:**

  {
    "error": "Tipo MIME 'application/xml' não suportado"
  }

#### **Supported MIME Types**

- `text/plain`
- `text/html`

### Testing Steps

1. **Login to Obtain Session Key**

   - Use the **POST** `/login` request from the Postman collection.
   - Send the request with the required credentials.
   - Copy the `key` from the response for use in subsequent requests.

2. **Upload a File**

   - Use the **POST** `/arquivos` request.
   - Add the `Authorization` header with the session key obtained earlier.
   - Include the file data in the request body.

3. **List All Files**

   - Use the **GET** `/arquivos` request to retrieve the list of stored files.

4. **Retrieve a Specific File**

   - Use the **GET** `/arquivos/{filename}` request to retrieve the content of a specific file.
   - Replace `{filename}` with the actual file name you uploaded.

5. **Error Handling**

   - Test the server's responses to invalid inputs, missing headers, or unauthorized access by modifying the requests accordingly.

## Developers

- **Natthan Elias** - [GitHub Profile](https://github.com/NatthanElias)
- **Artur Mariano** - [GitHub Profile](https://github.com/ArturMariano13)
