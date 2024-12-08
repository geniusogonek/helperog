from backend.main import main as main_backend
from frontend.main import main as main_frontend
from threading import Thread

backend_thread = Thread(target=main_backend)
backend_thread.start()

main_frontend()