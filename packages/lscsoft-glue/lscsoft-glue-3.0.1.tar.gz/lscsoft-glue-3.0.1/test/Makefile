PYTHON ?= python

check : \
	glue_ligolw_ilwd_verify \
	iterutils_verify \
	lal_verify \
	ligo_lw_test_01 \
	test_ldbd \
	test_ligolw_array \
	test_ligolw_ligolw \
	test_ligolw_lsctables \
	test_ligolw_table \
	test_ligolw_tokenizer \
	test_ligolw_utils \
	test_ligolw_utils_segments \
	test_pidfile \
	test_pipeline \
	;
	@echo "All Tests Passed"

define printpassfail
	{ echo "Pass" ; true ; } || { echo "Fail" ; false ; }
endef

%: %.py
	@echo "=== start $@ ===>"
	$(PYTHON) $< && $(printpassfail)
	@echo "<=== end $@ ==="

clean :
	rm -f ligo_lw_test_01*png
