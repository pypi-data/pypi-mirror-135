## Masonite package sync

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/masonite-package-sync">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
  <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/girardinsamuel/masonite-package-sync?include_prereleases">
  <img src="https://img.shields.io/github/license/girardinsamuel/masonite-package-sync.svg" alt="License">
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Update a masonite package with latest project template files.
It's useful when you maintain a package to update the project template used for example in tests/integrations/.

```
pip install masonite-package-sync
```

Pull the default Masonite project template into the current directory

```
python masonite-package pull
```

```
python masonite-package pull --repo johndoe/other-project --branch develop
```

```
python masonite-package pull --directory other/dir/test/
```

If you want to update the test project inside your Masonite package do :

```
python masonite-package pull --directory tests/integrations/
```

It will replace the project and update paths to work !
