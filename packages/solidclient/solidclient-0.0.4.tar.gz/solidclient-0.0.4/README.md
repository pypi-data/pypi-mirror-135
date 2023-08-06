# Python Solid Client

A [Solid](https://solidproject.org/) client written in Python.

## Developing the module

We are using Python 3.8 on Ubuntu Focal for the development of this project.
Use the following commands to create a virtual environment.

```
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --require-hashes -r dev-requirements.txt
python3 -m pip install --require-hashes -r requirements.txt
```

### How to update any requirements?

Modify the corresponding requirements file, and then use the `pip-compile` tool
to regenerate the requirements files.

Example:

```
pip-compile --allow-unsafe --generate-hashes --output-file=requirements.txt requirements.in
```

## License

MIT
