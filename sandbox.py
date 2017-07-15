import subprocess
from OJ.settings import SUDO_PASSWORD, SUDO_USER


class Sandbox:

    def __init__(self):
        self.create_sandbox()

    def create_sandbox(self):
        count = id(self)
        cmd = 'echo ' + SUDO_PASSWORD + \
              ' | sudo -S cgcreate -g cpu,memory,blkio,devices,freezer:/sandbox_' + \
              str(count) + ';\n' + 'cgset -r cpu.cfs_period_us=100000 -r ' \
                                   'cpu.cfs_quota_us=1000 sandbox_' + str(count) + ';\n' + \
              'cgset -r memory.limit_in_bytes=256M sandbox_' + str(count) + ';\n' + \
              'cgset -r devices.deny=a sandbox_' + str(count) + ';\n' \
              'sudo cgexec -g cpu,memory,blkio,devices,freezer:/sandbox_' + \
              str(count) + '   \\\n' + \
              'prlimit --nofile=256 --nproc=512 --locks=32         \\\n' \
              'unshare - -mount - -uts - -ipc - -pid - -mount - proc = / proc - -fork ' \
              'sh - c " \n' \
              'mount -t tmpfs none /home \n' \
              'mount -t tmpfs none /tmp \n' \
              'mount -t tmpfs none /sys \n' \
              'mount -t tmpfs none /var/log \n' \
              'exec su -l ' + SUDO_USER + ' \n";'
        subprocess.Popen(cmd, shell=True)
        print("CREATE : "+cmd)
        return

    def run_sandbox(self):
        cmd = 'echo ' + SUDO_PASSWORD + ' | sudo -S cgexec -g ' \
                                        'cpu,memory,blkio,devices,freezer:sandbox_' + \
              str(id(self)) + ' bash; numactl --physcpubind=+1 '
        return cmd

    def delete_sandbox(self):
        cmd = 'echo ' + SUDO_PASSWORD + ' | ' \
              'sudo -S cgdelete -g cpu,memory,blkio,devices,freezer:/sandbox_' + \
              str(id(self)) + ';rm -Rf /etc/netns/sandbox_' + str(id(self))
        print("DELETE : "+cmd)
        subprocess.Popen(cmd, shell=True)
        return

