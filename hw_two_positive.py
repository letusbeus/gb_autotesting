from hw_two_checkers import checkout, take_data, folder_in, folder_out, folder_ext


def test_archive_files():
    # test Add files to the archive
    res1 = checkout(f"cd {folder_in}; 7z a ../out/arx2 test1 test2", "Everything is Ok")
    res2 = checkout(f"ls {folder_out}", "arx2")
    assert res1 and res2, "test1 FAIL"


def test_check_hash_sum():
    # test Check hash sum with CRC32 and 7z h
    hash_date_crc32 = str(take_data(f"cd {folder_out}; crc32 arx2.7z")).upper()
    hash_date_7z_check = checkout(f"cd {folder_out}; 7z h arx2.7z", hash_date_crc32)
    assert hash_date_7z_check, "test2 FAIL"


def test_show_archive_content():
    # test List the contents of the archive
    assert checkout(f"cd {folder_out}; 7z l arx2.7z", "Listing archive: arx2.7z")


def test_extract_files_without_dirname():
    # test Extract files from the archive (without using directory names)
    res1 = checkout(f"cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder_ext}", "test1")
    res3 = checkout(f"ls {folder_ext}", "test2")
    assert res1 and res2 and res3, "test2 FAIL"


def test_extract_files_using_full_path():
    # test Extract files with full paths
    res1 = checkout(f"cd {folder_out}; 7z x arx2.7z -o{folder_ext} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder_ext}", "test1")
    res3 = checkout(f"ls {folder_ext}", "test2")
    assert res1 and res2 and res3, "test2 FAIL"


def test_checking_archive_integrity():
    # test Checking the integrity of the archive
    assert checkout(f"cd {folder_out}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_update_archive_files():
    # test Updating files in the archive
    assert checkout(f"cd {folder_in}; 7z u arx2.7z", "Everything is Ok"), "test4 FAIL"


def test_delete_files():
    # test Deleting files from the archive
    assert checkout(f"cd {folder_out}; 7z d arx2.7z", "Everything is Ok"), "test5 FAIL"
