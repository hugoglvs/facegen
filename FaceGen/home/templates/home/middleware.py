# middleware.py
import os
import signal

class SubprocessTerminationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if there is a stored PID
        pid = request.session.get('subprocess_pid')

        if pid:
            try:
                # Send a signal to terminate the process
                os.kill(pid, signal.SIGTERM)
                # Optionally, remove the PID from the session
                del request.session['subprocess_pid']
            except ProcessLookupError:
                # Process already terminated
                pass

        response = self.get_response(request)
        return response

# Add your middleware in settings.py
MIDDLEWARE = [
    # Other middleware...
    'your_app.middleware.SubprocessTerminationMiddleware',
]
