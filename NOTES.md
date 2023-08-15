# Notes

Some general notes and guidelines.

## Release checklist

What to do when creating a new release:

- [ ] adjust version in `setup.cfg`
- [ ] update readme if necessary
- [ ] rebuild python package: `python -m build`
- [ ] edit `CHANGELOG.md`:
    - [ ] add release notes for version (at the top)
    - [ ] add link to version comparison (at the bottom)
- [ ] update docs if necessary
- [ ] commit
- [ ] tag commit: `git tag -a 'vX.X.X' -m "Version X.X.X <summary>"`
- [ ] push to Github: `git push origin --tags`
- [ ] add Github release and upload build files
- [ ] push package to pypi: `twine upload dist/<new-version>*`
- [ ] rebuild and redeploy docs if necessary
