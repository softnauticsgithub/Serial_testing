import subprocess
import os
import logging
import time
from openai import OpenAI

# Configure logging
logging.basicConfig(
    filename="Code_Formatting_logs.log",
    level=logging.INFO,
    format="%(message)s"
)

client = OpenAI(api_key="sk-proj-2By770zviWsreq3LW7fDGkfGTaTOKYJT"
                        "-ljdUvR0fGvbkaMju9G00dWHEET3BlbkFJjDPJFC1edC9Lnbat6qWXpmZo3mNk_B1jiWyC5Tf-DY447H9qVwk0wOKOsA")


def get_modified_python_files():
    """Returns a list of Python files modified in the latest commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True
    )
    modified_files = [file.strip() for file in result.stdout.split("\n") if file.endswith(".py")]
    return modified_files


def format_python_code(file_path):
    """Formats Python code using autopep8."""
    subprocess.run(["autopep8", "--in-place", file_path], shell=True)


def update_code_using_openai(file_path):
    """Uses OpenAI to correct and format the code."""
    with open(file_path, "r") as file:
        original_code = file.read()

    prompt = (
        "Correct the provided Python code for any errors and format it strictly according to flake8 and pylint "
        "standards. Make the following modifications:\n"
        "1. Add module-level docstrings.\n"
        "2. Add docstrings for all functions and methods.\n"
        "3. Convert all naming conventions to snake_case.\n"
        "4. Remove unused imports.\n"
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
    with open(file_path, "w") as file:
        file.write(cleaned_code)


def main():
    """Main function to process only modified Python files."""
    modified_files = get_modified_python_files()

    if not modified_files:
        logging.info("No modified Python files detected.")
        return

    for file_path in modified_files:
        logging.info(f"Processing file: {file_path}")
        print(f"Processing {file_path}...")

        update_code_using_openai(file_path)
        format_python_code(file_path)

        logging.info(f"Updated file: {file_path}")


if __name__ == "__main__":
    main()
