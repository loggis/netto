####################################################################################
### Anggi Agista
### email : agista.mailrespon@gmail.com
#####################################################################################

from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    sshport = models.IntegerField(default=22)
    TYPE_CHOICES = (
        ('router', 'Router'),
        ('switch', 'Switch')
    )
    device_type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True)
    SERIES_DEVICES = (
        ('Cisco Industrial Ethernet 2000 Switches','Cisco Industrial Ethernet 2000 Switches'),
        ('Cisco Industrial Ethernet 3000 Switches','Cisco Industrial Ethernet 3000 Switches'),
        ('Cisco Industrial Ethernet 4000 Switches','Cisco Industrial Ethernet 4000 Switches'),
        ('Cisco Industrial Ethernet 5000 Switches','Cisco Industrial Ethernet 5000 Switches'),
        ('Cisco Switch Catalyst 4500','Cisco Switch Catalyst 4500'),
        ('Cisco Switch Catalyst 4900','Cisco Switch Catalyst 4900'),
        ('Cisco Switch Catalyst 6800','Cisco Switch Catalyst 6800'),
        ('Cisco Switch Catalyst 3560','Cisco Switch Catalyst 3560'),
        ('Cisco Switch Catalyst 3750','Cisco Switch Catalyst 3750'),
        ('Cisco Switch Catalyst 6500','Cisco Switch Catalyst 6500'),
        ('Cisco Router ISR 1900','Cisco Router ISR 1900'),
        ('Cisco Router ISR 2900','Cisco Router ISR 2900'),
        ('Cisco Router ISR 3900','Cisco Router ISR 3900'),
        ('Cisco Router ISR 4000','Cisco Router ISR 4000'),
        ('Cisco Router ISR 1100','Cisco Router ISR 1100'),
        ('Cisco Router ISR 800','Cisco Router ISR 800'),
        ('Cisco Router ISR 900','Cisco Router ISR 900'),
        ('Cisco Router ASR 900','Cisco Router ASR 900'),
        ('Cisco Router ASR 1000','Cisco Router ASR 1000'),
        ('Cisco Router ASR 5000','Cisco Router ASR 5000'),
        ('Cisco Router ASR 9000','Cisco Router ASR 9000'),
        ('Cisco 8000 Series Routers','Cisco 8000 Series Routers'),
        ('Cisco Router 10000 Series','Cisco Router 10000 Series'),
        ('Cisco Router 12000 Series','Cisco Router 12000 Series'),
        ('Cisco Router ISR 1800','Cisco Router ISR 1800'),
        ('Cisco Router ISR 2800','Cisco Router ISR 2800'),
        ('Cisco Router ISR 3800','Cisco Router ISR 3800'),
        ('Cisco Router 7200 Series','Cisco Router 7200 Series'),
        ('Cisco Router 7600 Series','Cisco Router 7600 Series')
    )
    device_series = models.CharField(max_length=255, choices=SERIES_DEVICES, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} - {} - {} - {}".format(self.id, self.ip_address, self.hostname, self.device_type)

class Log(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    host = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)
    commandline = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.host, self.action, self.status)