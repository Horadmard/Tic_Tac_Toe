from subprocess import Popen

commands = ['client.py', 'client.py', 'server.py']
procs = [Popen(['python', i]) for i in commands]
for p in procs:
    p.wait()
