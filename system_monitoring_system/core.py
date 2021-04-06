import platform
import psutil
import time


class Get:
    def os(self):
        return platform.platform()

    def uptime(self):
        return int(time.time() - psutil.boot_time())


if __name__ == '__main__':
    exit()
