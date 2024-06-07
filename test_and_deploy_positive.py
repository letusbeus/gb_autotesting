from sshcheckers import ssh_checkout, ssh_getout, upload_or_download_files, data


class TestPositiveSsh:

    @staticmethod
    def save_log(starttime, name):
        """
        fixture for making stats log in log file, which announced in config.yaml
        :return:
        """
        with open(name, "a+", encoding="utf-8") as f:
            f.write(ssh_getout(data['host'], data['user'], data['passwd'], f"journalctl --since '{starttime}'", ""))

    def test_step1(self, start_time):
        """
        uploading files and installing program with check for successful deployment
        :return:
        """
        res = []
        upload_or_download_files(data['host'], data['user'], data['passwd'], f"/home/mantis/Downloads/{data['pocket_name']}.deb",
                                 f"/home/user2/{data['pocket_name']}.deb")
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"echo {data['passwd']} | sudo -S dpkg -i /home/{data['user']}/{data['pocket_name']}.deb",
                                f"Setting up {data['pocket_name']}"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'], f"echo {data['passwd']} | sudo -S dpkg -s {data['pocket_name']}",
                                "Status: install ok installed"))
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test1 FAIL"

    def test_step2(self, start_time, make_folders, clear_folders, make_files, stat_log):
        """
        test Add files to archive for ssh connecting user
        :param start_time:
        :param make_folders:
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = [ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2",
                            "Everything is Ok"),
               ssh_checkout(data['host'], data['user'], data['passwd'], f"ls {data['folder_out']}",
                            f"arx2.{data['arx_type']}")]
        print(res)
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test2 FAIL"

    def test_step3(self, start_time, inst_crc32, clear_folders, make_files, stat_log):
        """
        test check hash sum with CRC32 and 7z h on ssh connecting user
        :param start_time:
        :param inst_crc32:
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = []
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], f"cd {data['folder_in']}; 7z h {item}",
                                    "Everything is Ok"))
            hash_date_crc32 = str(ssh_getout(data['host'], data['user'], data['passwd'],
                                             f"cd {data['folder_in']}; crc32 {item}", "")).upper()
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'], f"cd {data['folder_in']}; 7z h {item}",
                                    hash_date_crc32))
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test3 FAIL"

    def test_step4(self, start_time, clear_folders, make_files, stat_log):
        """
        test List contents of archive on ssh connecting user
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = [ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2",
                            "Everything is Ok")]
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                    f"cd {data['folder_out']}; 7z l arx2.{data['arx_type']}", item))
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test4 FAIL"

    def test_step5(self, start_time, clear_folders, make_files, stat_log):
        """
        test Extract files from archive (without using directory names) ssh connecting user
        :param clear_folders:
        :param make_files:
        :param stat_log:
        :return:
        """
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx2",
                                "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"cd {data['folder_out']}; 7z e arx2.{data['arx_type']} -o{data['folder_ext']} -y",
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                    f"ls {data['folder_ext']}", item))
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test5 FAIL"

    def test_step6(self, start_time, clear_folders, make_files, make_subfolder, stat_log):
        """
        test eXtract files with full paths ssh connecting user
        :param clear_folders:
        :param make_files:
        :param make_subfolder:
        :param stat_log:
        :return:
        """
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"cd {data['folder_in']}; 7z a -t{data['arx_type']} {data['folder_out']}/arx",
                                "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"cd {data['folder_out']}; 7z x arx.{data['arx_type']} -o{data['folder_ext2']} -y",
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                    f"ls {data['folder_ext2']}", item))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"ls {data['folder_ext2']}", make_subfolder[0]))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"ls {data['folder_ext2']}", make_subfolder[0]))
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test6 FAIL"

    def test_step7(self, start_time, stat_log):
        """
        Test integrity of archive ssh connecting user
        :param stat_log:
        :return:
        """
        self.save_log(start_time, data['log_txt'])
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_out']}; 7z t arx.{data['arx_type']}",
                            "Everything is Ok"), "test7 FAIL"

    def test_step8(self, start_time, stat_log):
        """
        test Update files to archive ssh connecting user
        :param stat_log:
        :return:
        """
        self.save_log(start_time, data['log_txt'])
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_in']}; 7z u arx.{data['arx_type']}",
                            "Everything is Ok"), "test8 FAIL"

    def test_step9(self, start_time , stat_log):
        """
        test Delete files from archive ssh connecting user
        :param stat_log:
        :return:
        """
        self.save_log(start_time, data['log_txt'])
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_out']}; 7z d arx.{data['arx_type']}",
                            "Everything is Ok"), "test9 FAIL"

    def test_step10(self, start_time, clear_folders, stat_log):
        """
        delite all files in folders and check it ssh connecting user
        :param clear_folders:
        :param stat_log:
        :return:
        """
        res = [data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']]
        checkout_clean = []
        for item in res:
            iter_step = ssh_checkout(data['host'], data['user'], data['passwd'],
                                     f"cd {item}; ls -l", "total 0"), f"Here some files, {item} FAIL"
            checkout_clean.append(iter_step[0])
        self.save_log(start_time, data['log_txt'])
        assert all(checkout_clean), "test10 FAIL"

    def test_step11(self, start_time, clear_folders, stat_log):
        """
        Removing uninstalling program with check for successful deployment
        :return:
        """
        res = [ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"echo {data['passwd']} | sudo -S dpkg -r {data['pocket_name']}", "Removing", ),
               ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"echo {data['passwd']} | sudo -S dpkg -s {data['pocket_name']}",
                            "Status: deinstall ok")]
        self.save_log(start_time, data['log_txt'])
        self.save_log(start_time, data['log_txt'])
        assert all(res), "test11 FAIL"
