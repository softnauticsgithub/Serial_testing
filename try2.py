import subprocess
import os
import logging
import sys
from openai import OpenAI
import time
import re

# Configure OpenAI client
client = OpenAI(api_key="sk-proj-2By770zviWsreq3LW7fDGkfGTaTOKYJT"
                        "-ljdUvR0fGvbkaMju9G00dWHEET3BlbkFJjDPJFC1edC9Lnbat6qWXpmZo3mNk_B1jiWyC5Tf-DY447H9qVwk0wOKOsA")

# Configure logging
logging.basicConfig(filename="Code_Formatting_logs.log", level=logging.INFO, format="%(message)s")


def format_python_code(file_path):
    """Formats Python code using autopep8."""
    result = subprocess.run(["autopep8", "--in-place", file_path], shell=True, capture_output=True, text=True)
    return result


def check_code_with_flake8(file_path):
    """Checks Python code with flake8."""
    result = subprocess.Popen(["flake8",
        file_path
    ], stdout=subprocess.PIPE, text=True, shell=True)
    stdout = result.communicate()
    return stdout


def update_code_using_openai(file_path):
    """Updates Python code using OpenAI API to correct and format the code."""
    with open(file_path, "r") as file:
        original_code = file.read()

    prompt = ("Correct the provided Python code for any errors and format it strictly according to flake8 and pylint"
              "standards. Make the following modifications:\n"
              "1. Add module-level docstrings.\n"
              "2. Add docstrings for all functions and methods.\n"
              "3. Convert all naming conventions to snake_case.\n"
              "4. remove unused imports.\n"
              "5. Disable pylint's 'invalid-name' rule for the entire module with 'pylint: disable=invalid-name'.\n"
              "Provide only the modified code, without any additional text.\n"
              f"Code:\n{original_code}\n"
              )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=1024,
        temperature=0.2,
        stream=True
    )
    time.sleep(10)
    updated_code = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            updated_code += chunk.choices[0].delta.content

    cleaned_code = updated_code.replace("```python", "").replace("```", "")
    with open(file_path, "w+") as file:
        file.write(cleaned_code)


def main(changed_files):
    """Processes only the changed Python files."""
    for file_path in changed_files:
        if file_path.endswith(".py") and os.path.exists(file_path):
            logging.info(f"Processing file: {file_path}")
            print(file_path)

            # Check for Flake8 issues
            flake8_result = check_code_with_flake8(file_path)
            logging.info(f"Flake8 suggestions before update:\n{flake8_result[0]}")

            # Update code using OpenAI
            update_code_using_openai(file_path)
            time.sleep(10)

            # Format the code using autopep8
            logging.info("Formatting the code using autopep8...")
            format_python_code(file_path)

            # Re-check for Flake8 issues
            flake8_result = check_code_with_flake8(file_path)
            logging.info(f"Flake8 issues after update:\n{flake8_result[0]}")

            # Run pylint
            pylint_result = subprocess.Popen(["pylint",
                file_path
            ], stdout=subprocess.PIPE, text=True, shell=True)
            stdout = pylint_result.communicate()
            print(stdout)
            # logging.info(re.split(r'-{2,}', stdout[0])[1])
            # logging.info("--------------------------------------------------------------------------------------")


if __name__ == "__main__":
    changed_files = sys.argv[1:]
    if changed_files:
        main(changed_files)
