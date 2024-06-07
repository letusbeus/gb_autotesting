import paramiko
import subprocess
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def ssh_checkout(host, user, passwd, cmd, text, check_type='positive', port=22):
    """
    ssh_check ssh host using paramiko
    :param check_type: positive or negative checkout
    :param host:
    :param user:
    :param passwd:
    :param cmd:
    :param text:
    :param port:
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port,)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    try:
        if check_type == 'positive':
            if text in out and exit_code == 0:
                return True
            else:
                return False
        if check_type == 'negative':
            if text in out and exit_code != 0:
                return True
            else:
                return False
    except ValueError:
        raise Exception(print('check_type key must be: positive or negative'))


def ssh_getout(host, user, passwd, cmd, text, port=22):
    """
    return get out data from ssh host using paramiko
    :param host:
    :param user:
    :param passwd:
    :param cmd:
    :param text:
    :param port:
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port,)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    return out


def upload_or_download_files(host, user, passwd, local_path, remote_path, upl_or_down='upload', port=22):
    """
    upload or download files ssh host using paramiko
    :param upl_or_down: key 'upload' or 'download' for upload or download
    :param host:0.0.0.0 or another
    :param user:
    :param passwd:
    :param local_path:
    :param remote_path:
    :param port:
    :return:
    """
    print(f"Upload file: {local_path}, to the path: {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        if upl_or_down == 'upload':
            sftp.put(local_path, remote_path)
        if upl_or_down == 'download':
            sftp.get(remote_path, local_path)
    except ValueError:
        raise Exception(print('upl_or_down key must be: upload or download'))
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def take_data(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    return result.stdout
