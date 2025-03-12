
"""This script formats and updates Python code using autopep8, flake8, and OpenAI's model.

It processes Python files by:
1. Checking for flake8 issues.
2. Updating code using OpenAI Assistant.
3. Formatting code with autopep8.
"""

import subprocess
import os
import sys
import time
from openai import OpenAI

# pylint: disable=invalid-name

# Configure OpenAI client
client = OpenAI(api_key="sk-proj-2By770zviWsreq3LW7fDGkfGTaTOKYJT"
                        "-ljdUvR0fGvbkaMju9G00dWHEET3BlbkFJjDPJFC1edC9Lnbat6qWXpmZo3mNk_B1jiWyC5Tf-DY447H9qVwk0wOKOsA")

assistant_id = "asst_ohjld2zq70yjwOqIDCBIvWHM"

def format_python_code(file_path):
    """Formats Python code using autopep8.

    Args:
        file_path (str): Path to the Python file to format.

    Returns:
        subprocess.CompletedProcess: The result of the autopep8 formatting command.
    """
    result = subprocess.run(["autopep8", "--in-place", file_path], shell=True, capture_output=True, text=True)
    return result


def check_code_with_flake8(file_path):
    """Checks Python code with flake8.

    Args:
        file_path (str): Path to the Python file to check.

    Returns:
        tuple: The stdout and stderr output from the flake8 check.
    """
    result = subprocess.Popen([
        r"flake8 --extend-ignore E501,W292,E302,F841,F401,F821", file_path
    ], stdout=subprocess.PIPE, text=True, shell=True)
    stdout = result.communicate()
    return stdout


def update_code_using_openai(file_path):
    """Updates Python code using OpenAI Assistant.

    Args:
        file_path (str): Path to the Python file to update.

    """
    with open(file_path, "r") as file:
        original_code = file.read()

    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""
            Don't update comment if already added\n
            Code:\n
            {original_code}
        """
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while run.status not in ["completed", "failed"]:
        time.sleep(10)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        updated_code = messages.data[0].content[0].text.value  # Extract AI response
        cleaned_code = updated_code.replace("```python", "").replace("```", "")

        with open(file_path, "w") as file:
            file.write(cleaned_code)


def main(changed_files):
    """Processes only the changed Python files.

    Args:
        changed_files (list): List of file paths to process.
    """
    for file_path in changed_files:
        if file_path.endswith(".py") and os.path.exists(file_path):
            flake8_result = check_code_with_flake8(file_path)
            print((f"Flake8 suggestions before update:\n{flake8_result[0]}"))

            update_code_using_openai(file_path)
            time.sleep(3)

            print("Formatting the code using autopep8...")
            format_python_code(file_path)

            flake8_result = check_code_with_flake8(file_path)
            print((f"Flake8 suggestions after update:\n{flake8_result[0]}"))


if __name__ == "__main__":
    changed_files = sys.argv[1:]
    if changed_files:
        main(changed_files)
