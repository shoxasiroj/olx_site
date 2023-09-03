from datetime import datetime


def get_timed_path(instance, filename):
    return f"{datetime.now().timestamp()} {filename}"
