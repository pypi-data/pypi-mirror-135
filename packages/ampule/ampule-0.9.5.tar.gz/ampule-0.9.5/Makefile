MAKEFLAGS += -r -R --warn-undefined-variables --no-print-directory
include ampule_config.mk
#------------------------------------------------------------------------------
#Variables
#------------------------------------------------------------------------------
PYS      := $(shell find $(PY_DIR)/ -name '*.py')
PYS_BASE := $(basename $(PYS))
PDFS     := $(PYS_BASE:$(PY_DIR)/%=$(PDF_DIR)/%)
DEPS     := $(PYS_BASE:$(PY_DIR)/%=$(DEP_DIR)/%.d)

.DEFAULT_GOAL = figs
#------------------------------------------------------------------------------
#Plotting figures
#------------------------------------------------------------------------------
figs: $(PDFS)

$(PDF_DIR)/%: $(PY_DIR)/%.py $(DEP_DIR)/%.d
	@mkdir -p $(DEP_DIR)/$(*D); mkdir -p $(PDF_DIR)/$(*D)
	$(PYTHON3) $(PY_DIR)/$*.py $(DEP_DIR)/$*.d $(PDF_DIR)/$*
	@touch $(PDF_DIR)/$*

$(DEP_DIR)/%.d: ;
.PRECIOUS: $(DEP_DIR)/%.d
-include $(DEPS)
#------------------------------------------------------------------------------
#Cleaning targets
#------------------------------------------------------------------------------
.PHONY: clean
clean:
	rm -rf $(PDFS) $(DEPS)
