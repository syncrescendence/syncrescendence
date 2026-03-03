.PHONY: inventory check-artifact-law bootstrap-office migrate-communications-chain archive-shell-manifest rehouse-archived-artifact sync-reference-tree operator-tree

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
