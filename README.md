
# Video Game Store API

[Español](README.es.md)

This project is a video game store API that responds to HTTP requests. It includes user registration, login, and token-based authentication. It also handles errors in JSON format using appropriate HTTP status codes. In addition, it includes tests written with pytest.

For example, the API returns:

- **401** if you do not send a token, if the token is invalid or has expired, or if the email or password is incorrect.
- **404** if you look for a product that does not exist.
- **409** if the email or product name is already in use.
- **422** if you send invalid data, such as a price of 0 or an ID that is not a number.
- **500** if something goes wrong on the server. The response includes an `id_error`, which is also recorded in the log to help identify what went wrong.

## Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **pytest**
- **bcrypt**
- **PyJWT**
- **Uvicorn**

## Endpoints

| Method | Route | Description | Requires a token |
|--------|-------|-------------|------------------|
| POST | `/usuarios` | Register a new user | No |
| POST | `/login` | Log in and return a token | No |
| GET | `/perfil` | Display your account information | Yes |
| GET | `/productos` | List all products | No |
| GET | `/productos/{id}` | Retrieve a product by its ID | No |
| POST | `/productos` | Add a new product | Yes |
| PUT | `/productos/{id}` | Replace all the data of a product | Yes |
| PATCH | `/productos/{id}` | Update only the provided product data | Yes |
| DELETE | `/productos/{id}` | Delete a product | Yes |

For endpoints that require a token, first log in and include the returned `access_token` in the `Authorization: Bearer <token>` header. The token expires after 30 minutes.

Prices are stored in cents: `9000` represents $90.00.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL installed and running on your computer

## Installation

1. Clone this repository and enter the directory:

   ```bash
   git clone https://github.com/iamagustn/tienda-videojuegos-api
   cd tienda-videojuegos-api
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate it:

   Windows:

   ```bat
   venv\Scripts\activate
   ```

   Linux or macOS:

   ```bash
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables: copy the `.env.example` file, name the copy `.env`, and fill it in with your information.

   - `DB_USER` and `DB_PASSWORD`: your PostgreSQL username and password.
   - `DB_PORT`: the port on which PostgreSQL is running. If you do not specify it, the default port is 5432.
   - `LLAVE`: a long, random string used to sign tokens. You can generate one by running `python -c "import secrets; print(secrets.token_hex(32))"`.
   - `CORREO` and `CONTRASENA`: these variables are optional. The application works without them.

   If `DB_USER`, `DB_PASSWORD`, or `LLAVE` are missing, the application will not start and will inform you which variables are missing.

5. In PostgreSQL, create two databases: `tienda` for the API and `tienda_test` for the tests. You can do this using pgAdmin or psql:

   ```sql
   CREATE DATABASE tienda;
   CREATE DATABASE tienda_test;
   ```

6. Create the tables in the `tienda` database:

   ```bash
   python -m tienda.modelos_mapeados
   ```

## How to run it

From the project directory, with the virtual environment activated, run:

```bash
uvicorn tienda.main:app --reload
```

The API will be running at http://127.0.0.1:8000.

If you go to http://127.0.0.1:8000/docs, you can view all the endpoints and test those that do not require a token directly from your browser.

For endpoints that require a token, use Postman, Thunder Client, or a similar tool, since the documentation page in this project does not send the `Authorization` header.

## How to run the tests

With the virtual environment activated and PostgreSQL running, run the following command from the project directory:

```bash
pytest -v
```

The tests verify, for example, that users cannot access their profiles without a token, that requests for nonexistent products return a 404 status code, and that invalid IDs return a 422 status code.

The tests use the `tienda_test` database. They create the tables before each test and drop them afterward, so the data in the `tienda` database remains unaffected.
