"""Tests for automation/n8n-workflows/*.json (all files changed in this PR).

Covers: JSON validity, required top-level fields, node structure,
connection graph integrity, webhook paths, and node ID uniqueness.
"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = REPO_ROOT / "automation" / "n8n-workflows"

# All changed workflow files
CHANGED_WORKFLOWS = [
    "ai-guardian-cleanup.json",
    "ai-lead-hunter.json",
    "gitlab-ci-pipeline.json",
    "gitlab-merge-sync.json",
    "gitlab-tag-version.json",
    "infrastructure-monitor.json",
]

REQUIRED_NODE_FIELDS = {"name", "type", "typeVersion", "position"}

# Node types that must carry a unique id
ID_BEARING_TYPES = {
    "n8n-nodes-base.webhook",
    "n8n-nodes-base.code",
    "n8n-nodes-base.if",
    "n8n-nodes-base.switch",
    "n8n-nodes-base.httpRequest",
    "n8n-nodes-base.scheduleTrigger",
    "n8n-nodes-base.emailSend",
    "n8n-nodes-base.executeCommand",
    "n8n-nodes-base.splitInBatches",
}


def load_workflow(filename: str) -> dict:
    path = WORKFLOWS_DIR / filename
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Parametrize all workflows for structure tests
# ---------------------------------------------------------------------------

@pytest.fixture(params=CHANGED_WORKFLOWS)
def workflow(request):
    return load_workflow(request.param)


@pytest.fixture(params=CHANGED_WORKFLOWS)
def workflow_with_name(request):
    return request.param, load_workflow(request.param)


# ---------------------------------------------------------------------------
# JSON validity — individual files
# ---------------------------------------------------------------------------

class TestJsonValidity:
    @pytest.mark.parametrize("filename", CHANGED_WORKFLOWS)
    def test_file_is_valid_json(self, filename):
        path = WORKFLOWS_DIR / filename
        assert path.exists(), f"Workflow file not found: {filename}"
        with open(path) as f:
            data = json.load(f)
        assert data is not None

    @pytest.mark.parametrize("filename", CHANGED_WORKFLOWS)
    def test_file_is_dict(self, filename):
        data = load_workflow(filename)
        assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# Required top-level fields
# ---------------------------------------------------------------------------

class TestTopLevelFields:
    def test_has_name(self, workflow):
        assert "name" in workflow
        assert isinstance(workflow["name"], str) and workflow["name"].strip()

    def test_has_nodes(self, workflow):
        assert "nodes" in workflow
        assert isinstance(workflow["nodes"], list)

    def test_has_connections(self, workflow):
        assert "connections" in workflow
        assert isinstance(workflow["connections"], dict)

    def test_nodes_not_empty(self, workflow):
        assert len(workflow["nodes"]) > 0


# ---------------------------------------------------------------------------
# Node structure
# ---------------------------------------------------------------------------

class TestNodeStructure:
    def test_each_node_has_required_fields(self, workflow):
        for node in workflow["nodes"]:
            for field in REQUIRED_NODE_FIELDS:
                assert field in node, (
                    f"Node in '{workflow['name']}' missing field '{field}': {node}"
                )

    def test_node_position_is_list_of_two_numbers(self, workflow):
        for node in workflow["nodes"]:
            pos = node["position"]
            assert isinstance(pos, list) and len(pos) == 2, (
                f"Node '{node.get('name')}' position must be [x, y]"
            )
            for coord in pos:
                assert isinstance(coord, (int, float)), (
                    f"Node '{node.get('name')}' position coords must be numeric"
                )

    def test_node_type_is_string(self, workflow):
        for node in workflow["nodes"]:
            assert isinstance(node["type"], str) and node["type"].strip()

    def test_node_type_version_is_number(self, workflow):
        for node in workflow["nodes"]:
            assert isinstance(node["typeVersion"], (int, float)) and node["typeVersion"] > 0

    def test_node_names_unique_within_workflow(self, workflow):
        names = [n["name"] for n in workflow["nodes"]]
        assert len(names) == len(set(names)), (
            f"Duplicate node names in '{workflow['name']}': "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    def test_node_ids_unique_when_present(self, workflow):
        ids = [n["id"] for n in workflow["nodes"] if "id" in n]
        assert len(ids) == len(set(ids)), (
            f"Duplicate node IDs in '{workflow['name']}': "
            f"{[i for i in ids if ids.count(i) > 1]}"
        )


# ---------------------------------------------------------------------------
# Connection graph integrity
# ---------------------------------------------------------------------------

class TestConnectionGraph:
    def test_connection_sources_reference_existing_nodes(self, workflow):
        node_names = {n["name"] for n in workflow["nodes"]}
        for source_name in workflow["connections"]:
            assert source_name in node_names, (
                f"Connection source '{source_name}' in '{workflow['name']}' "
                f"does not match any node name"
            )

    def test_connection_targets_reference_existing_nodes(self, workflow):
        node_names = {n["name"] for n in workflow["nodes"]}
        for source_name, outputs in workflow["connections"].items():
            main_outputs = outputs.get("main", [])
            for output_group in main_outputs:
                for edge in output_group:
                    target = edge.get("node")
                    assert target in node_names, (
                        f"Connection target '{target}' from '{source_name}' "
                        f"in '{workflow['name']}' does not match any node name"
                    )

    def test_connection_edge_has_required_fields(self, workflow):
        for source_name, outputs in workflow["connections"].items():
            main_outputs = outputs.get("main", [])
            for output_group in main_outputs:
                for edge in output_group:
                    assert "node" in edge, (
                        f"Edge from '{source_name}' in '{workflow['name']}' missing 'node'"
                    )
                    assert "type" in edge, (
                        f"Edge from '{source_name}' in '{workflow['name']}' missing 'type'"
                    )
                    assert "index" in edge, (
                        f"Edge from '{source_name}' in '{workflow['name']}' missing 'index'"
                    )


# ---------------------------------------------------------------------------
# Workflow-specific: GitLab CI Pipeline
# ---------------------------------------------------------------------------

class TestGitLabCIPipelineWorkflow:
    @pytest.fixture
    def pipeline_wf(self):
        return load_workflow("gitlab-ci-pipeline.json")

    def test_workflow_name_contains_pipeline(self, pipeline_wf):
        assert "Pipeline" in pipeline_wf["name"] or "pipeline" in pipeline_wf["name"].lower()

    def test_has_webhook_node(self, pipeline_wf):
        node_types = [n["type"] for n in pipeline_wf["nodes"]]
        assert "n8n-nodes-base.webhook" in node_types

    def test_webhook_path_is_gitlab_ci_pipeline(self, pipeline_wf):
        webhook = next(
            n for n in pipeline_wf["nodes"] if n["type"] == "n8n-nodes-base.webhook"
        )
        assert webhook["parameters"]["path"] == "gitlab-ci-pipeline"

    def test_has_validate_and_parse_node(self, pipeline_wf):
        node_names = {n["name"] for n in pipeline_wf["nodes"]}
        assert "Validate & Parse" in node_names

    def test_has_route_by_status_switch(self, pipeline_wf):
        node_names = {n["name"] for n in pipeline_wf["nodes"]}
        assert "Route by Status" in node_names

    def test_validate_parse_code_checks_token(self, pipeline_wf):
        validate_node = next(
            n for n in pipeline_wf["nodes"] if n["name"] == "Validate & Parse"
        )
        code = validate_node["parameters"]["jsCode"]
        assert "GITLAB_WEBHOOK_SECRET" in code
        assert "x-gitlab-token" in code.lower() or "x-gitlab-token" in code

    def test_validate_parse_code_checks_pipeline_hook_event(self, pipeline_wf):
        validate_node = next(
            n for n in pipeline_wf["nodes"] if n["name"] == "Validate & Parse"
        )
        code = validate_node["parameters"]["jsCode"]
        assert "Pipeline Hook" in code

    def test_has_build_rollback_info_node(self, pipeline_wf):
        node_names = {n["name"] for n in pipeline_wf["nodes"]}
        assert "Build Rollback Info" in node_names

    def test_rollback_node_code_contains_revert_command(self, pipeline_wf):
        rollback_node = next(
            n for n in pipeline_wf["nodes"] if n["name"] == "Build Rollback Info"
        )
        code = rollback_node["parameters"]["jsCode"]
        assert "git revert" in code

    def test_calver_prep_node_exists(self, pipeline_wf):
        node_names = {n["name"] for n in pipeline_wf["nodes"]}
        assert "Prepare CalVer Prefix" in node_names

    def test_duration_formatting_in_validate_node(self, pipeline_wf):
        validate_node = next(
            n for n in pipeline_wf["nodes"] if n["name"] == "Validate & Parse"
        )
        code = validate_node["parameters"]["jsCode"]
        # Duration formatting logic must handle both <60s and >60s cases
        assert "durationSec" in code
        assert "60" in code

    def test_route_by_status_has_success_failed_running(self, pipeline_wf):
        switch_node = next(
            n for n in pipeline_wf["nodes"] if n["name"] == "Route by Status"
        )
        rules = switch_node["parameters"]["rules"]["values"]
        output_keys = {r["outputKey"] for r in rules}
        assert "Success" in output_keys
        assert "Failed" in output_keys
        assert "Running" in output_keys

    def test_settings_timezone_is_sao_paulo(self, pipeline_wf):
        assert pipeline_wf["settings"]["timezone"] == "America/Sao_Paulo"

    def test_is_not_active_by_default(self, pipeline_wf):
        assert pipeline_wf["active"] is False


# ---------------------------------------------------------------------------
# Workflow-specific: GitLab Merge Sync
# ---------------------------------------------------------------------------

class TestGitLabMergeSyncWorkflow:
    @pytest.fixture
    def merge_sync_wf(self):
        return load_workflow("gitlab-merge-sync.json")

    def test_workflow_name_contains_merge_sync(self, merge_sync_wf):
        assert "Merge" in merge_sync_wf["name"] or "merge" in merge_sync_wf["name"].lower()

    def test_webhook_path_is_gitlab_merge_sync(self, merge_sync_wf):
        webhook = next(
            n for n in merge_sync_wf["nodes"] if n["type"] == "n8n-nodes-base.webhook"
        )
        assert webhook["parameters"]["path"] == "gitlab-merge-sync"

    def test_has_protected_branch_check(self, merge_sync_wf):
        node_names = {n["name"] for n in merge_sync_wf["nodes"]}
        assert "Is Protected Branch?" in node_names

    def test_protected_branch_node_covers_main_develop_staging(self, merge_sync_wf):
        branch_node = next(
            n for n in merge_sync_wf["nodes"] if n["name"] == "Is Protected Branch?"
        )
        conditions = branch_node["parameters"]["conditions"]["conditions"]
        branches_covered = {c["rightValue"] for c in conditions}
        assert "main" in branches_covered
        assert "develop" in branches_covered
        assert "staging" in branches_covered

    def test_validate_node_checks_merged_state(self, merge_sync_wf):
        validate_node = next(
            n for n in merge_sync_wf["nodes"] if n["name"] == "Validate & Extract"
        )
        code = validate_node["parameters"]["jsCode"]
        assert "merged" in code

    def test_has_build_sync_command_node(self, merge_sync_wf):
        node_names = {n["name"] for n in merge_sync_wf["nodes"]}
        assert "Build Sync Command" in node_names

    def test_sync_command_node_uses_git_push(self, merge_sync_wf):
        sync_node = next(
            n for n in merge_sync_wf["nodes"] if n["name"] == "Build Sync Command"
        )
        code = sync_node["parameters"]["jsCode"]
        assert "git push github" in code

    def test_is_not_active_by_default(self, merge_sync_wf):
        assert merge_sync_wf["active"] is False


# ---------------------------------------------------------------------------
# Workflow-specific: GitLab Tag & Version
# ---------------------------------------------------------------------------

class TestGitLabTagVersionWorkflow:
    @pytest.fixture
    def tag_wf(self):
        return load_workflow("gitlab-tag-version.json")

    def test_webhook_path_is_gitlab_tag_version(self, tag_wf):
        webhook = next(
            n for n in tag_wf["nodes"] if n["type"] == "n8n-nodes-base.webhook"
        )
        assert webhook["parameters"]["path"] == "gitlab-tag-version"

    def test_validate_node_checks_merge_request_hook(self, tag_wf):
        validate_node = next(
            n for n in tag_wf["nodes"] if n["name"] == "Validate MR to Main"
        )
        code = validate_node["parameters"]["jsCode"]
        assert "Merge Request Hook" in code

    def test_validate_node_requires_target_branch_main(self, tag_wf):
        validate_node = next(
            n for n in tag_wf["nodes"] if n["name"] == "Validate MR to Main"
        )
        code = validate_node["parameters"]["jsCode"]
        assert "target_branch" in code
        assert "'main'" in code

    def test_has_calculate_calver_node(self, tag_wf):
        node_names = {n["name"] for n in tag_wf["nodes"]}
        assert "Calculate CalVer" in node_names

    def test_has_create_gitlab_tag_node(self, tag_wf):
        node_names = {n["name"] for n in tag_wf["nodes"]}
        assert "Create GitLab Tag" in node_names

    def test_has_create_github_tag_node(self, tag_wf):
        node_names = {n["name"] for n in tag_wf["nodes"]}
        assert "Create GitHub Tag Ref" in node_names

    def test_has_create_gitlab_release_node(self, tag_wf):
        node_names = {n["name"] for n in tag_wf["nodes"]}
        assert "Create GitLab Release" in node_names

    def test_calver_code_uses_date_prefix_format(self, tag_wf):
        calver_node = next(
            n for n in tag_wf["nodes"] if n["name"] == "Calculate CalVer"
        )
        code = calver_node["parameters"]["jsCode"]
        assert "datePrefix" in code
        assert "YYYY" in code or "yyyy" in code.lower() or "getFullYear" in code

    def test_is_not_active_by_default(self, tag_wf):
        assert tag_wf["active"] is False


# ---------------------------------------------------------------------------
# Workflow-specific: Infrastructure Monitor
# ---------------------------------------------------------------------------

class TestInfrastructureMonitorWorkflow:
    @pytest.fixture
    def monitor_wf(self):
        return load_workflow("infrastructure-monitor.json")

    def test_workflow_is_active(self, monitor_wf):
        # This workflow is a health monitor and should be active
        assert monitor_wf["active"] is True

    def test_has_schedule_trigger(self, monitor_wf):
        node_types = [n["type"] for n in monitor_wf["nodes"]]
        assert "n8n-nodes-base.scheduleTrigger" in node_types

    def test_schedule_is_5_minutes(self, monitor_wf):
        sched_node = next(
            n for n in monitor_wf["nodes"] if n["type"] == "n8n-nodes-base.scheduleTrigger"
        )
        # Verify the interval configuration
        params = sched_node["parameters"]
        rule = params.get("rule", {})
        intervals = rule.get("interval", [])
        assert any(
            i.get("field") == "minutes" and i.get("minutesInterval") == 5
            for i in intervals
        ), "Schedule trigger should run every 5 minutes"

    def test_monitors_three_services(self, monitor_wf):
        define_node = next(
            (n for n in monitor_wf["nodes"] if n["name"] == "Define Services"),
            None,
        )
        assert define_node is not None
        code = define_node["parameters"]["jsCode"]
        assert "jpglabs.com.br" in code
        assert "n8n.jpglabs.com.br" in code
        assert "chat.jpglabs.com.br" in code

    def test_has_slack_alert_node(self, monitor_wf):
        node_names = {n["name"] for n in monitor_wf["nodes"]}
        assert "Slack Alert" in node_names

    def test_has_slack_recovery_node(self, monitor_wf):
        node_names = {n["name"] for n in monitor_wf["nodes"]}
        assert "Slack Recovery" in node_names

    def test_track_consecutive_failures_node_present(self, monitor_wf):
        node_names = {n["name"] for n in monitor_wf["nodes"]}
        assert "Track Consecutive Failures" in node_names

    def test_consecutive_failure_threshold_is_2(self, monitor_wf):
        track_node = next(
            n for n in monitor_wf["nodes"] if n["name"] == "Track Consecutive Failures"
        )
        code = track_node["parameters"]["jsCode"]
        # The threshold for alerting must be >= 2
        assert ">= 2" in code or ">=2" in code


# ---------------------------------------------------------------------------
# Workflow-specific: AI Guardian Cleanup
# ---------------------------------------------------------------------------

class TestAIGuardianCleanupWorkflow:
    @pytest.fixture
    def guardian_wf(self):
        return load_workflow("ai-guardian-cleanup.json")

    def test_has_schedule_trigger(self, guardian_wf):
        node_types = [n["type"] for n in guardian_wf["nodes"]]
        assert "n8n-nodes-base.scheduleTrigger" in node_types

    def test_schedule_is_cron(self, guardian_wf):
        sched_node = next(
            n for n in guardian_wf["nodes"] if n["type"] == "n8n-nodes-base.scheduleTrigger"
        )
        # Old-style scheduleTrigger uses a `rule` string (cron) or object
        rule = sched_node["parameters"].get("rule", "")
        assert rule, "Schedule trigger must have a rule"

    def test_has_disk_cleanup_node(self, guardian_wf):
        node_names = {n["name"] for n in guardian_wf["nodes"]}
        assert "Disk Cleanup" in node_names

    def test_disk_cleanup_uses_docker_prune(self, guardian_wf):
        cleanup_node = next(
            n for n in guardian_wf["nodes"] if n["name"] == "Disk Cleanup"
        )
        command = cleanup_node["parameters"]["command"]
        assert "docker system prune" in command

    def test_disk_cleanup_removes_tmp(self, guardian_wf):
        cleanup_node = next(
            n for n in guardian_wf["nodes"] if n["name"] == "Disk Cleanup"
        )
        command = cleanup_node["parameters"]["command"]
        assert "/tmp/*" in command

    def test_cleanup_triggers_notification(self, guardian_wf):
        # Schedule -> Cleanup -> Notification chain must exist
        assert "Disk Cleanup" in guardian_wf["connections"]

    def test_has_success_notification(self, guardian_wf):
        node_names = {n["name"] for n in guardian_wf["nodes"]}
        assert "Success Notification" in node_names


# ---------------------------------------------------------------------------
# Workflow-specific: AI Lead Hunter
# ---------------------------------------------------------------------------

class TestAILeadHunterWorkflow:
    @pytest.fixture
    def lead_wf(self):
        return load_workflow("ai-lead-hunter.json")

    def test_has_schedule_trigger(self, lead_wf):
        node_types = [n["type"] for n in lead_wf["nodes"]]
        assert "n8n-nodes-base.scheduleTrigger" in node_types

    def test_schedule_is_every_hour(self, lead_wf):
        sched_node = next(
            n for n in lead_wf["nodes"] if n["type"] == "n8n-nodes-base.scheduleTrigger"
        )
        rule = sched_node["parameters"].get("rule", {})
        intervals = rule.get("interval", [])
        assert any(
            i.get("field") == "hours" and i.get("hoursInterval") == 1
            for i in intervals
        ), "Schedule should run every hour"

    def test_has_scrape_reddit_node(self, lead_wf):
        node_names = {n["name"] for n in lead_wf["nodes"]}
        assert "Scrape Reddit" in node_names

    def test_has_filter_keywords_node(self, lead_wf):
        node_names = {n["name"] for n in lead_wf["nodes"]}
        assert "Filter Keywords" in node_names

    def test_has_notify_slack_node(self, lead_wf):
        node_names = {n["name"] for n in lead_wf["nodes"]}
        assert "Notify Slack" in node_names

    def test_format_posts_extracts_title_url_author(self, lead_wf):
        format_node = next(
            n for n in lead_wf["nodes"] if n["name"] == "Format Posts"
        )
        code = format_node["parameters"]["jsCode"]
        assert "title" in code
        assert "url" in code
        assert "author" in code

    def test_log_to_diary_node_present(self, lead_wf):
        node_names = {n["name"] for n in lead_wf["nodes"]}
        assert "Log to Diary" in node_names

    def test_log_to_diary_writes_markdown(self, lead_wf):
        log_node = next(n for n in lead_wf["nodes"] if n["name"] == "Log to Diary")
        code = log_node["parameters"]["jsCode"]
        assert ".md" in code