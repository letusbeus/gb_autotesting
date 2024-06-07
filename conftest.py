from datetime import datetime

import pytest
import random
import string
import yaml

from sshcheckers import data, ssh_checkout, take_data


@pytest.fixture()
def start_time():
    """
    fixture for showing time
    :return:
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    """
    fixture for making folders
    :return:
    """
    return ssh_checkout(data['host'], data['user'], data['passwd'],
                        f"mkdir {data['folder_original']} {data['folder_in']} {data['folder_in']} {data['folder_out']} {data['folder_ext']} {data['folder_ext2']}",
                        "")


@pytest.fixture()
def clear_folders():
    """
    fixture for clearing folders
    :return:
    """
    return ssh_checkout(data['host'], data['user'], data['passwd'],
                        f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/* {data['folder_ext2']}/*",
                        "")


@pytest.fixture()
def make_files():
    """
    fixture for making files
    :return:
    """
    list_of_files = []
    for i in range(data['files_count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data['host'], data['user'], data['passwd'],
                        f"cd {data['folder_in']}; dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock",
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    """
    fixture for making subfolders
    :return:
    """
    test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    sub_folder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data['host'], data['user'], data['passwd'], f"cd {data['folder_in']}; mkdir {sub_folder_name}",
                        ""):
        return None, None
    if not ssh_checkout(data['host'], data['user'], data['passwd'],
                        f"cd {data['folder_in']}/{sub_folder_name}; dd if=/dev/urandom of={test_file_name} bs={data['bs']} count=1 iflag=fullblock",
                        ""):
        return sub_folder_name, None
    else:
        return sub_folder_name, test_file_name


@pytest.fixture(autouse=True)
def show_time():
    """
    fixture for showing time
    :return:
    """
    print(f"Start time: {datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')}")
    yield print(f"Stop time: {datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')}")


@pytest.fixture()
def make_broke_file():
    """
    fixture for making broke files
    :return:
    """
    ssh_checkout(data['host'], data['user'], data['passwd'], f"cd {data['folder_in']}; "
                                                             f"7z a -t{data['arx_type']} "
                                                             f"{data['folder_out']}/{data['arx_name']}",
                 "Everything is Ok")
    ssh_checkout(data['host'], data['user'], data['passwd'],
                 f"truncate -s 1 {data['folder_out']}/{data['arx_name']}.{data['arx_type']}", "")
    yield f"{data['arx_name']}"
    ssh_checkout(data['host'], data['user'], data['passwd'],
                 f"rm -f {data['folder_out']}/{data['arx_name']}.{data['arx_type']}", "")


@pytest.fixture()
def stat_log():
    """
    fixture for making stats log in log file, which announced in config.yaml
    :return:
    """
    with open(f"{data['log_check_txt']}", "a+", encoding="utf-8") as l:
        log_string = (f"Время: {datetime.now().strftime('%H:%M:%S.%f')}, Кол-во файлов: {data['files_count']}, "
                      f"Размер файлов: {data['bs']}, Загрузка процессора: {take_data('cat /proc/loadavg')} \n")
        yield l.write(log_string)


@pytest.fixture()
def inst_crc32():
    """
    fixture for making folders
    :return:
    """
    ssh_checkout(data['host'], data['user'], data['passwd'], f"echo {data['passwd']} | "
                                                             f"sudo apt-get -y install node-crc32", "")
    print("crc32 onstalled")
