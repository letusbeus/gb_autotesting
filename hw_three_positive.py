from hw_three_checkers import (checkout, take_data)
from conftest import data


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, stat_log):
        """
        test Add files to archive
        :param make_folders:
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res1 = checkout(f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2", "Everything is Ok")
        res2 = checkout(f"ls {data['folder_out']}", f"arx2.{data['arx_type']}")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, stat_log):
        """
        test check hash sum with CRC32 and 7z h
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = []
        for item in make_files:
            res.append(checkout(f"cd {data['folder_in']}; 7z h {item}", "Everything is Ok"))
            hash_date_crc32 = str(take_data(f"cd {data['folder_in']}; crc32 {item}")).upper()
            res.append(checkout(f"cd {data['folder_in']}; 7z h {item}", hash_date_crc32))
        assert all(res), "test2 FAIL"

    def test_step3(self, clear_folders, make_files, stat_log):
        """
        test List contents of archive
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = [checkout(f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2",
                        "Everything is Ok")]
        for item in make_files:
            res.append(checkout(f"cd {data['folder_out']}; 7z l arx2.{data['arx_type']}", item))
        assert all(res), "test3 FAIL"

    def test_step4(self, clear_folders, make_files, stat_log):
        """
        test Extract files from archive (without using directory names)
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = [checkout(f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2",
                        "Everything is Ok"),
               checkout(f"cd {data['folder_out']}; 7z e arx2.{data['arx_type']} -o{data['folder_ext']} -y",
                        "Everything is Ok")]
        for item in make_files:
            res.append(checkout(f"ls {data['folder_ext']}", item))
        assert all(res), "test2 FAIL"

    def test_step5(self, clear_folders, make_files, make_subfolder, stat_log):
        """
        test eXtract files with full paths
        :param clear_folders:
        :param make_files:
        :param make_subfolder:
        :param stat_log:
        :return:
        """
        res = [
            checkout(f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx", "Everything is Ok"),
            checkout(f"cd {data['folder_out']}; 7z x arx.{data['arx_type']} -o{data['folder_ext2']} -y",
                     "Everything is Ok")]
        for item in make_files:
            res.append(checkout(f"ls {data['folder_ext2']}", item))
        res.append(checkout(f"ls {data['folder_ext2']}", make_subfolder[0]))
        res.append(checkout(f"ls {data['folder_ext2']}", make_subfolder[0]))
        assert all(res), "test5 FAIL"

    def test_step6(self, stat_log):
        """
        Test integrity of archive
        :param stat_log:
        :return:
        """
        assert checkout(f"cd {data['folder_out']}; 7z t arx.{data['arx_type']}", "Everything is Ok"), "test3 FAIL"

    def test_step7(self, stat_log):
        """
        test Update files to archive
        :param stat_log:
        :return:
        """
        assert checkout(f"cd {data['folder_in']}; 7z u arx.{data['arx_type']}", "Everything is Ok"), "test4 FAIL"

    def test_step8(self, stat_log):
        """
        test Delete files from archive
        :param stat_log:
        :return:
        """
        assert checkout(f"cd {data['folder_out']}; 7z d arx.{data['arx_type']}", "Everything is Ok"), "test5 FAIL"

    def test_step9(self, clear_folders, stat_log):
        """
        delite all files in folders and check it
        :param clear_folders:
        :param stat_log:
        :return:
        """
        res = [data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']]
        checkout_clean = []
        for item in res:
            iter_step = checkout(f"cd {item}; ls -l", "total 0"), f"Here some files, {item} FAIL"
            checkout_clean.append(iter_step[0])
        assert all(checkout_clean), "test9 FAIL"
