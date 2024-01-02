import sys
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request
from beaker.middleware import SessionMiddleware
from app.log import create_logger
logger = create_logger(__name__)

url_map = Map()

session_opts = {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.auto': True
}


class Server:
    def application(self, environ: dict, start_response):
        """Handles HTTP requests and routes them to the appropriate endpoint."""
        request = Request(environ)
        logger.debug(f"Incoming request: {vars(request)})")
        session = environ['beaker.session']  # Access Beaker session

        try:
            urls = url_map.bind_to_environ(environ)
            endpoint, args = urls.match()
            response = endpoint(request, *args)
        except HTTPException as e:
            response = e
            logger.error(
                f"Endpoint: {request.path}, Method: {request.method}, Response Status: {e}")

        return response(environ, start_response)

    def run(self) -> None:
        """Starts the server and listens for incoming requests."""
        # Wrap the application with SessionMiddleware for session management
        app_with_sessions = SessionMiddleware(self.application, session_opts)

        try:
            logger.info("Starting server on http://127.0.0.1:4000")
            run_simple("0.0.0.0", 4000, app_with_sessions,
                       use_reloader=True, use_debugger=True)
        except Exception as e:
            logger.error("Unable to start server", exc_info=e)
            sys.exit(1)
