"""Wrappers around the `requests <https://pypi.org/project/requests/>`_ library."""

import requests
from pathlib import Path
from typing import Union


def download(url: str, output_file: Union[Path, str], overwrite: bool = True) -> None:
    """Gets the file from the ``url`` and saves it as ``output_file``.

    :param url: The URL of the file to retrieve.
    :param output_file: The path to which to save the file upon retrieval.
    :param overwrite: If ``True``, existing files are overwritten silently.
    :raises: :class:`RuntimeError` if file retrieval fails.
    :raises: :class:`FileExistsError` if ``overwrite`` is ``False`` and ``output_file`` exists.
    :raises: :class:`IsADirectoryError` if ``output_file`` is a directory.
    :raises: :class:`OSError` if the parent directory to ``output_file`` does not exist.
    """

    if not isinstance(url, str):
        raise TypeError(f"Expected type 'string' for URL but got '{type(url)}.")
    if len(url) < 1:
        raise ValueError("URL cannot be an empty string.")

    if not isinstance(output_file, (Path, str)):
        raise TypeError(f"Expected type 'Path' or 'string' for output_file but got '{type(output_file)}.")
    if len(str(output_file)) < 1:
        raise ValueError("Output file path cannot be an empty string.")

    if not isinstance(overwrite, bool):
        raise TypeError(f"Expected type 'bool' for overwrite parameter but got '{type(overwrite)}'.")

    output_file = Path(output_file).expanduser().resolve()
    if not output_file.parent.exists():
        raise OSError(f"Parent directory does not exist: '{output_file.parent}")
    if output_file.is_dir():
        raise IsADirectoryError(f"Cannot create file '{output_file}': is a directory.")
    if not overwrite and output_file.exists():
        raise FileExistsError(f"File exists: '{output_file}")

    try:
        response = requests.get(url)
        if not response.status_code == 200:
            raise Exception(f"server returned {response.status_code}: {response.reason}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve '{url}': {e}")

    if output_file.exists():
        output_file.unlink()
    with open(output_file, 'wb') as file:
        file.write(response.content)
