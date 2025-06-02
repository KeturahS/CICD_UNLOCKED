import psutil
from App_SetUp.models import ServerLoadRecord

def record_server_load():
    record = ServerLoadRecord.objects.create(
        cpu_percent=psutil.cpu_percent(interval=1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage('/').percent
    )
    return record


def is_high_load(threshold_cpu=85.0, threshold_mem=90.0):
    latest = ServerLoadRecord.objects.order_by('-timestamp').first()
    if not latest:
        return False  # אם אין אף רשומה – אין עומס

    return (
        latest.cpu_percent >= threshold_cpu or
        latest.memory_percent >= threshold_mem
    )
