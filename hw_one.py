import subprocess
import string


def run_command_and_check(command: str, search_text: str, split_words: bool = False) -> bool:
    """
    Executes a given shell command, checks if the specified text is in the output, and returns the result.

    This function takes a command string, executes it in the shell, and checks if the specified text is present in
    the command's output.
    Optionally, it can split the output into words by removing punctuation.

    :param command: main command to use
    :param search_text: text for check
    :param split_words: True or False for splitting text in result or not
    :return: True if the command executed successfully and the text is found in its output, otherwise False.
    """
    result = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if split_words:
        for i in string.punctuation:
            if i in out:
                out = out.replace(i, ' ')
    print(out)
    if search_text in out and result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    print(run_command_and_check('cat /etc/os-release', 'Minotaur', True))
