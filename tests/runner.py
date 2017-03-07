import subprocess
import json


def run(cmd, raw=False):
    cmd = cmd.split()
    try:
        ret = subprocess.check_output(cmd)
    except Exception as e:
        pytest.fail(e)
    return ret if raw else json.loads(ret)
