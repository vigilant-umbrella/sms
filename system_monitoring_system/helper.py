import core
from exceptions import ArgumentError
from fpdf import FPDF
import os


def create_report(resource):
    pdf = FPDF(orientation='P', format='A4')
    try:
        if os.name == 'nt':
            pdf.add_font('Montserrat', '', 'Montserrat-Regular.ttf', uni=True)
            pdf.add_font('Montserrat', 'B', 'Montserrat-Bold.ttf', uni=True)
        else:
            pdf.add_font('Montserrat', '', os.path.join(
                os.path.expanduser('~'), '.sms/Montserrat-Regular.ttf'), uni=True)
            pdf.add_font('Montserrat', 'B', os.path.join(
                os.path.expanduser('~'), '.sms/Montserrat-Bold.ttf'), uni=True)
        font_style = 'Montserrat'
    except:
        font_style = 'Arial'

    g = core.Get()

    if resource == 'Main Menu':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Overall Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
        text = 'OS: {}'.format(g.os())
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Uptime: {} seconds'.format(g.uptime())
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # CPU data
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='CPU:-', ln=1)
        pdf.set_font(font_style, '', 12)
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
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Memory:-', ln=1)
        pdf.set_font(font_style, '', 12)
        memory_dict = g.memory()
        text = 'Total: {:,} Bytes'.format(memory_dict['total'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Used: {:,} Bytes'.format(memory_dict['used_incl'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Free: {:,} Bytes'.format(memory_dict['free'])
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        # Network data
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Network:-', ln=1)
        pdf.set_font(font_style, '', 12)
        networks = g.network()
        for network_dict in networks:
            text = 'Interface: {}'.format(network_dict['interface'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'IP: {}'.format(network_dict['ip'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        # Storage data
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Storage:-', ln=1)
        pdf.set_font(font_style, '', 12)
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
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Swap:-', ln=1)
        pdf.set_font(font_style, '', 12)
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
        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Users:-', ln=1)
        pdf.set_font(font_style, '', 12)
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

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='CPU Usage Summary - ', ln=1)

        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Overall:-', ln=1)
        pdf.set_font(font_style, '', 12)
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
        for cpu_core in cpu_dict['cores']:
            pdf.ln()
            pdf.set_font(font_style, 'B', 16)
            text = 'Core {}:-'.format(counter)
            pdf.cell(0, h=15, txt=text, ln=1)
            pdf.set_font(font_style, '', 12)
            text = 'User: {} %'.format(cpu_core['user'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'System: {} %'.format(cpu_core['system'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Idle: {} %'.format(cpu_core['idle'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'I/O Wait: {} %'.format(cpu_core['iowait'])
            pdf.cell(0, h=5, txt=text, ln=1)
            counter += 1

    elif resource == 'Memory':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Memory Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
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

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Network Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
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

        speed_dict = core.test_speed()

        text = 'Download speed: {}'.format(speed_dict['down_speed'])
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Upload speed: {}'.format(speed_dict['up_speed'])
        pdf.cell(0, h=5, txt=text, ln=1)

    elif resource == 'Storage':
        pdf.add_page()
        pdf.set_author('SMS')

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Storage Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
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

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Process Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
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

        pdf.set_font(font_style, 'B', 10)
        pdf.cell(0, txt='System Monitoring System', ln=1, align='C')

        pdf.set_font(font_style, 'B', 32)
        pdf.cell(0, h=25, txt='Report', ln=1, align='C')

        pdf.set_font(font_style, 'B', 20)
        pdf.cell(0, h=15, txt='Miscellaneous Usage Summary - ', ln=1)

        pdf.set_font(font_style, '', 12)
        text = 'OS: {}'.format(g.os())
        pdf.cell(0, h=5, txt=text, ln=1)
        text = 'Uptime: {} seconds'.format(g.uptime())
        pdf.cell(0, h=5, txt=text, ln=1)
        pdf.ln()

        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Users:-', ln=1)
        pdf.set_font(font_style, '', 12)
        users = g.users()
        for user_dict in users:
            text = 'Name: {}'.format(user_dict['name'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Session started: {}'.format(user_dict['sess_started'])
            pdf.cell(0, h=5, txt=text, ln=1)
            text = 'Host: {}'.format(user_dict['host'])
            pdf.cell(0, h=5, txt=text, ln=1)
            pdf.ln()

        pdf.set_font(font_style, 'B', 16)
        pdf.cell(0, h=15, txt='Swap:-', ln=1)
        pdf.set_font(font_style, '', 12)
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


if __name__ == '__main__':
    exit()
