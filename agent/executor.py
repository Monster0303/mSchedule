from subprocess import Popen, PIPE


class Executor:
    def run(self, script, timeout=None):
        proc = Popen(script, shell=True, stdout=PIPE)
        code = proc.wait(timeout=timeout)
        output = proc.stdout.read()

        return code, output
