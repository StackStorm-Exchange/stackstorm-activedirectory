THIS_FILE := $(lastword $(MAKEFILE_LIST))
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
CI_REPO_PATH ?= $(ROOT_DIR)/ci
CI_REPO_BRANCH ?= master

# read in pack's name from pack.yaml, export it so that the ci/Makefile
# can access its value
export PACK_NAME := $(shell grep "name:" pack.yaml | awk '{ print $$2 }')

.PHONY: all
all: .DEFAULT

.PHONY: clean
clean: clean-ci-repo clean-pyc

.PHONY: pack-name
pack-name: .pack-name

.PHONY: .pack-name
.pack-name:
	@echo $(PACK_NAME)

# Clone the ci-repo into the ci/ directory
.PHONY: clone-ci-repo
clone-ci-repo:
	@echo
	@echo "==================== clone-ci-repo ===================="
	@echo
	@if [ ! -d "$(CI_REPO_PATH)" ]; then \
		git clone https://github.com/EncoreTechnologies/ci-stackstorm.git --depth 1 --single-branch --branch $(CI_REPO_BRANCH) $(CI_REPO_PATH); \
	else \
		cd $(CI_REPO_PATH); \
		git pull; \
	fi;

# Clean the ci-repo (calling `make clean` in that directory), then remove the
# ci-repo directory
.PHONY: clean-ci-repo
clean-ci-repo:
	@echo
	@echo "==================== clean-ci-repo ===================="
	@echo
	@if [ -d "$(CI_REPO_PATH)" ]; then \
		make -f $(ROOT_DIR)/ci/Makefile clean; \
	fi;
	rm -rf $(CI_REPO_PATH)

# Clean *.pyc files.
.PHONY: clean-pyc
clean-pyc:
	@echo
	@echo "==================== clean-pyc ===================="
	@echo
	find $(ROOT_DIR) -name 'ci' -prune -or -name '.git' -or -type f -name "*.pyc" -print | xargs rm

# list all makefile targets
.PHONY: list
list:
	@if [ -d "$(CI_REPO_PATH)" ]; then \
		$(MAKE) --no-print-directory -f $(ROOT_DIR)/ci/Makefile list; \
	fi;
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | sort | uniq | xargs

# forward all make targets not found in this makefile to the ci makefile to do
# the actual work (by calling the invoke-ci-makefile target)
# http://stackoverflow.org/wiki/Last-Resort_Makefile_Targets
# Unfortunately the .DEFAULT target doesn't allow for dependencies
# so we have to manually specify all of the steps in this target.
.DEFAULT: 
	$(MAKE) clone-ci-repo
	@echo
	@echo "==================== invoke ci/Makefile (targets: $(MAKECMDGOALS)) ===================="
	@echo
	make -f $(ROOT_DIR)/ci/Makefile $(MAKECMDGOALS)
