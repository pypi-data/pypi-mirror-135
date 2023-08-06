# BasketCase
Fetch resources from Instagram.

It can download images and videos in their highest quality from any type of publication. You will need a session cookie to avoid rate limits and access controls.

## Installation and usage
1. Install it from [PyPI](https://pypi.org/project/basketcase/). The `--user` flag means it will be installed in your home directory.

```sh
pip install --user basketcase
```

> This will put the executable `basketcase` on your PATH.

2. Create a text file (e.g. `basketcase.txt`) and populate it with resource URLs:

```
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
```

3. Pipe the contents of the file to the script, optionally passing the session cookie.

```sh
cat basketcase.txt | basketcase -c session_cookie_id
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase_{timestamp}/`).

## Development setup
1. `cd` to the project root and create a virtual environment in a directory named `venv`, which is conveniently ignored in version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

3. Install this package in editable mode.

```sh
pip install -e .
```

### Package build and upload
1. Update the requirements list.

```sh
pip freeze --exclude-editable > requirements.txt
```

2. Increment the version on `setup.cfg`.
3. Build and upload to PyPI.

```sh
python -m build
python -m twine upload dist/*
```

4. Commit and push the changes (and the new version tag) to the git repository.

