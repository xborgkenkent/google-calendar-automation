 python -m venv env
 env/Scripts/activate
 pip install fastapi uvicorn google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
 uvicorn app.main:app --reload