import pytest

from runner import run

import os
CONFIG_PY = "config.py"


def test_backup_config_py():
    if os.path.exists(CONFIG_PY):
        os.rename(CONFIG_PY, CONFIG_PY+".pytest.bak")


def test_registry_no_args():
    run("./registry.py", raw=True)


def test_registry_init_config():
    run("./registry.py init_config", raw=True)

    import config
    assert config.gateway
    assert config.device


def test_registry_list():
    ret = run("./registry.py list")

    assert len(ret["devices"]) >= 2


def test_registry_list_query():
    ret = run("./registry.py list device=gateway")

    import config
    device = ret["devices"][0]
    assert device["uuid"] == config.gateway["uuid"]


def test_registry_register_unregister():
    reg = run("./registry.py register")
    ret = run("./registry.py unregister {uuid}".format(**reg))

    assert ret['uuid'] == reg['uuid']


def test_publisher():
    run("./publisher.py", raw=True)


def test_cleanup_config_devices():
    import config
    cmd = "./registry.py unregister {uuid}"
    run(cmd.format(**config.device))
    run(cmd.format(**config.gateway))

    os.remove("config.py")
    os.remove("config.pyc")


def test_restore_config_py():
    if os.path.exists(CONFIG_PY+".pytest.bak"):
        os.rename(CONFIG_PY+".pytest.bak", CONFIG_PY)
