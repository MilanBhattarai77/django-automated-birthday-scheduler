import os
from celery import Celery

# Set the default Django settings module for the Celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classbased.settings')

# Create a Celery instance and configure it with settings from Django
app = Celery('classbased')

# Load task modules from all registered Django apps (e.g., myapps.tasks)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    Debug task to print request information for troubleshooting Celery setup.
    """
    print(f'Request: {self.request!r}')