################################################################################
# Description:
#  Executes testing and validation for python code and configuration files
#  within a StackStorm pack.
#
# Pre-requisites
#   # Extra packages
#   yum -y install gcc python-devel python2-pip libyaml libyaml-devel
#
#   # upgrade pip
#   pip install --upgrade pip
#  
#   # st2sdk
#   pip install PyYAML
#   pip install st2sdk
#
#
# Targets:
#  validate-yaml :
#     Checks all .yaml files to ensure they are properly formatted.
#     Validates they are free of syntax errors.
#
#  validate-json :
#     Checks all .json files to ensure they are properly formatted.
#     Validates they are free of syntax errors.
#     
#  validate-pack-metadata-exists :
#     Checks if this pack contains a pack.yaml file
#
#  validate-pack-register :
#     Tries to register this pack with the local StackStorm installation.
#     It succeeds if the registration succeeds, fails otherwise.
#  
#  validate-pack-pylint :
#     See st2sdk
#
#
################################################################################

YAML_FILES := $(shell find $(SOURCEDIR) -name '*.yaml')
JSON_FILES := $(shell find $(SOURCEDIR) -name '*.json')

PACK_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY : all
all : validate


.PHONY : validate
all : validate-yaml \
			validate-json \
			validate-pack-metadata-exists \
			validate-pack-register \
			validate-pack-pylint \


.PHONY: validate-yaml
validate-yaml: $(YAML_FILES)
	@echo "Validating YAML"
	@for yaml in $(YAML_FILES); do \
		st2-check-validate-yaml-file $$yaml; \
	done


.PHONY: validate-json
validate-json: $(JSON_FILES)
	@echo "Validating JSON"
	@for json in $(JSON_FILES); do \
		st2-check-validate-json-file $$json; \
	done


.PHONY: validate-pack-metadata-exists
validate-pack-metadata-exists: $(PACK_DIR) validate-yaml validate-json
	@echo "Validating pack metadata"
	st2-check-validate-pack-metadata-exists $(PACK_DIR)


.PHONY: validate-pack-register
validate-pack-register: $(PACK_DIR) validate-pack-metadata-exists
	@echo "Validating pack registration"
	st2-check-register-pack-resources $(PACK_DIR)


.PHONY: validate-pack-pylint
validate-pack-pylint: $(PACK_DIR) validate-pack-register
	@echo "Validating python files with pylint"
	st2-check-pylint-pack $(PACK_DIR)

