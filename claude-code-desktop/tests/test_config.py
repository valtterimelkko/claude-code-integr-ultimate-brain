import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from config import config_path, load_config  # noqa: E402


def test_default_config_is_user_local(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("NOTION_CONFIG_FILE", raising=False)

    assert config_path() == tmp_path / "config" / "ultimate-brain-notion" / "env.conf"


def test_common_uses_database_ids_from_config(monkeypatch, tmp_path):
    config = tmp_path / "env.conf"
    config.write_text("NOTES_DB_ID=notes-123\nPROJECTS_DB_ID=projects-456\n")
    monkeypatch.setenv("NOTION_CONFIG_FILE", str(config))
    sys.modules.pop("common", None)

    common = importlib.import_module("common")

    assert common.NOTES_DB_ID == "notes-123"
    assert common.PROJECTS_DB_ID == "projects-456"


def test_installer_uses_user_local_config_without_sudo_or_source_mutation():
    installer = Path(__file__).resolve().parents[1] / "install.sh"
    content = installer.read_text()

    assert "sudo " not in content
    assert "common.py.backup" not in content
    assert "XDG_CONFIG_HOME" in content


def test_load_config_reads_values_without_executing_shell(monkeypatch, tmp_path):
    config = tmp_path / "env.conf"
    config.write_text(
        "NOTES_DB_ID=notes-123\n"
        "PROJECTS_DB_ID=projects-456\n"
        "NOTION_TOKEN=secret-example\n"
        "IGNORED_LINE\n"
    )
    monkeypatch.setenv("NOTION_CONFIG_FILE", str(config))

    values = load_config()

    assert values["NOTES_DB_ID"] == "notes-123"
    assert values["PROJECTS_DB_ID"] == "projects-456"
    assert values["NOTION_TOKEN"] == "secret-example"
    assert "IGNORED_LINE" not in values
