.PHONY: inventory check-artifact-law render-adapters validate-constitution validate-metadata-naming validate-tributary-disposition check-office-harness-coherence bootstrap-office migrate-communications-chain archive-shell-manifest rehouse-archived-artifact sync-reference-tree stage-feedstock operator-tree harness-tranche-ab harness-registry-effective harness-promoted-atoms-smoke office-watch-once dispatch-office-task manus-create manus-wait bootstrap-mini revive-mini-constellation constellation-mini-status install-mini-constellation-launchagent tooling-surface-status mini-constellation-collect-status acumen-init-registry acumen-validate-registry acumen-identity-probe acumen-poll-youtube acumen-build-triage-packet acumen-run-gemini-triage acumen-run-triage acumen-deterministic-track acumen-build-dawn-brief acumen-build-verified-signal-brief acumen-build-primary-source-queue-readout acumen-build-intelligence-product-family acumen-pipeline-run acumen-record-triage-decision acumen-record-model-call acumen-rematerialize-evidence acumen-validate-evidence acumen-build-verification-bridge acumen-validate-verification-bridge acumen-validate-live-batch-proof acumen-preflight acumen-sample-run acumen-live-batch exocortex-sync-surface-registry exocortex-import-connector-guide exocortex-audit-control-plane exocortex-sync-connector-manifest exocortex-apply-connector-receipts exocortex-connector-verification-run exocortex-control-plane-run ajna-exocortex-access-program ajna-auth-wave-packet ontology-project-repo webshell-dev webshell-smoke webshell-callback-smoke webshell-generate-token webshell-keychain-status webshell-keychain-init-callback webshell-launchagent-install webshell-launchagent-status webshell-launchagent-restart

inventory:
	python3 operators/validators/artifact_law_inventory.py --format both

check-artifact-law:
	python3 operators/validators/artifact_law_inventory.py --format both --check

render-adapters:
	python3 operators/config/render_successor_adapters.py

validate-constitution:
	python3 operators/validators/validate_constitution.py
	python3 operators/config/render_successor_adapters.py --check

validate-metadata-naming:
	python3 operators/validators/validate_metadata_naming.py $(if $(filter 1 true yes,$(STRICT)),--strict,)

validate-tributary-disposition:
	python3 operators/validators/validate_tributary_disposition.py

check-office-harness-coherence:
	python3 operators/validators/validate_office_harness_coherence.py $(if $(filter 1 true yes,$(STRICT)),--strict,)

bootstrap-office:
	@test -n "$(NAME)" || (echo "usage: make bootstrap-office NAME=office-name" && exit 1)
	python3 operators/bootstrap_office.py "$(NAME)"

migrate-communications-chain:
	@test -n "$(PROMPT)" || (echo "usage: make migrate-communications-chain PROMPT=/abs/path/prompt.md RESPONSE=/abs/path/response.md ASSESSMENT=/abs/path/assessment.md [SURFACE=oracle]" && exit 1)
	@test -n "$(RESPONSE)" || (echo "usage: make migrate-communications-chain PROMPT=/abs/path/prompt.md RESPONSE=/abs/path/response.md ASSESSMENT=/abs/path/assessment.md [SURFACE=oracle]" && exit 1)
	@test -n "$(ASSESSMENT)" || (echo "usage: make migrate-communications-chain PROMPT=/abs/path/prompt.md RESPONSE=/abs/path/response.md ASSESSMENT=/abs/path/assessment.md [SURFACE=oracle]" && exit 1)
	python3 operators/migrate_communications_chain.py --prompt "$(PROMPT)" --response "$(RESPONSE)" --assessment "$(ASSESSMENT)" --surface "$(or $(SURFACE),generic)"

operator-tree:
	@find operators -maxdepth 2 -type f | sort

archive-shell-manifest:
	@test -n "$(ROOT)" || (echo "usage: make archive-shell-manifest ROOT=/abs/path LABEL=name" && exit 1)
	@test -n "$(LABEL)" || (echo "usage: make archive-shell-manifest ROOT=/abs/path LABEL=name" && exit 1)
	python3 operators/migrate/archive_shell_manifest.py --root "$(ROOT)" --label "$(LABEL)"

rehouse-archived-artifact:
	@test -n "$(SOURCE)" || (echo "usage: make rehouse-archived-artifact SOURCE=/abs/path DEST_REL=pedigree/rehoused/foo.md LABEL=slug REASON='why'" && exit 1)
	@test -n "$(DEST_REL)" || (echo "usage: make rehouse-archived-artifact SOURCE=/abs/path DEST_REL=pedigree/rehoused/foo.md LABEL=slug REASON='why'" && exit 1)
	@test -n "$(LABEL)" || (echo "usage: make rehouse-archived-artifact SOURCE=/abs/path DEST_REL=pedigree/rehoused/foo.md LABEL=slug REASON='why'" && exit 1)
	@test -n "$(REASON)" || (echo "usage: make rehouse-archived-artifact SOURCE=/abs/path DEST_REL=pedigree/rehoused/foo.md LABEL=slug REASON='why'" && exit 1)
	python3 operators/migrate/rehouse_archived_artifact.py --source "$(SOURCE)" --dest-rel "$(DEST_REL)" --label "$(LABEL)" --reason "$(REASON)"

sync-reference-tree:
	@test -n "$(SOURCE_ROOT)" || (echo "usage: make sync-reference-tree SOURCE_ROOT=/abs/path DEST_REL=knowledge/references/foo LABEL=slug REASON='why' [REPLACE=1]" && exit 1)
	@test -n "$(DEST_REL)" || (echo "usage: make sync-reference-tree SOURCE_ROOT=/abs/path DEST_REL=knowledge/references/foo LABEL=slug REASON='why' [REPLACE=1]" && exit 1)
	@test -n "$(LABEL)" || (echo "usage: make sync-reference-tree SOURCE_ROOT=/abs/path DEST_REL=knowledge/references/foo LABEL=slug REASON='why' [REPLACE=1]" && exit 1)
	@test -n "$(REASON)" || (echo "usage: make sync-reference-tree SOURCE_ROOT=/abs/path DEST_REL=knowledge/references/foo LABEL=slug REASON='why' [REPLACE=1]" && exit 1)
	python3 operators/migrate/sync_reference_tree.py --source-root "$(SOURCE_ROOT)" --dest-rel "$(DEST_REL)" --label "$(LABEL)" --reason "$(REASON)" $(if $(REPLACE),--replace,)

stage-feedstock:
	@test -n "$(SOURCE)" || (echo "usage: make stage-feedstock SOURCE=/abs/path/file.md LABEL=slug REASON='why'" && exit 1)
	@test -n "$(LABEL)" || (echo "usage: make stage-feedstock SOURCE=/abs/path/file.md LABEL=slug REASON='why'" && exit 1)
	@test -n "$(REASON)" || (echo "usage: make stage-feedstock SOURCE=/abs/path/file.md LABEL=slug REASON='why'" && exit 1)
	python3 operators/knowledge/stage_feedstock_artifact.py --source "$(SOURCE)" --label "$(LABEL)" --reason "$(REASON)"

harness-tranche-ab:
	python3 operators/validators/harness_tranche_ab.py --source-dir "$(or $(SOURCE_DIR),/Users/system/Desktop/harnesses)" --cc-tag "$(or $(CC_TAG),cc79)"

harness-registry-effective:
	python3 operators/validators/render_harness_effective_registry.py

harness-promoted-atoms-smoke:
	python3 operators/validators/harness_promoted_atoms_smoke.py

office-watch-once:
	@test -n "$(OFFICE)" || (echo "usage: make office-watch-once OFFICE=psyche [REPO_ROOT=/abs/path]" && exit 1)
	python3 operators/runtime/office_inbox_watch.py --office "$(OFFICE)" --repo-root "$(or $(REPO_ROOT),$(CURDIR))" --once

dispatch-office-task:
	@test -n "$(OFFICE)" || (echo "usage: make dispatch-office-task OFFICE=psyche TITLE='task title' PAYLOAD_FILE=/abs/path/payload.md" && exit 1)
	@test -n "$(TITLE)" || (echo "usage: make dispatch-office-task OFFICE=psyche TITLE='task title' PAYLOAD_FILE=/abs/path/payload.md" && exit 1)
	@test -n "$(PAYLOAD_FILE)" || (echo "usage: make dispatch-office-task OFFICE=psyche TITLE='task title' PAYLOAD_FILE=/abs/path/payload.md" && exit 1)
	python3 operators/runtime/dispatch_office_task.py --office "$(OFFICE)" --repo-root "$(or $(REPO_ROOT),$(CURDIR))" --title "$(TITLE)" --payload-file "$(PAYLOAD_FILE)" --sender "$(or $(SENDER),commander)"

manus-create:
	@test -n "$(PROMPT_FILE)" || (echo "usage: make manus-create PROMPT_FILE=communications/prompts/PACKET-....md" && exit 1)
	python3 operators/exocortex/manus_task_api.py create --prompt-file "$(PROMPT_FILE)"

manus-wait:
	@test -n "$(TASK_ID)" || (echo "usage: make manus-wait TASK_ID=taskid [EXTRACT=1] [TIMEOUT=900] [INTERVAL=15]" && exit 1)
	python3 operators/exocortex/manus_task_api.py wait --task-id "$(TASK_ID)" --timeout-seconds "$(or $(TIMEOUT),900)" --interval-seconds "$(or $(INTERVAL),15)" $(if $(EXTRACT),--extract-text,)

bootstrap-mini:
	./operators/machines/bootstrap-mac-mini.sh all

revive-mini-constellation:
	./operators/machines/revive-mini-constellation.sh

constellation-mini-status:
	./operators/machines/constellation-mini-status.sh

install-mini-constellation-launchagent:
	./operators/machines/install-mini-constellation-launchagent.sh

tooling-surface-status:
	python3 operators/runtime/collect-tooling-surface-status.py

mini-constellation-collect-status:
	python3 operators/runtime/collect-mini-constellation-status.py --host "$(or $(REMOTE_HOST),mini)"

acumen-init-registry:
	python3 operators/acumen/init_registry.py --seed "$(or $(SEED),operators/acumen/channel_seed.example.json)" --output "$(or $(OUTPUT),runtime/acumen/registry.json)" $(if $(MERGE),--merge,)

acumen-validate-registry:
	python3 operators/acumen/validate_registry.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" $(if $(filter 1 true yes,$(STRICT)),--strict,)

acumen-identity-probe:
	python3 operators/acumen/identity_binding_probe.py --binding "$(or $(BINDING),orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json)" --output "$(or $(OUTPUT),orchestration/state/ACUMEN-IDENTITY-STATUS.json)" $(if $(filter 1 true yes,$(STRICT)),--strict,)

acumen-poll-youtube:
	python3 operators/acumen/poll_youtube_registry.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --cursor "$(or $(CURSOR),runtime/acumen/poll_cursor.json)" --output-jsonl "$(or $(OUTPUT_JSONL),runtime/acumen/poll-candidates.jsonl)" --status-json "$(or $(STATUS_JSON),orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json)" --api-key-env "$(or $(API_KEY_ENV),ACUMEN_YOUTUBE_API_KEY)" --max-results-per-channel "$(or $(MAX_RESULTS),10)" --overlap-seconds "$(or $(OVERLAP_SECONDS),120)" --timeout-seconds "$(or $(TIMEOUT_SECONDS),20)" $(if $(RETRY_DELAYS),--retry-delays-seconds "$(RETRY_DELAYS)",) $(foreach CHANNEL,$(CHANNEL_IDS),--channel-id "$(CHANNEL)") $(if $(filter 1 true yes,$(FORCE)),--force,) $(if $(filter 1 true yes,$(STRICT)),--strict-identity,)

acumen-build-triage-packet:
	@test -n "$(CHANNEL_ID)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.json [PROMPT_OUTPUT=/abs/path/prompt.md]" && exit 1)
	@test -n "$(VIDEO_JSON)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.json [PROMPT_OUTPUT=/abs/path/prompt.md]" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.json [PROMPT_OUTPUT=/abs/path/prompt.md]" && exit 1)
	python3 operators/acumen/build_triage_packet.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --channel-id "$(CHANNEL_ID)" --video "$(VIDEO_JSON)" --output "$(OUTPUT)" $(if $(PROMPT_OUTPUT),--prompt-output "$(PROMPT_OUTPUT)",)

acumen-run-gemini-triage:
	@test -n "$(PACKET)" || (echo "usage: make acumen-run-gemini-triage PACKET=/abs/path/triage-packet.json OUTPUT=/abs/path/triage-decision.json [QUEUE=/abs/path/triage-decisions.jsonl] [MODEL=gemini-2.5-flash]" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-run-gemini-triage PACKET=/abs/path/triage-packet.json OUTPUT=/abs/path/triage-decision.json [QUEUE=/abs/path/triage-decisions.jsonl] [MODEL=gemini-2.5-flash]" && exit 1)
	python3 operators/acumen/run_gemini_triage.py --packet "$(PACKET)" --output "$(OUTPUT)" $(if $(QUEUE),--append-jsonl "$(QUEUE)",) $(if $(MODEL),--model "$(MODEL)",) $(if $(API_BASE),--api-base "$(API_BASE)",) $(if $(API_KEY_ENV),--api-key-env "$(API_KEY_ENV)",) $(if $(TIMEOUT_SECONDS),--timeout-seconds "$(TIMEOUT_SECONDS)",) $(if $(MAX_ATTEMPTS),--max-attempts "$(MAX_ATTEMPTS)",) $(if $(RETRY_BACKOFF_SECONDS),--retry-backoff-seconds "$(RETRY_BACKOFF_SECONDS)",) $(if $(MAX_PROMPT_CHARS),--max-prompt-chars "$(MAX_PROMPT_CHARS)",) $(if $(MAX_OUTPUT_TOKENS),--max-output-tokens "$(MAX_OUTPUT_TOKENS)",) $(if $(MAX_TOTAL_TOKENS),--max-total-tokens "$(MAX_TOTAL_TOKENS)",)

acumen-run-triage:
	@test -n "$(POLL_JSONL)" || (echo "usage: make acumen-run-triage POLL_JSONL=/abs/path/poll.jsonl QUEUE=/abs/path/triage-decisions.jsonl [REGISTRY=runtime/acumen/registry.json] [TRAINING_JSONL=runtime/acumen/training-corpus.jsonl] [STATUS_JSON=runtime/acumen/triage-status.json] [ARTIFACT_DIR=runtime/acumen/out/triage] [MODE=auto|heuristic|gemini]" && exit 1)
	@test -n "$(QUEUE)" || (echo "usage: make acumen-run-triage POLL_JSONL=/abs/path/poll.jsonl QUEUE=/abs/path/triage-decisions.jsonl [REGISTRY=runtime/acumen/registry.json] [TRAINING_JSONL=runtime/acumen/training-corpus.jsonl] [STATUS_JSON=runtime/acumen/triage-status.json] [ARTIFACT_DIR=runtime/acumen/out/triage] [MODE=auto|heuristic|gemini]" && exit 1)
	python3 operators/acumen/run_triage.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --poll-jsonl "$(POLL_JSONL)" --queue-jsonl "$(QUEUE)" --training-jsonl "$(or $(TRAINING_JSONL),runtime/acumen/training-corpus.jsonl)" --status-json "$(or $(STATUS_JSON),runtime/acumen/triage-status.json)" --artifact-dir "$(or $(ARTIFACT_DIR),runtime/acumen/out/triage)" --mode "$(or $(MODE),auto)" $(if $(MODEL),--model "$(MODEL)",) $(if $(API_BASE),--api-base "$(API_BASE)",) $(if $(API_KEY_ENV),--api-key-env "$(API_KEY_ENV)",) $(if $(TIMEOUT_SECONDS),--timeout-seconds "$(TIMEOUT_SECONDS)",) $(if $(MAX_LIVE_CALLS),--max-live-calls "$(MAX_LIVE_CALLS)",) $(if $(MAX_RETRIES),--max-retries "$(MAX_RETRIES)",) $(if $(RETRY_BACKOFF_SECONDS),--retry-backoff-seconds "$(RETRY_BACKOFF_SECONDS)",) $(if $(MAX_PROMPT_CHARS),--max-prompt-chars "$(MAX_PROMPT_CHARS)",) $(if $(MAX_OUTPUT_TOKENS),--max-output-tokens "$(MAX_OUTPUT_TOKENS)",) $(if $(MAX_TOTAL_TOKENS),--max-total-tokens "$(MAX_TOTAL_TOKENS)",) $(if $(ESTIMATED_COST_PER_CALL_USD),--estimated-cost-per-call-usd "$(ESTIMATED_COST_PER_CALL_USD)",) $(if $(MAX_ESTIMATED_COST_USD),--max-estimated-cost-usd "$(MAX_ESTIMATED_COST_USD)",)

acumen-deterministic-track:
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-deterministic-track OUTPUT=/abs/path/out.md [INPUT_TEXT=/abs/path/file.txt|INPUT_CAPTIONS=/abs/path/captions.json] [GENRE=Commentary] [DEPTH=Precis] [POLISH=clean_verbatim]" && exit 1)
	@test -n "$(INPUT_TEXT)$(INPUT_CAPTIONS)" || (echo "usage: make acumen-deterministic-track OUTPUT=/abs/path/out.md [INPUT_TEXT=/abs/path/file.txt|INPUT_CAPTIONS=/abs/path/captions.json] [GENRE=Commentary] [DEPTH=Precis] [POLISH=clean_verbatim]" && exit 1)
	python3 operators/acumen/deterministic_track.py $(if $(INPUT_TEXT),--input-text "$(INPUT_TEXT)",) $(if $(INPUT_CAPTIONS),--input-captions "$(INPUT_CAPTIONS)",) --genre "$(or $(GENRE),Commentary)" --target-depth "$(or $(DEPTH),Precis)" --target-polish "$(or $(POLISH),clean_verbatim)" $(if $(RESOLUTION_JSON),--resolution-json "$(RESOLUTION_JSON)",) $(if $(DEBUG_JSON),--debug-json "$(DEBUG_JSON)",) --output "$(OUTPUT)"

acumen-build-dawn-brief:
	@test -n "$(INPUT_JSONL)" || (echo "usage: make acumen-build-dawn-brief INPUT_JSONL=/abs/path/decisions.jsonl OUTPUT=/abs/path/DAWN-BRIEF.md" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-dawn-brief INPUT_JSONL=/abs/path/decisions.jsonl OUTPUT=/abs/path/DAWN-BRIEF.md" && exit 1)
	python3 operators/acumen/build_dawn_brief.py --input-jsonl "$(INPUT_JSONL)" --output "$(OUTPUT)"

acumen-build-verified-signal-brief:
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-verified-signal-brief OUTPUT=/abs/path/VERIFIED-SIGNAL-BRIEF.md [ASSESSMENT_JSON_DIR=runtime/acumen/out/augur-return-assessments] [QUEUE_JSON=orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json]" && exit 1)
	python3 operators/acumen/build_verified_signal_brief.py --assessment-json-dir "$(or $(ASSESSMENT_JSON_DIR),runtime/acumen/out/augur-return-assessments)" --queue-json "$(or $(QUEUE_JSON),orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json)" --output "$(OUTPUT)"

acumen-build-primary-source-queue-readout:
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-primary-source-queue-readout OUTPUT=/abs/path/PRIMARY-SOURCE-QUEUE-READOUT.md [QUEUE_JSON=orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json] [ASSESSMENT_JSON_DIR=runtime/acumen/out/augur-return-assessments]" && exit 1)
	python3 operators/acumen/build_primary_source_queue_readout.py --queue-json "$(or $(QUEUE_JSON),orchestration/state/ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json)" --assessment-json-dir "$(or $(ASSESSMENT_JSON_DIR),runtime/acumen/out/augur-return-assessments)" --output "$(OUTPUT)"

acumen-build-intelligence-product-family:
	@test -n "$(DATESTAMP)" || (echo "usage: make acumen-build-intelligence-product-family DATESTAMP=YYYYMMDD [OUT=runtime/acumen/out]" && exit 1)
	$(MAKE) acumen-build-verified-signal-brief OUTPUT="$(or $(OUT),runtime/acumen/out)/VERIFIED-SIGNAL-BRIEF-$(DATESTAMP).md" $(if $(ASSESSMENT_JSON_DIR),ASSESSMENT_JSON_DIR="$(ASSESSMENT_JSON_DIR)",) $(if $(QUEUE_JSON),QUEUE_JSON="$(QUEUE_JSON)",)
	$(MAKE) acumen-build-primary-source-queue-readout OUTPUT="$(or $(OUT),runtime/acumen/out)/PRIMARY-SOURCE-QUEUE-READOUT-$(DATESTAMP).md" $(if $(ASSESSMENT_JSON_DIR),ASSESSMENT_JSON_DIR="$(ASSESSMENT_JSON_DIR)",) $(if $(QUEUE_JSON),QUEUE_JSON="$(QUEUE_JSON)",)

acumen-pipeline-run:
	@test -n "$(QUEUE)" || (echo "usage: make acumen-pipeline-run QUEUE=/abs/path/triage-decisions.jsonl OUT=/abs/path/output-dir [REGISTRY=runtime/acumen/registry.json] [STATUS_JSON=orchestration/state/ACUMEN-PIPELINE-STATUS.json] [BINDING=orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json] [POLL_MODE=auto|fixture|live] [FIXTURE_FEED=/abs/path/feed.json] [TRIAGE_MODE=auto|heuristic|gemini] [STRICT_IDENTITY=1]" && exit 1)
	@test -n "$(OUT)" || (echo "usage: make acumen-pipeline-run QUEUE=/abs/path/triage-decisions.jsonl OUT=/abs/path/output-dir [REGISTRY=runtime/acumen/registry.json] [STATUS_JSON=orchestration/state/ACUMEN-PIPELINE-STATUS.json] [BINDING=orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json] [POLL_MODE=auto|fixture|live] [FIXTURE_FEED=/abs/path/feed.json] [TRIAGE_MODE=auto|heuristic|gemini] [STRICT_IDENTITY=1]" && exit 1)
	python3 operators/acumen/pipeline_flow.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --queue "$(QUEUE)" --out "$(OUT)" --status-json "$(or $(STATUS_JSON),orchestration/state/ACUMEN-PIPELINE-STATUS.json)" --identity-binding "$(or $(BINDING),orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json)" --poll-cursor-json "$(or $(POLL_CURSOR_JSON),runtime/acumen/poll_cursor.json)" --poll-status-json "$(or $(POLL_STATUS_JSON),runtime/acumen/poll-status.json)" --poll-mode "$(or $(POLL_MODE),auto)" --training-jsonl "$(or $(TRAINING_JSONL),runtime/acumen/training-corpus.jsonl)" --triage-status-json "$(or $(TRIAGE_STATUS_JSON),runtime/acumen/triage-status.json)" --triage-mode "$(or $(TRIAGE_MODE),auto)" $(if $(FIXTURE_FEED),--fixture-feed "$(FIXTURE_FEED)",) $(if $(filter 1 true yes,$(FORCE_POLL)),--force-poll,) $(if $(TRIAGE_ARTIFACT_DIR),--triage-artifact-dir "$(TRIAGE_ARTIFACT_DIR)",) $(if $(IDENTITY_STATUS_JSON),--identity-status-json "$(IDENTITY_STATUS_JSON)",) $(if $(API_KEY_ENV),--triage-api-key-env "$(API_KEY_ENV)",) $(if $(API_BASE),--triage-api-base "$(API_BASE)",) $(if $(TIMEOUT_SECONDS),--triage-timeout-seconds "$(TIMEOUT_SECONDS)",) $(if $(MAX_LIVE_CALLS),--max-live-calls "$(MAX_LIVE_CALLS)",) $(if $(MAX_RETRIES),--max-retries "$(MAX_RETRIES)",) $(if $(RETRY_BACKOFF_SECONDS),--retry-backoff-seconds "$(RETRY_BACKOFF_SECONDS)",) $(if $(MAX_PROMPT_CHARS),--max-prompt-chars "$(MAX_PROMPT_CHARS)",) $(if $(MAX_OUTPUT_TOKENS),--max-output-tokens "$(MAX_OUTPUT_TOKENS)",) $(if $(MAX_TOTAL_TOKENS),--max-total-tokens "$(MAX_TOTAL_TOKENS)",) $(if $(ESTIMATED_COST_PER_CALL_USD),--estimated-cost-per-call-usd "$(ESTIMATED_COST_PER_CALL_USD)",) $(if $(MAX_ESTIMATED_COST_USD),--max-estimated-cost-usd "$(MAX_ESTIMATED_COST_USD)",) $(if $(filter 1 true yes,$(STRICT_IDENTITY)),--strict-identity,)

acumen-record-triage-decision:
	@test -n "$(INPUT_JSON)" || (echo "usage: make acumen-record-triage-decision INPUT_JSON=/abs/path/decision.json ACTOR=acumen.triage" && exit 1)
	@test -n "$(ACTOR)" || (echo "usage: make acumen-record-triage-decision INPUT_JSON=/abs/path/decision.json ACTOR=acumen.triage" && exit 1)
	python3 operators/acumen/record_evidence.py decision --input-json "$(INPUT_JSON)" --actor "$(ACTOR)"

acumen-record-model-call:
	@test -n "$(INPUT_JSON)" || (echo "usage: make acumen-record-model-call INPUT_JSON=/abs/path/model-call.json ACTOR=acumen.triage" && exit 1)
	@test -n "$(ACTOR)" || (echo "usage: make acumen-record-model-call INPUT_JSON=/abs/path/model-call.json ACTOR=acumen.triage" && exit 1)
	python3 operators/acumen/record_evidence.py model-call --input-json "$(INPUT_JSON)" --actor "$(ACTOR)"

acumen-rematerialize-evidence:
	python3 operators/acumen/rematerialize_evidence.py

acumen-validate-evidence:
	python3 operators/validators/validate_acumen_evidence.py

acumen-build-verification-bridge:
	python3 operators/acumen/build_verification_bridge.py --triage-ledger "$(or $(TRIAGE_LEDGER),orchestration/state/registry/acumen-triage-decision-ledger.jsonl)" --training-ledger "$(or $(TRAINING_LEDGER),orchestration/state/registry/acumen-training-corpus-ledger.jsonl)" --sandbox-ledger "$(or $(SANDBOX_LEDGER),orchestration/state/SANDBOX-EVENT-LEDGER.jsonl)" --dossier-dir "$(or $(DOSSIER_DIR),runtime/acumen/out/verification-dossiers)" --bridge-status-json "$(or $(BRIDGE_STATUS_JSON),orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json)" --portfolio-json "$(or $(PORTFOLIO_JSON),runtime/acumen/out/verification-portfolio.json)" --portfolio-md "$(or $(PORTFOLIO_MD),runtime/acumen/out/verification-portfolio.md)" $(if $(INCLUDE_INGESTED),--include-ingested,) $(if $(MAX_ITEMS),--max-items "$(MAX_ITEMS)",) $(foreach DECISION,$(DECISIONS),--decision "$(DECISION)") $(foreach VIDEO_ID,$(VIDEO_IDS),--video-id "$(VIDEO_ID)") $(foreach EVENT_ID,$(TRIAGE_EVENT_IDS),--triage-event-id "$(EVENT_ID)")

acumen-validate-verification-bridge:
	python3 operators/validators/validate_acumen_verification_bridge.py --bridge-json "$(or $(BRIDGE_JSON),orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json)" --output-md "$(or $(OUTPUT_MD),orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.md)" --output-json "$(or $(OUTPUT_JSON),orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.json)"

acumen-validate-live-batch-proof:
	python3 operators/validators/validate_acumen_live_batch_proof.py --ledger "$(or $(RECEIPT_LEDGER),orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl)" --status-json "$(or $(PROOF_STATUS_JSON),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json)" --output-md "$(or $(OUTPUT_MD),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.md)" --output-json "$(or $(OUTPUT_JSON),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.json)"

acumen-preflight:
	$(MAKE) acumen-init-registry SEED="$(or $(SEED),operators/acumen/channel_seed.example.json)" OUTPUT="$(or $(REGISTRY_OUTPUT),runtime/acumen/registry.json)" $(if $(MERGE),MERGE="$(MERGE)",)
	$(MAKE) acumen-validate-registry REGISTRY="$(or $(REGISTRY),$(or $(REGISTRY_OUTPUT),runtime/acumen/registry.json))" $(if $(STRICT),STRICT="$(STRICT)",)
	$(MAKE) acumen-identity-probe BINDING="$(or $(BINDING),orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json)" OUTPUT="$(or $(IDENTITY_OUTPUT),orchestration/state/ACUMEN-IDENTITY-STATUS.json)" $(if $(STRICT),STRICT="$(STRICT)",)

acumen-sample-run:
	$(MAKE) acumen-preflight $(if $(SEED),SEED="$(SEED)",) $(if $(REGISTRY_OUTPUT),REGISTRY_OUTPUT="$(REGISTRY_OUTPUT)",) $(if $(REGISTRY),REGISTRY="$(REGISTRY)",) $(if $(BINDING),BINDING="$(BINDING)",) $(if $(IDENTITY_OUTPUT),IDENTITY_OUTPUT="$(IDENTITY_OUTPUT)",) $(if $(STRICT),STRICT="$(STRICT)",)
	$(MAKE) acumen-build-triage-packet CHANNEL_ID="$(or $(CHANNEL_ID),UC_x5XG1OV2P6uZZ5FSM9Ttw)" VIDEO_JSON="$(or $(VIDEO_JSON),runtime/acumen/sample-video.json)" REGISTRY="$(or $(REGISTRY),$(or $(REGISTRY_OUTPUT),runtime/acumen/registry.json))" OUTPUT="$(or $(TRIAGE_OUTPUT),runtime/acumen/out/triage-packet.sample.json)" PROMPT_OUTPUT="$(or $(TRIAGE_PROMPT_OUTPUT),runtime/acumen/out/triage-prompt.sample.md)"
	$(MAKE) acumen-deterministic-track INPUT_TEXT="$(or $(INPUT_TEXT),runtime/acumen/sample-transcript.txt)" GENRE="$(or $(GENRE),Commentary)" DEPTH="$(or $(DEPTH),Precis)" POLISH="$(or $(POLISH),clean_verbatim)" $(if $(RESOLUTION_JSON),RESOLUTION_JSON="$(RESOLUTION_JSON)",) $(if $(DEBUG_JSON),DEBUG_JSON="$(DEBUG_JSON)",) OUTPUT="$(or $(TRACK_OUTPUT),runtime/acumen/out/deterministic-sample.md)"
	$(MAKE) acumen-build-dawn-brief INPUT_JSONL="$(or $(INPUT_JSONL),runtime/acumen/triage-decisions.sample.jsonl)" OUTPUT="$(or $(DAWN_OUTPUT),runtime/acumen/out/DAWN-BRIEF-sample.md)"
	$(MAKE) acumen-pipeline-run QUEUE="$(or $(QUEUE),runtime/acumen/triage-decisions.jsonl)" OUT="$(or $(OUT),runtime/acumen/out)" REGISTRY="$(or $(REGISTRY),$(or $(REGISTRY_OUTPUT),runtime/acumen/registry.json))" STATUS_JSON="$(or $(STATUS_JSON),orchestration/state/ACUMEN-PIPELINE-STATUS.json)" BINDING="$(or $(BINDING),orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json)" POLL_MODE=fixture FIXTURE_FEED="$(or $(FIXTURE_FEED),runtime/acumen/poll-fixture.sample.json)" TRIAGE_MODE="$(or $(TRIAGE_MODE),heuristic)" FORCE_POLL=1 TRAINING_JSONL="$(or $(TRAINING_JSONL),runtime/acumen/training-corpus.jsonl)" $(if $(STRICT),STRICT_IDENTITY="$(STRICT)",)

acumen-live-batch:
	@status=0; \
	python3 operators/acumen/run_live_batch_proof.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --binding "$(or $(BINDING),orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json)" --queue "$(or $(QUEUE),runtime/acumen/triage-decisions.jsonl)" --training-jsonl "$(or $(TRAINING_JSONL),runtime/acumen/training-corpus.jsonl)" --out "$(or $(OUT),runtime/acumen/out)" --pipeline-status-json "$(or $(STATUS_JSON),orchestration/state/ACUMEN-PIPELINE-STATUS.json)" --identity-status-json "$(or $(IDENTITY_OUTPUT),orchestration/state/ACUMEN-IDENTITY-STATUS.json)" --poll-status-json "$(or $(POLL_STATUS_JSON),orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json)" --triage-status-json "$(or $(TRIAGE_STATUS_JSON),runtime/acumen/triage-status.json)" --proof-status-json "$(or $(PROOF_STATUS_JSON),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json)" --receipt-ledger "$(or $(RECEIPT_LEDGER),orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl)" --youtube-api-env "$(or $(YOUTUBE_API_ENV),ACUMEN_YOUTUBE_API_KEY)" --gemini-api-env "$(or $(API_KEY_ENV),GEMINI_API_KEY)" --api-base "$(or $(API_BASE),https://generativelanguage.googleapis.com/v1beta/models)" --timeout-seconds "$(or $(TIMEOUT_SECONDS),45)" --max-live-calls "$(or $(MAX_LIVE_CALLS),12)" --max-retries "$(or $(MAX_RETRIES),2)" --retry-backoff-seconds "$(or $(RETRY_BACKOFF_SECONDS),1.5)" --max-prompt-chars "$(or $(MAX_PROMPT_CHARS),18000)" --max-output-tokens "$(or $(MAX_OUTPUT_TOKENS),220)" --max-total-tokens "$(or $(MAX_TOTAL_TOKENS),4096)" --estimated-cost-per-call-usd "$(or $(ESTIMATED_COST_PER_CALL_USD),0)" --max-estimated-cost-usd "$(or $(MAX_ESTIMATED_COST_USD),0)" $(if $(filter 1 true yes,$(FORCE_POLL)),--force-poll,) || status=$$?; \
	python3 operators/validators/validate_acumen_live_batch_proof.py --ledger "$(or $(RECEIPT_LEDGER),orchestration/state/registry/acumen-live-batch-proof-ledger.jsonl)" --status-json "$(or $(PROOF_STATUS_JSON),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-STATUS.json)" --output-md "$(or $(PROOF_REPORT_MD),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.md)" --output-json "$(or $(PROOF_REPORT_JSON),orchestration/state/ACUMEN-LIVE-BATCH-PROOF-REPORT.json)"; \
	exit $$status

exocortex-sync-surface-registry:
	python3 operators/exocortex/exocortex_surface_registry_bridge.py $(if $(PROJECT_ONTOLOGY),--project-ontology,) --ontology-url "$(or $(ONTOLOGY_URL),domain)"

exocortex-import-connector-guide:
	python3 operators/exocortex/import_connector_guide.py --guide "$(or $(GUIDE),/Users/system/Desktop/guide.md)" $(if $(REGISTRY),--registry "$(REGISTRY)",) $(if $(OUTPUT),--output "$(OUTPUT)",)

exocortex-audit-control-plane:
	python3 operators/exocortex/exocortex_control_plane_audit.py $(if $(REGISTRY),--registry "$(REGISTRY)",) $(if $(TELEOLOGY),--teleology "$(TELEOLOGY)",) $(if $(CONNECTOR_MANIFEST),--connector-manifest "$(CONNECTOR_MANIFEST)",) $(if $(OUTPUT_JSON),--output-json "$(OUTPUT_JSON)",) $(if $(OUTPUT_MD),--output-md "$(OUTPUT_MD)",)

exocortex-sync-connector-manifest:
	python3 operators/exocortex/exocortex_connector_manifest_bridge.py $(if $(PROJECT_ONTOLOGY),--project-ontology,) --ontology-url "$(or $(ONTOLOGY_URL),domain)"

exocortex-apply-connector-receipts:
	@test -n "$(RECEIPTS)" || (echo "usage: make exocortex-apply-connector-receipts RECEIPTS=/abs/path/receipts.json [BATCH_ID=batch-id] [STRICT=1]" && exit 1)
	python3 operators/exocortex/apply_connector_verification_receipts.py --receipts "$(RECEIPTS)" $(if $(MANIFEST),--manifest "$(MANIFEST)",) $(if $(TRACKER),--tracker "$(TRACKER)",) $(if $(TRACKER_MD),--tracker-md "$(TRACKER_MD)",) $(if $(BATCH_ID),--batch-id "$(BATCH_ID)",) $(if $(filter 1 true yes,$(STRICT)),--strict-unknown,)

exocortex-connector-verification-run:
	@test -n "$(RECEIPTS)" || (echo "usage: make exocortex-connector-verification-run RECEIPTS=/abs/path/receipts.json [BATCH_ID=batch-id] [STRICT=1] [PROJECT_ONTOLOGY=1]" && exit 1)
	$(MAKE) exocortex-apply-connector-receipts RECEIPTS="$(RECEIPTS)" $(if $(BATCH_ID),BATCH_ID="$(BATCH_ID)",) $(if $(STRICT),STRICT="$(STRICT)",)
	$(MAKE) exocortex-audit-control-plane
	$(MAKE) exocortex-sync-connector-manifest $(if $(PROJECT_ONTOLOGY),PROJECT_ONTOLOGY=1,) ONTOLOGY_URL="$(or $(ONTOLOGY_URL),domain)"
	$(MAKE) ontology-project-repo

exocortex-control-plane-run:
	$(MAKE) exocortex-import-connector-guide GUIDE="$(or $(GUIDE),/Users/system/Desktop/guide.md)"
	$(MAKE) exocortex-audit-control-plane
	$(MAKE) exocortex-sync-connector-manifest $(if $(PROJECT_ONTOLOGY),PROJECT_ONTOLOGY=1,) ONTOLOGY_URL="$(or $(ONTOLOGY_URL),domain)"
	$(MAKE) ontology-project-repo

ajna-exocortex-access-program:
	python3 operators/exocortex/render_ajna_access_program.py $(if $(REGISTRY),--registry "$(REGISTRY)",) $(if $(TELEOLOGY),--teleology "$(TELEOLOGY)",) $(if $(OUTPUT_JSON),--output-json "$(OUTPUT_JSON)",) $(if $(OUTPUT_MD),--output-md "$(OUTPUT_MD)",)

ajna-auth-wave-packet:
	@test -n "$(WAVE)" || (echo "usage: make ajna-auth-wave-packet WAVE=wave1_priority_hubs OUTPUT=/abs/path/packet.md [PROGRAM=/abs/path/program.json]" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make ajna-auth-wave-packet WAVE=wave1_priority_hubs OUTPUT=/abs/path/packet.md [PROGRAM=/abs/path/program.json]" && exit 1)
	python3 operators/exocortex/build_ajna_auth_wave_packet.py --wave "$(WAVE)" --output "$(OUTPUT)" $(if $(PROGRAM),--program "$(PROGRAM)",)

ontology-project-repo:
	python3 operators/ontology/ontology_v1.py project-repo

webshell-dev:
	python3 operators/webshell/syncrescendence_dev_shell.py --repo-root "$(or $(REPO_ROOT),$(CURDIR))" --host "$(or $(HOST),127.0.0.1)" --port "$(or $(PORT),8890)" $(if $(CALLBACK_TOKEN),--callback-token "$(CALLBACK_TOKEN)",) $(if $(GITHUB_WEBHOOK_SECRET),--github-webhook-secret "$(GITHUB_WEBHOOK_SECRET)",) $(if $(SLACK_SIGNING_SECRET),--slack-signing-secret "$(SLACK_SIGNING_SECRET)",) $(if $(ENFORCE_PROVIDER_SIGNATURES),--enforce-provider-signatures,)

webshell-smoke:
	@test -n "$(PORT)" || (echo "usage: make webshell-smoke PORT=8890" && exit 1)
	curl -fsS "http://127.0.0.1:$(PORT)/health" > /dev/null
	curl -fsS "http://127.0.0.1:$(PORT)/status" > /dev/null
	curl -fsS "http://127.0.0.1:$(PORT)/docs" > /dev/null
	echo "webshell smoke passed on :$(PORT)"

webshell-callback-smoke:
	@test -n "$(PORT)" || (echo "usage: make webshell-callback-smoke PORT=8890 CALLBACK_TOKEN=token" && exit 1)
	@test -n "$(CALLBACK_TOKEN)" || (echo "usage: make webshell-callback-smoke PORT=8890 CALLBACK_TOKEN=token" && exit 1)
	@curl -fsS -X POST "http://127.0.0.1:$(PORT)/callbacks/generic" \
	  -H "Content-Type: application/json" \
	  -H "X-Sync-Token: $(CALLBACK_TOKEN)" \
	  -d '{"event":"callback-smoke","source":"make"}' > /dev/null
	@echo "webshell callback smoke passed on :$(PORT)"

webshell-generate-token:
	python3 -c "import secrets; print(secrets.token_urlsafe(32))"

webshell-keychain-status:
	./operators/webshell/webshell_keychain.sh status

webshell-keychain-init-callback:
	./operators/webshell/webshell_keychain.sh init-callback-token

webshell-launchagent-install:
	./operators/webshell/install_local_webshell_launchagent.sh

webshell-launchagent-status:
	./operators/webshell/webshell_launchagent_status.sh

webshell-launchagent-restart:
	launchctl kickstart -k "gui/$$(id -u)/com.syncrescendence.webshell-ops"
