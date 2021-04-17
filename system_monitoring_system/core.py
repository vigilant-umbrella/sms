from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from exceptions import ArgumentError
from fpdf import FPDF
import ifcfg
import os
import platform
import psutil
import secrets
import smtplib
import speedtest
import time


class Get:
    def os(self):
        return platform.platform()

    def uptime(self):
        return int(time.time() - psutil.boot_time())

    def cpu(self):
        result = {}
        result['load_avg'] = os.getloadavg()
        overall = psutil.cpu_times_percent(interval=1)
        result['user'] = overall.user
        result['system'] = overall.system
        result['idle'] = overall.idle
        result['iowait'] = overall.iowait

        num_cores = 0
        cores_dicts = []
        for core in psutil.cpu_times_percent(interval=1, percpu=True):
            cores_dicts.append(dict())
            cores_dicts[num_cores]['user'] = core.user
            cores_dicts[num_cores]['system'] = core.system
            cores_dicts[num_cores]['idle'] = core.idle
            cores_dicts[num_cores]['iowait'] = core.iowait
            num_cores += 1

        result['num_cores'] = num_cores
        result['cores'] = tuple(cores_dicts)

        return result

    def memory(self):
        result = {}
        details = psutil.virtual_memory()
        result['total'] = details.total
        result['available'] = details.available
        result['used_excl'] = details.total-details.available
        result['used_incl'] = details.used
        result['percent'] = details.percent
        result['free'] = details.free

        return result

    def process(self):
        result = []

        for p in psutil.process_iter():
            p_dict = {}
            p_dict['pid'] = p.pid
            p_dict['name'] = p.name()
            p_dict['user'] = p.username()
            p_dict['status'] = p.status()
            p_dict['created'] = p.create_time()
            p_dict['memory'] = p.memory_percent()
            p_dict['cpu'] = p.cpu_percent(0)
            result.append(p_dict)

        return tuple(result)

    def storage(self):
        result = []

        for partition in psutil.disk_partitions():
            parition_dict = {}
            parition_dict['device'] = partition.device
            parition_dict['mountpoint'] = partition.mountpoint
            parition_dict['fstype'] = partition.fstype
            parition_dict['options'] = partition.opts
            usage = psutil.disk_usage(partition.mountpoint)
            parition_dict['total'] = usage.total
            parition_dict['used'] = usage.used
            parition_dict['free'] = usage.free
            parition_dict['percent'] = usage.percent
            result.append(parition_dict)

        return tuple(result)

    def network(self):
        result = []

        details = psutil.net_io_counters(pernic=True)
        ip_details = ifcfg.interfaces()
        for net in details.keys():
            net_dict = {}
            net_dict['interface'] = net
            net_dict['ip'] = ip_details[net]['inet']
            net_dict['bytes_sent'] = details[net].bytes_sent
            net_dict['bytes_recv'] = details[net].bytes_recv
            net_dict['packets_sent'] = details[net].packets_sent
            net_dict['packets_recv'] = details[net].packets_recv
            net_dict['errin'] = details[net].errin
            net_dict['errout'] = details[net].errout
            net_dict['dropin'] = details[net].dropin
            net_dict['dropout'] = details[net].dropout
            result.append(net_dict)

        return tuple(result)

    def swap(self):
        result = {}
        details = psutil.swap_memory()
        result['total'] = details.total
        result['used'] = details.used
        result['free'] = details.free
        result['percent'] = details.percent
        result['sin'] = details.sin
        result['sout'] = details.sout

        return result

    def users(self):
        result = []

        for user in psutil.users():
            user_dict = {}
            user_dict['name'] = user.name
            user_dict['sess_started'] = datetime.utcfromtimestamp(user.started)
            user_dict['host'] = user.host
            result.append(user_dict)

        return tuple(result)


def test_speed():
    result = {}

    s = speedtest.Speedtest()
    s.download()
    s.upload()
    speed_dict = s.results.dict()

    result['down_speed'] = speed_dict['download']
    result['up_speed'] = speed_dict['upload']

    return result


def create_report(resource):
    pdf = FPDF(orientation='P', format='A4')
    pdf.add_font('Montserrat', '', 'Montserrat-Regular.ttf', uni=True)
    pdf.add_font('Montserrat', 'B', 'Montserrat-Bold.ttf', uni=True)

    g = Get()

    if resource == 'Main Menu':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Overall Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        text = 'OS: {}'.format(g.os())
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Uptime: {} seconds'.format(g.uptime())
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # CPU data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='CPU:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        cpu_dict = g.cpu()
        text = 'Load Average: {} {} {}'.format(
            cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'User: {} %'.format(cpu_dict['user'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'System: {} %'.format(cpu_dict['system'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Idle: {} %'.format(cpu_dict['idle'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'I/O Wait: {} %'.format(cpu_dict['iowait'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Cores: {}'.format(cpu_dict['num_cores'])
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # Memory data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Memory:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        memory_dict = g.memory()
        text = 'Total: {:,} Bytes'.format(memory_dict['total'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used: {:,} Bytes'.format(memory_dict['used_incl'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Free: {:,} Bytes'.format(memory_dict['free'])
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # Network data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Network:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        networks = g.network()
        for network_dict in networks:
            text = 'Interface: {}'.format(network_dict['interface'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'IP: {}'.format(network_dict['ip'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        # Storage data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Storage:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        storages = g.storage()
        for storage_dict in storages:
            text = 'Device: {}'.format(storage_dict['device'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Mounted: {}'.format(storage_dict['mountpoint'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Total: {:,} Bytes'.format(storage_dict['total'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Used: {:,} Bytes ({}%)'.format(
                storage_dict['used'], storage_dict['percent'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Free: {:,} Bytes'.format(storage_dict['free'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        # Swap data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Swap:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        swap_dict = g.swap()
        text = 'Total: {:,} Bytes'.format(swap_dict['total'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used: {:,} Bytes ({}%)'.format(
            swap_dict['used'], swap_dict['percent'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Free: {:,} Bytes'.format(swap_dict['free'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Swapped in: {:,} Bytes'.format(swap_dict['sin'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Swapped out: {:,} Bytes'.format(swap_dict['sout'])
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # Users data
        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Users:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        users = g.users()
        for user_dict in users:
            text = 'Name: {}'.format(user_dict['name'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Session started: {}'.format(user_dict['sess_started'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Host: {}'.format(user_dict['host'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

    elif resource == 'CPU':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='CPU Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Overall:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        cpu_dict = g.cpu()
        text = 'Load Average: {} {} {}'.format(
            cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'User: {} %'.format(cpu_dict['user'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'System: {} %'.format(cpu_dict['system'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Idle: {} %'.format(cpu_dict['idle'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'I/O Wait: {} %'.format(cpu_dict['iowait'])
        pdf.cell(0, h=5, txt=text, ln=1)

        counter = 1
        for core in cpu_dict['cores']:
            pdf.ln()
            pdf.set_font('Montserrat', 'B', 16)
            text = 'Core {}:-'.format(counter)
            pdf.cell(0, h=15, txt=text, ln=1)
            pdf.set_font('Montserrat', '', 12)
            text = 'User: {} %'.format(core['user'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'System: {} %'.format(core['system'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Idle: {} %'.format(core['idle'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'I/O Wait: {} %'.format(core['iowait'])
            pdf.cell(0, h=5, txt=text, ln=1)
            counter += 1

    elif resource == 'Memory':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Memory Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        memory_dict = g.memory()
        text = 'Total: {:,} Bytes'.format(memory_dict['total'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Available: {:,} Bytes'.format(memory_dict['available'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used (excl. Cache & buffer): {:,} Bytes ({}%)'.format(
            memory_dict['used_excl'], memory_dict['percent'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used (incl. Cache & buffer): {:,} Bytes'.format(
            memory_dict['used_incl'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Free: {:,} Bytes'.format(memory_dict['free'])
        pdf.cell(0, h=5, txt=text, ln=1)

    elif resource == 'Network':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Network Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        networks = g.network()
        for network_dict in networks:
            text = 'Interface: {}'.format(network_dict['interface'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'IP: {}'.format(network_dict['ip'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Bytes sent: {}'.format(network_dict['bytes_sent'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Bytes received: {}'.format(network_dict['bytes_recv'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Packets sent: {}'.format(network_dict['packets_sent'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Packets received: {}'.format(network_dict['packets_recv'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Errors in: {}'.format(network_dict['errin'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Errors out: {}'.format(network_dict['errout'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Dropped in: {}'.format(network_dict['dropin'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Dropped out: {}'.format(network_dict['dropout'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        speed_dict = test_speed()

        text = 'Download speed: {}'.format(speed_dict['down_speed'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Upload speed: {}'.format(speed_dict['up_speed'])
        pdf.cell(0, h=5, txt=text, ln=1)

    elif resource == 'Storage':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Storage Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        storages = g.storage()
        for storage_dict in storages:
            text = 'Device: {}'.format(storage_dict['device'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Mounted: {}'.format(storage_dict['mountpoint'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Type: {}'.format(storage_dict['fstype'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Options: {}'.format(storage_dict['options'])
            pdf.multi_cell(0, h=5, txt=text)
            text = 'Total: {:,} Bytes'.format(storage_dict['total'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Used: {:,} Bytes ({}%)'.format(
                storage_dict['used'], storage_dict['percent'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Free: {:,} Bytes'.format(storage_dict['free'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

    elif resource == 'Process':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Process Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        processes = g.process()
        for process_dict in processes:
            text = 'PID: {}'.format(process_dict['pid'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Name: {}'.format(process_dict['name'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'User: {}'.format(process_dict['user'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Status: {}'.format(process_dict['status'])
            pdf.multi_cell(0, h=5, txt=text)
            text = 'Created: {} seconds since the epoch'.format(
                process_dict['created'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Memory: {} %'.format(process_dict['memory'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'CPU: {} %'.format(process_dict['cpu'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

    elif resource == 'Miscellaneous':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font('Montserrat', 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font('Montserrat', 'B', 20)
        pdf.cell(0, h=15, txt='Miscellaneous Usage Summary - ', ln=1)

        pdf.set_font('Montserrat', '', 12)
        text = 'OS: {}'.format(g.os())
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Uptime: {} seconds'.format(g.uptime())
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Users:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        users = g.users()
        for user_dict in users:
            text = 'Name: {}'.format(user_dict['name'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Session started: {}'.format(user_dict['sess_started'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Host: {}'.format(user_dict['host'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        pdf.set_font('Montserrat', 'B', 16)
        pdf.cell(0, h=15, txt='Swap:-', ln=1)
        pdf.set_font('Montserrat', '', 12)
        swap_dict = g.swap()
        text = 'Total: {:,} Bytes'.format(swap_dict['total'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used: {:,} Bytes ({}%)'.format(
            swap_dict['used'], swap_dict['percent'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Free: {:,} Bytes'.format(swap_dict['free'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Swapped in: {:,} Bytes'.format(swap_dict['sin'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Swapped out: {:,} Bytes'.format(swap_dict['sout'])
        pdf.cell(0, h=5, txt=text, ln=1)

    else:
        msg = 'Invalid Arugment Provided while creating report.'
        raise ArgumentError(msg)

    return pdf


def down_report(resource='Main Menu'):
    pdf = create_report(resource)

    download_folder = ''
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        download_folder = location
    else:
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    pdf.output(download_folder+'/report.pdf', 'F')


def send_email(resource='Main Menu'):
    pdf = create_report(resource)

    sender = secrets.USERNAME
    password = secrets.PASSWORD
    receivers = ['bcs_2019008@iiitm.ac.in',
                 'bcs_2019075@iiitm.ac.in', 'bcs_2019025@iiitm.ac.in']

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'System Monitoring System'
    message['To'] = ', '.join(receivers)
    message['Subject'] = 'Report - System Monitoring System'

    body = """
    Hi,

    Please find attached the report you requested.

    Regards,
    System Monitoring System Team
    """

    message.attach(MIMEText(body, 'plain'))

    payload = MIMEBase('application', 'octate-stream', Name='report.pdf')
    payload.set_payload(pdf.output('report.pdf', 'S'))

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition',
                       'attachment', filename='report.pdf')
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, receivers, text)
    session.quit()
    print('Mail Sent')


if __name__ == '__main__':
    exit()
