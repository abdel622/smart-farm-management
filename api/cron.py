from .models import Device

def my_cron_job():
    # your functionality goes here
    Device.objects.create(type='field')
    print("Hello")