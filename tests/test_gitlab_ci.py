"""Tests for .gitlab-ci.yml (new file added in this PR).

Covers: YAML parse validity, required stages, job structure, rules,
runner tags, and script content.
"""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
CI_PATH = REPO_ROOT / ".gitlab-ci.yml"


@pytest.fixture(scope="module")
def ci_config():
    with open(CI_PATH) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Parse & top-level structure
# ---------------------------------------------------------------------------

class TestCITopLevel:
    def test_file_exists(self):
        assert CI_PATH.exists(), ".gitlab-ci.yml must exist"

    def test_file_is_valid_yaml(self):
        with open(CI_PATH) as f:
            data = yaml.safe_load(f)
        assert data is not None

    def test_stages_key_present(self, ci_config):
        assert "stages" in ci_config

    def test_stages_is_list(self, ci_config):
        assert isinstance(ci_config["stages"], list)

    def test_stages_not_empty(self, ci_config):
        assert len(ci_config["stages"]) > 0

    def test_sync_stage_declared(self, ci_config):
        assert "sync" in ci_config["stages"]


# ---------------------------------------------------------------------------
# mesh-sync job
# ---------------------------------------------------------------------------

class TestMeshSyncJob:
    def test_mesh_sync_job_exists(self, ci_config):
        assert "mesh-sync" in ci_config

    def test_mesh_sync_job_is_dict(self, ci_config):
        assert isinstance(ci_config["mesh-sync"], dict)

    def test_mesh_sync_stage_is_sync(self, ci_config):
        assert ci_config["mesh-sync"]["stage"] == "sync"

    def test_mesh_sync_has_tags(self, ci_config):
        assert "tags" in ci_config["mesh-sync"]
        tags = ci_config["mesh-sync"]["tags"]
        assert isinstance(tags, list) and len(tags) > 0

    def test_mesh_sync_tags_include_vps(self, ci_config):
        assert "vps" in ci_config["mesh-sync"]["tags"]

    def test_mesh_sync_tags_include_mesh_sync(self, ci_config):
        assert "mesh-sync" in ci_config["mesh-sync"]["tags"]

    def test_mesh_sync_has_rules(self, ci_config):
        assert "rules" in ci_config["mesh-sync"]
        rules = ci_config["mesh-sync"]["rules"]
        assert isinstance(rules, list) and len(rules) > 0

    def test_mesh_sync_has_script(self, ci_config):
        assert "script" in ci_config["mesh-sync"]
        script = ci_config["mesh-sync"]["script"]
        assert isinstance(script, list) and len(script) > 0

    def test_mesh_sync_script_uses_mesh_sync_sh(self, ci_config):
        script = ci_config["mesh-sync"]["script"]
        full_script = "\n".join(script)
        assert "mesh-sync.sh" in full_script

    def test_mesh_sync_script_passes_branch_ref(self, ci_config):
        script = ci_config["mesh-sync"]["script"]
        full_script = "\n".join(script)
        assert "$CI_COMMIT_REF_NAME" in full_script


# ---------------------------------------------------------------------------
# Rules structure
# ---------------------------------------------------------------------------

class TestMeshSyncRules:
    def test_rules_trigger_on_push(self, ci_config):
        rules = ci_config["mesh-sync"]["rules"]
        push_rule = next(
            (r for r in rules if r.get("if") == '$CI_PIPELINE_SOURCE == "push"'),
            None,
        )
        assert push_rule is not None, "No rule for push events found"

    def test_rules_trigger_on_merge_request(self, ci_config):
        rules = ci_config["mesh-sync"]["rules"]
        mr_rule = next(
            (r for r in rules if r.get("if") == '$CI_PIPELINE_SOURCE == "merge_request_event"'),
            None,
        )
        assert mr_rule is not None, "No rule for merge_request_event found"

    def test_push_rule_runs_on_success(self, ci_config):
        rules = ci_config["mesh-sync"]["rules"]
        push_rule = next(
            (r for r in rules if r.get("if") == '$CI_PIPELINE_SOURCE == "push"'),
            None,
        )
        assert push_rule is not None
        assert push_rule.get("when") == "on_success"

    def test_mr_rule_runs_on_success(self, ci_config):
        rules = ci_config["mesh-sync"]["rules"]
        mr_rule = next(
            (r for r in rules if r.get("if") == '$CI_PIPELINE_SOURCE == "merge_request_event"'),
            None,
        )
        assert mr_rule is not None
        assert mr_rule.get("when") == "on_success"

    def test_exactly_two_rules(self, ci_config):
        rules = ci_config["mesh-sync"]["rules"]
        assert len(rules) == 2, f"Expected 2 rules, got {len(rules)}"


# ---------------------------------------------------------------------------
# No unexpected top-level keys
# ---------------------------------------------------------------------------

class TestCINoUnexpectedJobs:
    def test_only_one_job_defined(self, ci_config):
        # Keys other than 'stages' should all be job definitions
        job_keys = [k for k in ci_config if k != "stages"]
        assert job_keys == ["mesh-sync"], (
            f"Unexpected top-level keys: {job_keys}"
        )