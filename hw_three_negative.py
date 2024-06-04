from conftest import data
from hw_three_checkers import checkout_negative


class TestNegative:
    def test_negative_step1(self, make_folders, make_broke_file):
        """
        test Extract files from archive (without using directory names)
        :param make_folders:
        :param make_broke_file:
        :return:
        """
        assert checkout_negative(
            f"cd {data['folder_out']}; 7z e {data['arx_name']}.{data['arx_type']} -o{data['folder_ext']} -y",
            "ERROR"), "test1 FAIL"

    def test_negative_step2(self, make_folders, make_broke_file):
        """
        test eXtract files with full paths
        :param make_folders:
        :param make_broke_file:
        :return:
        """
        assert checkout_negative(
            f"cd {data['folder_out']}; 7z x {data['arx_name']}.{data['arx_type']} -o{data['folder_ext']} -y",
            "ERROR"), "test1 FAIL"

    def test_negative_step3(self, make_folders, make_broke_file):
        """
        Test integrity of archive
        :param make_folders:
        :param make_broke_file:
        :return:
        """
        assert checkout_negative(f"cd {data['folder_out']}; 7z t {data['arx_name']}.{data['arx_type']}",
                                 "ERROR"), "test3 FAIL"
