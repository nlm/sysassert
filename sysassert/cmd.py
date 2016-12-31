import subprocess
import os

def pathexpand(command):
    defaultpath = '/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'
    command = list(command)
    if not command[0].startswith('/'):
        for path in os.environ.get('PATH', defaultpath).split(':'):
            filename = '{0}/{1}'.format(path, command[0])
            if os.path.exists(filename):
                command[0] = filename
                break
    return command

def rawcmd(command):
    process = subprocess.Popen(pathexpand(command), shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    return process.stdout.read().decode()

def cmd(command):
    process = subprocess.Popen(pathexpand(command), shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    return (process.wait(), [line.decode().strip('\n')
                             for line in process.stdout.readlines()])
