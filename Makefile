.PHONY: inventory check-artifact-law bootstrap-office migrate-communications-chain archive-shell-manifest rehouse-archived-artifact sync-reference-tree stage-feedstock operator-tree harness-tranche-ab harness-registry-effective harness-promoted-atoms-smoke office-watch-once dispatch-office-task manus-create manus-wait bootstrap-mini revive-mini-constellation constellation-mini-status install-mini-constellation-launchagent webshell-dev webshell-smoke

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

webshell-dev:
	python3 operators/webshell/syncrescendence_dev_shell.py --repo-root "$(or $(REPO_ROOT),$(CURDIR))" --host "$(or $(HOST),127.0.0.1)" --port "$(or $(PORT),8890)" $(if $(CALLBACK_TOKEN),--callback-token "$(CALLBACK_TOKEN)",)

webshell-smoke:
	@test -n "$(PORT)" || (echo "usage: make webshell-smoke PORT=8890" && exit 1)
	curl -fsS "http://127.0.0.1:$(PORT)/health" > /dev/null
	curl -fsS "http://127.0.0.1:$(PORT)/status" > /dev/null
	curl -fsS "http://127.0.0.1:$(PORT)/docs" > /dev/null
	echo "webshell smoke passed on :$(PORT)"

webshell-callback-smoke:
	@test -n "$(PORT)" || (echo "usage: make webshell-callback-smoke PORT=8890 CALLBACK_TOKEN=token" && exit 1)
	@test -n "$(CALLBACK_TOKEN)" || (echo "usage: make webshell-callback-smoke PORT=8890 CALLBACK_TOKEN=token" && exit 1)
	curl -fsS -X POST "http://127.0.0.1:$(PORT)/callbacks/generic" \
	  -H "Content-Type: application/json" \
	  -H "X-Sync-Token: $(CALLBACK_TOKEN)" \
	  -d '{"event":"callback-smoke","source":"make"}' > /dev/null
	echo "webshell callback smoke passed on :$(PORT)"
