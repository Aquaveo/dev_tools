"""Script to generate files for building Conan 2 libraries from templates using TOML data."""
# 1. Standard python modules
import argparse
from pathlib import Path

# 2. Third party modules
from jinja2 import Template
import toml  # Could use `import tomllib` if Python 3.11+


def render_template_with_toml(toml_file_path: str, template_dir: str, output_dir: str = None):
    """
    Render templates with the data contained in a single TOML file.

    Args:
        toml_file_path (str): Path to the TOML file.
        template_dir (str): Path to the directory containing template files.
        output_dir (str, optional): Directory to store rendered output files. If not provided,
                                    output files are stored in the same directory as the TOML file.
    """
    toml_file = Path(toml_file_path)
    template_dir = Path(template_dir)

    # Default output_dir to the directory of the TOML file if not specified
    output_dir = Path(output_dir) if output_dir else toml_file.parent

    if not toml_file.exists():
        raise FileNotFoundError(f"The specified TOML file does not exist: {toml_file_path}")

    # Parse the TOML file into a dictionary
    toml_content = toml_file.read_text()
    toml_data = toml.loads(toml_content)

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all template files in the specified template directory
    template_files = list(template_dir.glob("*.jinja"))
    if not template_files:
        raise FileNotFoundError(
            f"No template files (with .jinja extension) were found in the directory: {template_dir}")

    # Iterate through each template file and render it with TOML data
    for template_file in template_files:
        # Read the template content
        template_content = template_file.read_text()

        # Load the template with Jinja2
        template = Template(template_content, keep_trailing_newline=True)

        # Render the template with the TOML data
        rendered_content = template.render(toml_data)

        # Determine the output file name (strip `.jinja` extension)
        output_file_name = template_file.stem  # Use `stem` to get the filename without the `.jinja` extension

        # Write the rendered content directly to the output directory
        output_file = output_dir / output_file_name
        output_file.write_text(rendered_content)

    print(f"Templates rendered successfully using the TOML file: {toml_file_path}")


def main():
    parser = argparse.ArgumentParser(description="Render templates using a single TOML file.")
    parser.add_argument("--template_dir", default="templates", help="Directory containing template files.")
    parser.add_argument("--output_dir", default=None,
                        help="Directory to store rendered output files. Defaults to the TOML file's directory if not specified.")
    parser.add_argument("toml_file", help="Path to the required TOML file (always the last argument).")

    args = parser.parse_args()

    try:
        render_template_with_toml(
            toml_file_path=args.toml_file,
            template_dir=args.template_dir,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
