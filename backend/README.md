# ...existing code...

## Running the Application

To run the Flask application with Gunicorn, use the following command:

```sh
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

**Note:** Do not use Uvicorn to run the Flask application as it is not compatible with Flask's WSGI interface.
