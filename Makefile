.PHONY: inventory check-artifact-law bootstrap-office migrate-communications-chain operator-tree

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
