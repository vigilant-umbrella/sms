from datetime import datetime
import ifcfg
import os
import platform
import psutil
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

    def cpu_overall(self):
        return psutil.cpu_percent(interval=1)

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
        for p in psutil.process_iter():
            p_dict = {}
            p_dict['pid'] = p.pid
            p_dict['name'] = p.name()
            p_dict['user'] = p.username()
            p_dict['status'] = p.status()
            p_dict['created'] = p.create_time()
            p_dict['memory'] = p.memory_percent()
            p_dict['cpu'] = p.cpu_percent(0)

            yield p_dict

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
            net_dict['ip'] = ip_details[net]['inet'] if ip_details[net]['inet'] != None else 'None'
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


if __name__ == '__main__':
    exit()
