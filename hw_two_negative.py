from hw_two_checkers import checkout_negative, folder_out, folder_ext


def test_negative_extract_without_structure():
    # test neg 1
    assert checkout_negative(f"cd {folder_out}; 7z e arx3.7z -o{folder_ext} -y", "ERROR"), "test1 FAIL"


def test_negative_extract_with_full_structure():
    # test neg 1
    assert checkout_negative(f"cd {folder_out}; 7z x arx3.7z -o{folder_ext} -y", "ERROR"), "test2 FAIL"


def test_negative_check_integrity():
    # test neg 2
    assert checkout_negative(f"cd {folder_out}; 7z t arx3.7z", "ERROR"), "test3 FAIL"
