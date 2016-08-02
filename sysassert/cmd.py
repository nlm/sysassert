import subprocess

def rawcmd(command):
    process = subprocess.Popen(command, shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    return process.stdout.read().decode()

def cmd(command):
    process = subprocess.Popen(command, shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    return (process.wait(), [line.decode().strip('\n')
                             for line in process.stdout.readlines()])
