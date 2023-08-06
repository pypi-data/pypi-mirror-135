mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
PACKAGE := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))


help:
	@echo "Run :"
	@echo "  - make install to install the program"
	@echo "  - make doc to compile the doc"
	@echo "  - make a_command to run python setup.py 'a_command'"

.PHONY: help Makefile

doc:
	@echo "Making documentation..."
	@pip3 install pdoc3
	@pdoc --html $(PACKAGE) -o docs
	@mv docs/$(PACKAGE)/* docs/
	@rm -r docs/$(PACKAGE)
