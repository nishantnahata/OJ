import os
import ntpath
import signal
import subprocess

from time import monotonic as timer
from django.core.exceptions import ValidationError
from django.db import models
from problemset.models import Problem
from OJ.settings import MEDIA_ROOT
from constants import langs
from django.contrib.auth.models import User
from sandbox import Sandbox


def validate_lang(value):
    if value not in langs:
        raise ValidationError('%s No such Language ' % value)

# For now timeout is kept constant... Later it will be updated.
timeout = 2


def compare(a, b):
    return [c for c in a if(c.isprintable() and (not c.isspace()))] == \
           [c for c in b if(c.isprintable() and (not c.isspace()))]


def get_status(returncode):
    if returncode == 124:
        return 0
    if returncode != 0:
        return 1
    return 2


class Result:

    def __init__(self, toe, status, stdout=None):
        self.stdout = str(stdout, "utf-8")
        self.status = get_status(status)
        self.toe = toe


class Submission(models.Model):
    lang = models.CharField(validators=[validate_lang], max_length=10, default='cpp')
    code = models.FileField(null=True)
    status = models.CharField(max_length=10, blank=True)
    toe = models.CharField(max_length=10, default='1.00')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
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
            return ['python', '-m', 'py_compile', file_name]

    def get_run_command(self, name, sandbox):
        cmd = sandbox.run_sandbox()
        if self.lang == 'java':
            cmd += 'java ' + name
        elif self.lang in ['c', 'cpp']:
            cmd += './' + name
        else:
            cmd += 'python3 ' + name
        print("RUN : "+cmd)
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

    def run(self, inp=None):
        name = self.get_obj_file_name()
        sandbox = Sandbox()
        cmd = self.get_run_command(name, sandbox)
        start = timer()
        stdout = b''
        stderr = b''
        env = os.environ.copy()
        r = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE, bufsize=4*1024,
                             cwd=MEDIA_ROOT, preexec_fn=os.setsid,env=env)
        try:
            if inp is not None:
                stdout, stderr = r.communicate(timeout=timeout, input=inp.encode())
            else:
                stdout, stderr = r.communicate(timeout=timeout)
            print('STDOUT : ' + str(stdout, "utf-8"))
            print('STDERR : ' + str(stderr, "utf-8"))
        except subprocess.TimeoutExpired as e:
            print("Timeout expired")
            os.killpg(r.pid, signal.SIGINT)
            r.returncode = 124
        print('Return Code : ' + str(r.returncode))
        if self.lang != 'python':
            os.remove(MEDIA_ROOT+'/'+name)
        print('Elapsed seconds: {:.2f}'.format(timer() - start))
        sandbox.delete_sandbox()
        return Result(timer() - start, r.returncode, stdout)

