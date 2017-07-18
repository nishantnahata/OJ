import subprocess
from OJ.settings import SUDO_PASSWORD, SUDO_USER


class Sandbox:

    def __init__(self):
        self.create_sandbox()

    def create_sandbox(self):
        count = id(self)
        cmd = 'echo ' + SUDO_PASSWORD + \
              ' | sudo -S cgcreate -g cpu,memory,blkio,devices,freezer:/sandbox_' + \
              str(count) + ';\n' + \
              'sudo cgset -r memory.limit_in_bytes=256M sandbox_' + str(count) + ';\n' \
              'sudo cgset -r memory.soft_limit_in_bytes=256M sandbox_' + str(count) + ';\n' \
              'sudo cgset -r memory.kmem.limit_in_bytes=256M sandbox_' + str(count) + ';\n' \
              'sudo cgset -r memory.memsw.limit_in_bytes=256M sandbox_' + str(count) + ';\n'
        subprocess.Popen(cmd, shell=True)
        print("CREATE : "+cmd)
        return

    def run_sandbox(self):
        cmd = 'echo ' + SUDO_PASSWORD + ' | sudo -S unshare --mount;sudo unshare --mount;' \
              'sudo cgexec -g cpu,memory,blkio,devices,freezer:sandbox_' + \
              str(id(self)) + ' numactl --physcpubind=+1 '
        return cmd

    def delete_sandbox(self):
        cmd = 'echo ' + SUDO_PASSWORD + ' | ' \
              'sudo -S cgdelete -g cpu,memory,blkio,devices,freezer:/sandbox_' + \
              str(id(self)) + ';rm -Rf /etc/netns/sandbox_' + str(id(self))
        print("DELETE : "+cmd)
        subprocess.Popen(cmd, shell=True)
        return

