import subprocess
import json

import pytest


def run(cmd, raw=False):
    cmd = cmd.split()
    try:
        ret = subprocess.check_output(cmd)
    except Exception as e:
        print(e.output)
        pytest.fail(e)
    return ret if raw else json.loads(ret)
