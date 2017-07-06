import ntpath
import os
import subprocess
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from OJ import settings
from OJ.settings import MEDIA_ROOT


class Result:

    def __init__(self, toe, status):
        self.status = status
        self.toe = toe


class Problem(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    statement = models.CharField(max_length=500)
    input = models.CharField(max_length=100)
    output = models.CharField(max_length=100)
    constraints = models.CharField(max_length=100)
    tl = models.FloatField(default=2.00)
    ml = models.IntegerField()
    users = models.ManyToManyField(User)
    checker = models.FileField(default=settings.MEDIA_ROOT+'/default_tester.cpp')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_count(self):
        print(self.created_at)
        print("USER_COUNT")
        if self.users is None:
            return '0'
        return str(self.users.count())

    def get_file_name(self):
        return ntpath.basename(self.checker.path)

    def get_obj_file_name(self):
        return os.path.splitext(self.get_file_name())[0]

    def compile(self):
        file_name = self.get_file_name()
        name = self.get_obj_file_name()

        if os.path.isfile(name):
            os.remove(name)

        if os.path.isfile(MEDIA_ROOT + '/' + file_name):
            cmd = ['g++', '-std=c++14', '-o', name, file_name]
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

    def run_checker(self, name, test, out):
        cmd = './'+name+' '+test.inp.path+' '+test.out.path+' '+out
        r = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             cwd=MEDIA_ROOT, preexec_fn=os.setsid)
        stdout, stderr = r.communicate()
        return str(stdout, "utf-8")

    def test(self, submission):
        self.compile()
        name = self.get_obj_file_name()
        toe = 0.00
        print("Compilation successful")
        for test in self.test_set.all():
            with open(test.inp.path, 'r') as f:
                inp = f.read().replace('\n', '')
            r = submission.run(inp)
            toe = max(toe, r.toe)
            if r.status < 2:
                r.toe = toe
                os.remove(MEDIA_ROOT+'/'+name)
                return Result(toe, r.status)
            out = open(MEDIA_ROOT+'/test/tmp.txt', 'w+')
            out.write(r.stdout)
            out.close()
            flag = self.run_checker(name, test, out.name)
            os.remove(out.name)
            if flag == '0':
                os.remove(MEDIA_ROOT + '/' + name)
                return Result(toe, 4)
        print("TESTED SUCCESSFULLY")
        os.remove(MEDIA_ROOT + '/' + name)
        return Result(toe, 3)


class Test(models.Model):
    inp = models.FileField(upload_to='test/', null=True)
    out = models.FileField(upload_to='test/', null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
