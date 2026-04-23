"""Shared fixtures and helpers for the test suite."""

import json
import os
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def automation_dir():
    return REPO_ROOT / "automation" / "n8n-workflows"


@pytest.fixture
def infrastructure_docs_dir():
    return REPO_ROOT / "infrastructure" / "docs"


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)