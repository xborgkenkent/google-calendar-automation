![Watch the video](https://github.com/user-attachments/assets/96d58efe-4e21-4cfa-afeb-35ca78d9a3a4)

[Demo video](https://drive.google.com/file/d/12uU9R0mx3HB5UiaVsPIspeDEUB4NtDEx/view?usp=sharing)

# Tech Stack: Python, FastAPI, Nuxt, Vue, Google Calendar API, OpenAI API

# Setup Instructions

# Enable Google Calendar API
You can find detailed instructions on how to enable the Google Calendar API and create the necessary credentials by following this link:
[Google Calendar API Guide](https://developers.google.com/workspace/calendar/api/quickstart/nodejs)

This guide will walk you through the process in the Google Cloud Console. After setting up your credentials, **paste the downloaded `credentials.json` file into the `app` folder** and proceed with the backend setup below.

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
3.  **After the installation completes, copy the example environment file:**

    ```bash
    cp example.env .env
    ```

4.  **Install the required Python packages:**

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

3.  **After the installation completes, copy the example environment file:**

    ```bash
    cp example.env .env
    ```

4.  **Run the Nuxt.js development server:**

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
