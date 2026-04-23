"""Tests for infrastructure/docs/axis-llm-preset.yaml.

Covers: schema structure, model catalog integrity, routing consistency,
endpoint configuration, policy fields, and cross-reference validation.
"""

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
PRESET_PATH = REPO_ROOT / "infrastructure" / "docs" / "axis-llm-preset.yaml"

REQUIRED_CAPABILITIES = {"coder", "reasoning", "tool_use", "math", "general_ptbr", "fast_cheap"}
REQUIRED_MODEL_FIELDS = {
    "id", "family", "arch", "active_params", "total_params",
    "quant", "size_gb", "license", "license_commercial_ok",
    "strengths", "max_ctx_native",
}
VALID_ARCHES = {"dense", "moe"}
VALID_QUANT_PATTERN = re.compile(r"^Q\d|^MXFP|^FP|^BF|^INT")


@pytest.fixture(scope="module")
def preset():
    with open(PRESET_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def model_ids(preset):
    return {m["id"] for m in preset["models"]}


# ---------------------------------------------------------------------------
# Top-level schema
# ---------------------------------------------------------------------------

class TestTopLevelSchema:
    def test_file_is_parseable(self):
        with open(PRESET_PATH) as f:
            data = yaml.safe_load(f)
        assert data is not None

    def test_version_is_1(self, preset):
        assert preset["version"] == 1

    def test_generated_at_is_present(self, preset):
        assert "generated_at" in preset
        assert preset["generated_at"]

    def test_source_of_truth_is_present(self, preset):
        assert "source_of_truth" in preset
        assert preset["source_of_truth"]

    def test_top_level_sections_exist(self, preset):
        for section in ("endpoints", "server_defaults", "models", "routing", "policy"):
            assert section in preset, f"Missing top-level section: {section}"


# ---------------------------------------------------------------------------
# Endpoint configuration
# ---------------------------------------------------------------------------

class TestEndpoints:
    def test_primary_endpoint_exists(self, preset):
        assert "primary" in preset["endpoints"]

    def test_fallback_endpoint_exists(self, preset):
        assert "fallback" in preset["endpoints"]

    def test_primary_has_required_fields(self, preset):
        primary = preset["endpoints"]["primary"]
        for field in ("name", "base_url", "openai_compat_url", "transport", "health_check"):
            assert field in primary, f"primary endpoint missing field: {field}"

    def test_fallback_has_required_fields(self, preset):
        fallback = preset["endpoints"]["fallback"]
        for field in ("name", "base_url", "openai_compat_url", "transport", "health_check", "condition"):
            assert field in fallback, f"fallback endpoint missing field: {field}"

    def test_primary_health_check_fields(self, preset):
        hc = preset["endpoints"]["primary"]["health_check"]
        assert "path" in hc
        assert "timeout_ms" in hc
        assert "expect_status" in hc

    def test_fallback_health_check_fields(self, preset):
        hc = preset["endpoints"]["fallback"]["health_check"]
        assert "path" in hc
        assert "timeout_ms" in hc
        assert "expect_status" in hc

    def test_primary_transport_is_tailscale(self, preset):
        assert preset["endpoints"]["primary"]["transport"] == "tailscale"

    def test_fallback_transport_is_public(self, preset):
        assert preset["endpoints"]["fallback"]["transport"] == "public"

    def test_health_check_timeout_is_positive(self, preset):
        for ep in ("primary", "fallback"):
            timeout = preset["endpoints"][ep]["health_check"]["timeout_ms"]
            assert isinstance(timeout, int) and timeout > 0

    def test_health_check_expect_status_200(self, preset):
        for ep in ("primary", "fallback"):
            status = preset["endpoints"][ep]["health_check"]["expect_status"]
            assert status == 200

    def test_openai_compat_url_ends_with_v1(self, preset):
        for ep in ("primary", "fallback"):
            url = preset["endpoints"][ep]["openai_compat_url"]
            assert url.endswith("/v1"), f"openai_compat_url for {ep} should end with /v1"


# ---------------------------------------------------------------------------
# Server defaults
# ---------------------------------------------------------------------------

class TestServerDefaults:
    def test_num_ctx_is_positive_int(self, preset):
        val = preset["server_defaults"]["num_ctx"]
        assert isinstance(val, int) and val > 0

    def test_keep_alive_is_string(self, preset):
        assert isinstance(preset["server_defaults"]["keep_alive"], str)

    def test_num_parallel_is_positive_int(self, preset):
        val = preset["server_defaults"]["num_parallel"]
        assert isinstance(val, int) and val > 0

    def test_num_threads_is_positive_int(self, preset):
        val = preset["server_defaults"]["num_threads"]
        assert isinstance(val, int) and val > 0

    def test_flash_attention_is_bool(self, preset):
        assert isinstance(preset["server_defaults"]["flash_attention"], bool)

    def test_max_loaded_models_is_positive_int(self, preset):
        val = preset["server_defaults"]["max_loaded_models"]
        assert isinstance(val, int) and val > 0


# ---------------------------------------------------------------------------
# Model catalog
# ---------------------------------------------------------------------------

class TestModelCatalog:
    def test_models_list_is_not_empty(self, preset):
        assert len(preset["models"]) > 0

    @pytest.mark.parametrize("field", sorted(REQUIRED_MODEL_FIELDS))
    def test_all_models_have_field(self, preset, field):
        for model in preset["models"]:
            assert field in model, f"Model {model.get('id', '?')} missing field: {field}"

    def test_model_ids_are_unique(self, preset):
        ids = [m["id"] for m in preset["models"]]
        assert len(ids) == len(set(ids)), "Duplicate model IDs found"

    def test_model_ids_are_non_empty_strings(self, preset):
        for model in preset["models"]:
            assert isinstance(model["id"], str) and model["id"].strip()

    def test_model_arch_is_valid(self, preset):
        for model in preset["models"]:
            assert model["arch"] in VALID_ARCHES, (
                f"Model {model['id']} has unknown arch: {model['arch']}"
            )

    def test_model_strengths_is_list(self, preset):
        for model in preset["models"]:
            assert isinstance(model["strengths"], list), (
                f"Model {model['id']} strengths should be a list"
            )

    def test_model_strengths_not_empty(self, preset):
        for model in preset["models"]:
            assert len(model["strengths"]) > 0, (
                f"Model {model['id']} has empty strengths"
            )

    def test_model_size_gb_is_positive(self, preset):
        for model in preset["models"]:
            assert isinstance(model["size_gb"], (int, float)) and model["size_gb"] > 0, (
                f"Model {model['id']} has invalid size_gb"
            )

    def test_model_max_ctx_native_is_positive(self, preset):
        for model in preset["models"]:
            assert isinstance(model["max_ctx_native"], int) and model["max_ctx_native"] > 0, (
                f"Model {model['id']} has invalid max_ctx_native"
            )

    def test_model_license_commercial_ok_is_valid(self, preset):
        valid_values = {True, False, "review_first"}
        for model in preset["models"]:
            assert model["license_commercial_ok"] in valid_values, (
                f"Model {model['id']} has unexpected license_commercial_ok: "
                f"{model['license_commercial_ok']}"
            )

    def test_expected_model_ids_present(self, model_ids):
        expected = {
            "qwen3-coder:30b",
            "gpt-oss:20b",
            "phi4:14b",
            "qwen2.5:32b-instruct-q4_K_M",
            "qwen2.5-coder:14b",
            "qwen2.5-coder:7b",
            "deepseek-coder-v2:16b",
            "gemma4:26b",
            "gemma4:e4b",
        }
        for mid in expected:
            assert mid in model_ids, f"Expected model ID not found: {mid}"

    def test_moe_models_active_params_less_than_total(self, preset):
        for model in preset["models"]:
            if model["arch"] == "moe":
                active = model["active_params"]
                total = model["total_params"]
                # Strip trailing 'B' and compare numerically when possible
                def parse_b(val):
                    if isinstance(val, str):
                        return float(val.rstrip("B"))
                    return float(val)
                assert parse_b(active) < parse_b(total), (
                    f"MoE model {model['id']}: active_params should be < total_params"
                )


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

class TestRouting:
    def test_all_required_capabilities_present(self, preset):
        routing = preset["routing"]
        for cap in REQUIRED_CAPABILITIES:
            assert cap in routing, f"Missing routing capability: {cap}"

    def test_routing_primary_references_valid_model(self, preset, model_ids):
        for cap, config in preset["routing"].items():
            primary = config["primary"]
            assert primary in model_ids, (
                f"Routing '{cap}' primary '{primary}' not in model catalog"
            )

    def test_routing_fallback_chain_references_valid_models(self, preset, model_ids):
        for cap, config in preset["routing"].items():
            for fallback in config.get("fallback_chain", []):
                assert fallback in model_ids, (
                    f"Routing '{cap}' fallback_chain entry '{fallback}' not in model catalog"
                )

    def test_routing_each_cap_has_reason(self, preset):
        for cap, config in preset["routing"].items():
            assert "reason" in config and config["reason"], (
                f"Routing '{cap}' missing reason"
            )

    def test_routing_fallback_chain_is_list(self, preset):
        for cap, config in preset["routing"].items():
            assert isinstance(config.get("fallback_chain", []), list), (
                f"Routing '{cap}' fallback_chain must be a list"
            )

    def test_routing_primary_not_in_own_fallback_chain(self, preset):
        for cap, config in preset["routing"].items():
            primary = config["primary"]
            fallback_chain = config.get("fallback_chain", [])
            assert primary not in fallback_chain, (
                f"Routing '{cap}' primary model appears in its own fallback_chain"
            )

    def test_coder_primary_is_qwen3(self, preset):
        assert preset["routing"]["coder"]["primary"] == "qwen3-coder:30b"

    def test_fast_cheap_primary_is_qwen25_7b(self, preset):
        assert preset["routing"]["fast_cheap"]["primary"] == "qwen2.5-coder:7b"


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------

class TestPolicy:
    def test_policy_sections_present(self, preset):
        for section in ("license_guard", "circuit_breaker", "retry", "model_load"):
            assert section in preset["policy"], f"Missing policy section: {section}"

    def test_license_guard_production_is_list(self, preset):
        production = preset["policy"]["license_guard"]["production"]
        assert isinstance(production, list) and len(production) > 0

    def test_license_guard_production_contains_apache_and_mit(self, preset):
        production = preset["policy"]["license_guard"]["production"]
        assert "apache-2.0" in production
        assert "mit" in production

    def test_circuit_breaker_fail_fast_is_bool(self, preset):
        val = preset["policy"]["circuit_breaker"]["fail_fast_on_health_check"]
        assert isinstance(val, bool)

    def test_circuit_breaker_pre_flight_required_is_bool(self, preset):
        val = preset["policy"]["circuit_breaker"]["pre_flight_required"]
        assert isinstance(val, bool)

    def test_retry_max_attempts_positive(self, preset):
        val = preset["policy"]["retry"]["max_attempts"]
        assert isinstance(val, int) and val > 0

    def test_retry_backoff_ms_is_list_of_ints(self, preset):
        backoff = preset["policy"]["retry"]["backoff_ms"]
        assert isinstance(backoff, list) and len(backoff) > 0
        for b in backoff:
            assert isinstance(b, int) and b > 0

    def test_retry_backoff_ms_is_ascending(self, preset):
        backoff = preset["policy"]["retry"]["backoff_ms"]
        assert backoff == sorted(backoff), "backoff_ms should be in ascending order"

    def test_block_list_reasons_present(self, preset):
        reasons = preset["policy"]["license_guard"].get("block_list_reasons", [])
        assert isinstance(reasons, list) and len(reasons) > 0


# ---------------------------------------------------------------------------
# Examples section
# ---------------------------------------------------------------------------

class TestExamples:
    def test_examples_section_present(self, preset):
        assert "examples" in preset

    def test_curl_example_present(self, preset):
        assert "curl_openai_compat" in preset["examples"]

    def test_node_sdk_example_present(self, preset):
        assert "node_openai_sdk" in preset["examples"]

    def test_python_sdk_example_present(self, preset):
        assert "python_openai_sdk" in preset["examples"]

    def test_curl_example_references_valid_model(self, preset, model_ids):
        curl = preset["examples"]["curl_openai_compat"]
        found = any(mid in curl for mid in model_ids)
        assert found, "curl example does not reference any known model ID"