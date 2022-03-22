# /bin/env python
# coding: utf-8

import pytest

#Golden_output_trs_I
def test_Golden_output_trs_I():
    b_files_equal = True

    f_validated = open('Golden_output_trs_I', 'r')
    f_test = open('output_trs_I', 'r')

    i = 0
    for (str_validated_line, str_test_line) in zip(f_validated, f_test):
        i += 1
        if str_validated_line != str_test_line:
            b_files_equal = False

    if 0 == i:
        b_files_equal = False

    f_validated.close()
    f_test.close()

    assert b_files_equal is True

#Golden_output_trs_II
def test_Golden_output_trs_II():
    b_files_equal = True

    f_validated = open('Golden_output_trs_II', 'r')
    f_test = open('output_trs_II', 'r')

    i = 0
    for (str_validated_line, str_test_line) in zip(f_validated, f_test):
        i += 1
        if str_validated_line != str_test_line:
            b_files_equal = False

    if 0 == i:
        b_files_equal = False

    f_validated.close()
    f_test.close()

    assert b_files_equal is True

if __name__ == '__main__':
    pytest.main()
