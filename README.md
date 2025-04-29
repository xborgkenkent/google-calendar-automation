# Setup Instructions

These instructions will guide you through setting up the development environment for this project, which includes a Python/FastAPI backend and a Nuxt.js frontend.

## Backend Setup (FastAPI)

1.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv env
    ```

2.  **Activate the virtual environment:**

    * **On Windows:**

        ```bash
        .\env\Scripts\activate
        ```

    * **On macOS and Linux:**

        ```bash
        source env/bin/activate
        ```

3.  **Install the required Python packages:**

    ```bash
    pip install fastapi uvicorn google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

4.  **Run the FastAPI application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    * `app.main:app`:  Specifies the module (`app.main`) and the application object (`app`) within that module.
    * `--reload`: Enables automatic reloading of the server when you make code changes, which is very useful during development.

## Frontend Setup (Nuxt.js)

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install the Node.js dependencies:**

    ```bash
    npm install
    ```

    or

    ```bash
    yarn install
    ```

    or

    ```bash
    pnpm install
    ```

3.  **Run the Nuxt.js development server:**

    ```bash
    npm run dev
    ```

    or

    ```bash
    yarn dev
    ```

    or

    ```bash
    pnpm dev
    ```
