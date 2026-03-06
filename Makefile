.PHONY: inventory check-artifact-law bootstrap-office migrate-communications-chain archive-shell-manifest rehouse-archived-artifact sync-reference-tree stage-feedstock operator-tree harness-tranche-ab harness-registry-effective harness-promoted-atoms-smoke office-watch-once dispatch-office-task manus-create manus-wait bootstrap-mini revive-mini-constellation constellation-mini-status install-mini-constellation-launchagent tooling-surface-status mini-constellation-collect-status acumen-init-registry acumen-validate-registry acumen-identity-probe acumen-build-triage-packet acumen-deterministic-track acumen-build-dawn-brief acumen-pipeline-run exocortex-sync-surface-registry exocortex-import-connector-guide exocortex-audit-control-plane exocortex-sync-connector-manifest exocortex-control-plane-run ontology-project-repo webshell-dev webshell-smoke webshell-callback-smoke webshell-generate-token webshell-keychain-status webshell-keychain-init-callback webshell-launchagent-install webshell-launchagent-status webshell-launchagent-restart

inventory:
	python3 operators/validators/artifact_law_inventory.py --format both

check-artifact-law:
	python3 operators/validators/artifact_law_inventory.py --format both --check

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

acumen-build-triage-packet:
	@test -n "$(CHANNEL_ID)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.md" && exit 1)
	@test -n "$(VIDEO_JSON)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.md" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-triage-packet CHANNEL_ID=<youtube channel id> VIDEO_JSON=/abs/path/video.json [REGISTRY=runtime/acumen/registry.json] OUTPUT=/abs/path/out.md" && exit 1)
	python3 operators/acumen/build_triage_packet.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --channel-id "$(CHANNEL_ID)" --video "$(VIDEO_JSON)" --output "$(OUTPUT)"

acumen-deterministic-track:
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-deterministic-track OUTPUT=/abs/path/out.md [INPUT_TEXT=/abs/path/file.txt|INPUT_CAPTIONS=/abs/path/captions.json] [GENRE=Commentary] [DEPTH=Precis] [POLISH=clean_verbatim]" && exit 1)
	@test -n "$(INPUT_TEXT)$(INPUT_CAPTIONS)" || (echo "usage: make acumen-deterministic-track OUTPUT=/abs/path/out.md [INPUT_TEXT=/abs/path/file.txt|INPUT_CAPTIONS=/abs/path/captions.json] [GENRE=Commentary] [DEPTH=Precis] [POLISH=clean_verbatim]" && exit 1)
	python3 operators/acumen/deterministic_track.py $(if $(INPUT_TEXT),--input-text "$(INPUT_TEXT)",) $(if $(INPUT_CAPTIONS),--input-captions "$(INPUT_CAPTIONS)",) --genre "$(or $(GENRE),Commentary)" --target-depth "$(or $(DEPTH),Precis)" --target-polish "$(or $(POLISH),clean_verbatim)" $(if $(RESOLUTION_JSON),--resolution-json "$(RESOLUTION_JSON)",) $(if $(DEBUG_JSON),--debug-json "$(DEBUG_JSON)",) --output "$(OUTPUT)"

acumen-build-dawn-brief:
	@test -n "$(INPUT_JSONL)" || (echo "usage: make acumen-build-dawn-brief INPUT_JSONL=/abs/path/decisions.jsonl OUTPUT=/abs/path/DAWN-BRIEF.md" && exit 1)
	@test -n "$(OUTPUT)" || (echo "usage: make acumen-build-dawn-brief INPUT_JSONL=/abs/path/decisions.jsonl OUTPUT=/abs/path/DAWN-BRIEF.md" && exit 1)
	python3 operators/acumen/build_dawn_brief.py --input-jsonl "$(INPUT_JSONL)" --output "$(OUTPUT)"

acumen-pipeline-run:
	@test -n "$(QUEUE)" || (echo "usage: make acumen-pipeline-run QUEUE=/abs/path/triage-decisions.jsonl OUT=/abs/path/output-dir [REGISTRY=runtime/acumen/registry.json]" && exit 1)
	@test -n "$(OUT)" || (echo "usage: make acumen-pipeline-run QUEUE=/abs/path/triage-decisions.jsonl OUT=/abs/path/output-dir [REGISTRY=runtime/acumen/registry.json]" && exit 1)
	python3 operators/acumen/pipeline_flow.py --registry "$(or $(REGISTRY),runtime/acumen/registry.json)" --queue "$(QUEUE)" --out "$(OUT)" --status-json "$(or $(STATUS_JSON),orchestration/state/ACUMEN-PIPELINE-STATUS.json)"

exocortex-sync-surface-registry:
	python3 operators/exocortex/exocortex_surface_registry_bridge.py $(if $(PROJECT_ONTOLOGY),--project-ontology,) --ontology-url "$(or $(ONTOLOGY_URL),domain)"

exocortex-import-connector-guide:
	python3 operators/exocortex/import_connector_guide.py --guide "$(or $(GUIDE),/Users/system/Desktop/guide.md)" $(if $(REGISTRY),--registry "$(REGISTRY)",) $(if $(OUTPUT),--output "$(OUTPUT)",)

exocortex-audit-control-plane:
	python3 operators/exocortex/exocortex_control_plane_audit.py $(if $(REGISTRY),--registry "$(REGISTRY)",) $(if $(TELEOLOGY),--teleology "$(TELEOLOGY)",) $(if $(CONNECTOR_MANIFEST),--connector-manifest "$(CONNECTOR_MANIFEST)",) $(if $(OUTPUT_JSON),--output-json "$(OUTPUT_JSON)",) $(if $(OUTPUT_MD),--output-md "$(OUTPUT_MD)",)

exocortex-sync-connector-manifest:
	python3 operators/exocortex/exocortex_connector_manifest_bridge.py $(if $(PROJECT_ONTOLOGY),--project-ontology,) --ontology-url "$(or $(ONTOLOGY_URL),domain)"

exocortex-control-plane-run:
	$(MAKE) exocortex-import-connector-guide GUIDE="$(or $(GUIDE),/Users/system/Desktop/guide.md)"
	$(MAKE) exocortex-audit-control-plane
	$(MAKE) exocortex-sync-connector-manifest $(if $(PROJECT_ONTOLOGY),PROJECT_ONTOLOGY=1,) ONTOLOGY_URL="$(or $(ONTOLOGY_URL),domain)"
	$(MAKE) ontology-project-repo

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
