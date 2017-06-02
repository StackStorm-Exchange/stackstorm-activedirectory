ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
CI_REPO_PATH ?= $(ROOT_DIR)/ci
CI_REPO_BRANCH ?= master

# read in pack's name from pack.yaml, export it so that the ci/Makefile
# can access its value
export PACK_NAME := $(shell grep "name:" pack.yaml | awk '{ print $$2 }')

.PHONY: all
all: invoke-ci-makefile

.PHONY: all
clean: clean-ci-repo

.PHONY: pack-name
pack-name: .pack-name invoke-ci-makefile

.PHONY: .pack-name
.pack-name:
	@echo $(PACK_NAME)

.PHONY: clone-ci-repo
clone-ci-repo:
	@echo
	@echo "==================== clone-ci-repo ===================="
	@echo
	@if [ ! -d "$(CI_REPO_PATH)" ]; then \
		git clone https://github.com/EncoreTechnologies/ci-stackstorm.git --depth 1 --single-branch --branch $(CI_REPO_BRANCH) $(CI_REPO_PATH); \
	else \
		pushd $(CI_REPO_PATH) &> /dev/null; \
		git pull; \
		popd &> /dev/null; \
	fi;

.PHONY: clean-ci-repo
clean-ci-repo:
	@echo
	@echo "==================== clean-ci-repo ===================="
	@echo
	@if [ -d "$(CI_REPO_PATH)" ]; then \
		make -f $(ROOT_DIR)/ci/Makefile clean; \
	fi;
	rm -rf $(CI_REPO_PATH)


# forward all make targets to the ci makefile to do the actual work
.PHONY: invoke-ci-makefile
invoke-ci-makefile: clone-ci-repo
	@echo
	@echo "==================== invoke-ci-makefile ===================="
	@echo
	make -f $(ROOT_DIR)/ci/Makefile $(MAKECMDGOALS)
