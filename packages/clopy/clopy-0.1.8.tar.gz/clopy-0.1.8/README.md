# Clopy

General purpose templating program to quickly setup projects and files

## Usage

1. In a new directory create a `template.py` file
2. Prompt the user for input required for the Jinja template file
    using standard output
3. Render the input to the template file using `[template_name].render`
4. Write the output file to disk

## Templates Aliases

If you find that a path is too long to type out or that you always find yourself typing
out the path to a certain template file, you can alias it using the `~/.config/clopy/templates.json`
file. There's an example `templates.json` included in the root direct of the repository.
