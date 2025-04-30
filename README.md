![image](https://github.com/user-attachments/assets/762c5d25-5e97-4394-82f2-050df6e96244)
![image](https://github.com/user-attachments/assets/6db557e5-a611-4440-8ca8-167b7cd9cb77)


# Setup Instructions

# Enable Google Calendar API
You can find detailed instructions on how to enable the Google Calendar API and create the necessary credentials by following this link:
[Google Calendar API Guide]([https://www.google.com/search?q=https://developers.google.com/calendar/api/quickstart/python%23step_1_turn_on_the](https://developers.google.com/workspace/calendar/api/quickstart/nodejs))

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
