from .start import register_start_handlers
from .create_event import register_create_event_handlers
from .consult import register_consult_handlers
from .my_events import register_my_events_handlers
from .check_db import register_check_db_handlers  # Импортируем новый хэндлер

def register_handlers(dp):
    register_start_handlers(dp)
    register_create_event_handlers(dp)
    register_consult_handlers(dp)
    register_my_events_handlers(dp)
    register_check_db_handlers(dp)  # Регистрируем новый хэндлер