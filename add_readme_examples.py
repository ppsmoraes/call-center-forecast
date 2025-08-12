import re
import sys
from io import StringIO


def capture_python_output(py_file):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            exec(f.read(), {'__name__': '__main__'})
    except Exception as e:
        print(f'Erro ao executar: {str(e)}')
    finally:
        sys.stdout = old_stdout

    return mystdout.getvalue()


def update_nth_output_block(md_file, output_text, n=1):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    parts = re.split(r'```output\n.*?\n```', md_content, flags=re.DOTALL)
    output_blocks = re.findall(r'```output\n.*?\n```', md_content, re.DOTALL)
    print(output_blocks)

    output_blocks[n - 1] = f'```output\n{output_text}\n```'

    updated_content = parts[0]
    for i in range(len(output_blocks)):
        updated_content += output_blocks[i] + parts[i + 1]

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)


def update_nth_python_block(py_file, md_file, n=1):
    with open(py_file, 'r', encoding='utf-8') as f:
        py_content = f.read()

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    parts = re.split(r'```python\n.*?\n```', md_content, flags=re.DOTALL)
    py_blocks = re.findall(r'```python\n.*?\n```', md_content, re.DOTALL)

    py_blocks[n - 1] = f'```python\n{py_content}\n```'

    updated_content = parts[0]
    for i in range(len(py_blocks)):
        updated_content += py_blocks[i] + parts[i + 1]

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)


if __name__ == "__main__":
    py_file = 'readme_exemples.py'
    md_file = 'README.md'

    output = capture_python_output(py_file)
    update_nth_python_block(py_file, md_file, 1)
    update_nth_output_block(md_file, output.strip(), 1)
