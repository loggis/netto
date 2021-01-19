####################################################################################
### 
#####################################################################################

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Device, Log
import time
import paramiko
from django.contrib.auth.decorators import login_required
from .resources import DeviceResource
from paramiko import SSHClient, AutoAddPolicy
import os

@login_required
def index(request):
    total_devices = Device.objects.all()
    log_activity = Log.objects.all()
    log_persentase = len(log_activity)*100/10000
    persentase_act = 'width:' + str(log_persentase) + '%'
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'total_devices': len(total_devices),
        'log_persentase': persentase_act,
        'logs': logsrec,
        'total_log': len(logsrec),
    }
    return render(request, 'netto/index.html', context)

@login_required
def configt(request):
    #for configure terminal
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_devicecft')
        selected_command = request.POST.get('rbconft')
        cisco_command = request.POST['txt_cisco_commandcft'].splitlines()
        sleept = int(request.POST['paramtscft'])
        if selected_command == 'conft':
            for x in selected_devices_id:
                try:
                    alat = get_object_or_404(Device, pk=x)
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                    conn = ssh_client.invoke_shell()
                    conn.send("conf t\n")
                    for cmd in cisco_command:
                        conn.send(cmd + "\n")
                        time.sleep(sleept)
                        log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Success", time=datetime.now(), messages="No Errors", commandline=cmd)
                        log.save()
                except Exception as e:
                    log = Log(device_id=alat, host=alat.ip_address, action="Configure Terminal", status="Failed", time=datetime.now(), messages=e, commandline=cisco_command)
                    log.save()
            return redirect('configt')
        else:
            for x in selected_devices_id:
                try:
                    alat = get_object_or_404(Device, pk=x)
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal length 0\n')
                    for cmd in cisco_command:
                        result.append("Result on {}".format(alat.ip_address))
                        conn.send(cmd + "\n")
                        time.sleep(sleept)
                        output = conn.recv(65535)
                        result.append(output.decode())
                        log = Log(device_id=alat, host=alat.ip_address, action="Show Verification", status="Success", time=datetime.now(), messages="No Errors", commandline=cmd)
                        log.save()
                except Exception as e:
                    log = Log(device_id=alat, host=alat.ip_address, action="Show Verification", status="Failed", time=datetime.now(), messages=e, commandline=cisco_command)
                    log.save()
            result = "\n".join(result)
            return render(request, 'netto/verify_result.html', {'result':result})
         
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'total_log': len(logsrec),
            'mode': 'Command Line',
            'logs': logsrec
        }
        return render(request, 'netto/conft.html', context)

@login_required
def deviceslist(request):
    total_devices = Device.objects.all()
    logsrec = Log.objects.all().order_by('-time')[:4]
    context = {
        'total_devices': len(total_devices),
        'list_devices': total_devices,
        'total_log': len(logsrec),
        'logs': logsrec
    }
    return render(request, 'netto/devices-list.html', context)
    
@login_required
def log(request):
    logsrec = Log.objects.all().order_by('-time')[:4]
    logs = Log.objects.all().order_by('-time')[:30]
    context = {
        'logs': logsrec,
        'total_log': len(logsrec),
        'logs1': logs
    }
    return render(request, 'netto/log.html', context)


@login_required
def saveconf(request):
    #for save conf
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                result.append("Result on {}".format(alat.ip_address))
                conn.send('write\n')
                time.sleep(sleept)
                output = conn.recv(65535)
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="Save Configurations", status="Success", time=datetime.now(), messages="No Errors", commandline="write memory")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="Save Configurations", status="Failed", time=datetime.now(), messages=e, commandline="write memory")
                log.save()
        result = "\n".join(result)
        return render(request, 'netto/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Save Configure',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'netto/saveconf.html', context)

@login_required
def pinging(request):
    if request.method == "POST":
        selected_devices_id = request.POST.getlist('cxb_device')
        result = []
        for x in selected_devices_id:
            alat = get_object_or_404(Device, pk=x)
            response = os.popen(f"ping {alat.ip_address}").read()
            if "Received = 4" in response:
                result.append(f"UP {alat.ip_address} Ping OK")
            else:
                result.append(f"DOWN {alat.ip_address} Ping Timeout")
        result = "\n".join(result) 
        return render(request, 'netto/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Pinging',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'netto/pinging.html', context)       

def reload(request):
    #for reload
    if request.method == "POST":
        result = []
        selected_devices_id = request.POST.getlist('cxb_device')
        sleept = int(request.POST['paramts'])
        for x in selected_devices_id:
            try:
                alat = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=alat.ip_address, username=alat.username, password=alat.password, allow_agent=False)
                conn = ssh_client.invoke_shell()
                conn.send('terminal length 0\n')
                #conn.send('reload\n')
                conn.send('reload\n') 
                time.sleep(sleept)
                conn.send('yes\n')
                time.sleep(sleept)
                conn.send('yes\n')
                output = conn.recv(65535)
                #result.append("Result on {}".format(alat.ip_address))
                result.append(output.decode())
                log = Log(device_id=alat, host=alat.ip_address, action="Reload", status="Success", time=datetime.now(), messages="No Errors", commandline="reload")
                log.save()
            except Exception as e:
                log = Log(device_id=alat, host=alat.ip_address, action="Reload", status="Failed", time=datetime.now(), messages=e, commandline="reload")
                log.save()
        result = "\n".join(result)
        return render(request, 'netto/verify_result.html', {'result':result})     
    else:
        devi = Device.objects.all()
        logsrec = Log.objects.all().order_by('-time')[:4]
        context = {
            'total_devices': len(devi),
            'devi': devi,
            'mode': 'Reload Devices',
            'total_log': len(logsrec),
            'logs': logsrec
        }
        return render(request, 'netto/reload.html', context)

@login_required
def verifcli(request, id):
    #for verify cli
    logcli = Log.objects.get(pk = id)
    return render(request, 'netto/verify_cli.html', {'logcli': logcli})

