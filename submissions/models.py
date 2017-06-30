import os
import ntpath
import signal
import subprocess

import resource

from time import monotonic as timer
from django.core.exceptions import ValidationError
from django.db import models

from OJ.settings import MEDIA_ROOT
from langs import langs
from django.contrib.auth.models import User


def validate_lang(value):
    if value not in langs:
        raise ValidationError('%s No such Language ' % value)

# For now timeout is kept constant... Later it will be updated.
timeout = 2


class Submission(models.Model):
    lang = models.CharField(validators=[validate_lang], max_length=10, default='cpp')
    code = models.FileField(null=True)
    status = models.CharField(max_length=10, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_map = {
        'c': '.c',
        'cpp': '.cpp',
        'java': '.java',
        'python': '.py'
    }

    def get_file_name(self):
        return ntpath.basename(self.code.path)

    def get_obj_file_name(self):
        name = os.path.splitext(self.get_file_name())[0]
        if self.lang == 'java':
            name += '.class'
        if self.lang == 'python':
            return self.get_file_name()
        return name

    def get_compile_command(self, name, file_name):
        if self.lang == 'java':
            return ['javac', file_name]
        elif self.lang == 'c':
            return ['gcc', '-o', name, file_name]
        elif self.lang == 'cpp':
            return ['g++', '-std=c++14', '-o', name, file_name]
        else:
            cmd = ['python3', file_name]
        return cmd

    def get_run_command(self, name):
        if self.lang == 'java':
            cmd = 'java ' + name
        elif self.lang in ['c', 'cpp']:
            cmd = './' + name
        else:
            cmd = 'python3 ' + name
        return cmd

    def compile(self):
        file_name = self.get_file_name()
        name = self.get_obj_file_name()

        if os.path.isfile(name) and \
                self.lang != 'python':
            os.remove(name)

        if os.path.isfile(MEDIA_ROOT+'/'+file_name):
            cmd = self.get_compile_command(name, file_name)
            print(cmd)
            r = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, cwd=MEDIA_ROOT)
            print("COMPILATION SUCCESSFUL!!")
            stderr = r.communicate()[1]
            if stderr:
                print(stderr)
                return stderr
            else:
                return 200
        else:
            return 404

    def run(self, test):
        name = self.get_obj_file_name()
        cmd = self.get_run_command(name)
        start = timer()
        env = os.environ.copy()
        print(resource.RLIM_INFINITY)
        r = subprocess.Popen(cmd, shell=True,
                             stdin=test, stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE, bufsize=4*1024,
                             cwd=MEDIA_ROOT, preexec_fn=os.setsid,
                             env=env)
        try:
            stdout, stderr = r.communicate(timeout=timeout)
            print(stderr)
        except subprocess.TimeoutExpired as e:
            print("Timeout expired")
            os.killpg(r.pid, signal.SIGINT)
            r.returncode = 124
        print(r.returncode)
        if self.lang != 'python':
            os.remove(name)
        print('Elapsed seconds: {:.2f}'.format(timer() - start))
        return r, '{:.2f}'.format(timer() - start)


class Test(models.Model):
    inp = models.FileField(upload_to='test/', null=True)
    out = models.FileField(upload_to='test/', null=True)
