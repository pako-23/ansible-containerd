import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("containerd")


def test_container_runtime(host):
    assert host.find_command("runc")
    assert host.find_command("containerd")


def test_container_runtime_started(host):
    service = host.service("containerd")
    assert service.is_enabled
    assert service.is_running


def test_container_runtime_config(host):
    config_file = host.file("/etc/containerd/config.toml")
    assert config_file.exists
    assert config_file.is_file
    assert config_file.user == "root"
    assert config_file.group == "root"
    assert config_file.mode == 0o644
    assert len(config_file.content) > 0
    assert config_file.content_string[-1] == "\n"
