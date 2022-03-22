del output_trs_I
del output_trs_II

python parselatest.py

python parselatest.py no_file

python parselatest.py bad_code.json

python parselatest.py bad_json.json

python parselatest.py Golden_input_trs_I.json

ren output_trs output_trs_I

python parselatest.py Golden_input_trs_II.json

ren output_trs output_trs_II

python test_module_pytest.py
