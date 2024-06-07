from sshcheckers import ssh_checkout, ssh_getout, upload_or_download_files, data


class TestNegativeSsh:

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
        upload_or_download_files(data['host'], data['user'], data['passwd'],
                                 f"/home/mantis/Downloads/{data['pocket_name']}.deb",
                                 f"/home/user2/{data['pocket_name']}.deb")
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"echo {data['passwd']} | "
                                f"sudo -S dpkg -i /home/{data['user']}/{data['pocket_name']}.deb",
                                f"Setting up {data['pocket_name']}"))
        res.append(ssh_checkout(data['host'], data['user'], data['passwd'],
                                f"echo {data['passwd']} | sudo -S dpkg -s {data['pocket_name']}",
                                "Status: install ok installed"))
        self.save_log(start_time, data['log_txt_negative'])
        assert all(res), "test1 FAIL"

    def test_negative_step2(self, start_time, make_folders, clear_folders, make_broke_file, stat_log):
        """
        est Extract files from archive (without using directory names) using ssh connecting user
        :param start_time:
        :param make_folders:
        :param clear_folders:
        :param make_broke_file:
        :param stat_log:
        :return:
        """

        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_out']}; 7z e {data['arx_name']}.{data['arx_type']} "
                            f"-o{data['folder_ext']} -y", "ERROR", "negative"), "test2 FAIL"

    def test_negative_step3(self, start_time, clear_folders, make_broke_file, stat_log):
        """
        test eXtract files with full paths using ssh connecting user
        :param clear_folders:
        :param make_broke_file:
        :param stat_log:
        :return:
        """
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_out']}; "
                            f"7z x {data['arx_name']}.{data['arx_type']} -o{data['folder_ext']} -y",
                            "ERROR", "negative"), "test3 FAIL"

    def test_negative_step4(self, start_time, clear_folders, make_broke_file, stat_log):
        """
        Test integrity of archive using ssh connecting user
        :param clear_folders:
        :param make_broke_file:
        :param stat_log:
        :return:
        """
        assert ssh_checkout(data['host'], data['user'], data['passwd'],
                            f"cd {data['folder_out']}; 7z t {data['arx_name']}.{data['arx_type']}",
                            "ERROR", "negative"), "test4 FAIL"

    def test_step5(self, start_time, clear_folders, stat_log):
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
        assert all(res), "test5 FAIL"
