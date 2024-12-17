# Notes

Some general notes and guidelines.

## Developing on NixOS

On NixOS, an attempt to create a venv locally and running `pip install -r requirements.txt` will fail, because
some of the pulled in pip wheels will attempt to compile the `cffi` package.
This requires the `libcffi` C library to be linked during the build, causing pip to fail on NixOS.

To fix this, use the provided `shell.nix`, which will pull in the required library and make it available in the
created venv. You have to delete your existing `.venv` folder if it is present:

```bash
rm -rf .venv
nix-shell
```

## Release checklist

What to do when creating a new release:

- [ ] adjust version in `setup.cfg`
- [ ] update readme if necessary
- [ ] edit `CHANGELOG.md`:
    - [ ] add release notes for version (at the top)
    - [ ] add link to version comparison (at the bottom)
- [ ] update docs if necessary
- [ ] rebuild python package: `python -m build`
- [ ] commit
- [ ] tag commit: `git tag -a 'vX.X.X' -m "Version X.X.X <summary>"`
- [ ] push to Github: `git push origin --tags`
- [ ] add Github release and upload build files
- [ ] push package to pypi: `twine upload dist/hyprpy-<new-version>*`
    - if using API: username `__token__` and password `<API-TOKEN>`
- [ ] rebuild and redeploy docs if necessary
