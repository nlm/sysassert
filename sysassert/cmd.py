import subprocess

def rawcmd(command):
    p = subprocess.Popen(command, shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return p.stdout.read().decode()

def cmd(command):
    p = subprocess.Popen(command, shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return (p.wait(), [line.decode().strip('\n')
                       for line in p.stdout.readlines()])
