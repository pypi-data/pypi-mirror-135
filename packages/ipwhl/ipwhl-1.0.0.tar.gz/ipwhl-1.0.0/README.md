# Floating cheeses utilities

## Prerequisites

The utilities depend on two Python libraries, [packaging] and [tomli].
Whilst the CI for the metadata installs these from IPWHL, one should
obtain them via the most convenient and maintainable way for local development.

## Usage

### Generators

```sh
ipwhl-prefix [PROJECT]...               # calculate path prefix for projects
ipwhl-declgen SRC DEST                  # generate declaration from wheel URL
ipwhl-publish SRC DEST                  # publish to IPFS MFS
```

### Checkers

```sh
ipwhl-nameck DIR                        # check declaration files organization
ipwhl-declck < paths-to-declarations    # check declarations' content
ipwhl-depsck DIR < supported-platforms  # check dependencies satisfaction
```

### Shared libraries

The following modules are internal API and can change without notice:

* ipwhl.deps: wrappers around packaging requirements and specifiers
* ipwhl.misc: miscellaneous helpers
* ipwhl.tags: high-level handling of wheel tags

## Contributing

Patches must pass the checks run by `tox` and should be sent to
[~cnx/ipwhl-devel@lists.sr.ht] using [`git send-email`][git-send-email],
with the following configurations:

    git config sendemail.to '~cnx/ipwhl-devel@lists.sr.ht'
    git config format.subjectPrefix 'PATCH ipwhl-utils'

## Copying

![AGPLv3](https://www.gnu.org/graphics/agplv3-155x51.png)

These programs are free software: you can redistribute them and/or modify them
under the terms of the GNU [Affero General Public License][agplv3] as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

[packaging]: https://packaging.pypa.io
[tomli]: https://pypi.org/project/tomli
[~cnx/ipwhl-devel@lists.sr.ht]: https://lists.sr.ht/~cnx/ipwhl-devel
[git-send-email]: https://git-send-email.io
[agplv3]: https://www.gnu.org/licenses/agpl-3.0.html
