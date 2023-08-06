# formbox

This tiny script formats an [mbox] as HTML or XML.  It is intended
for rendering email replies on websites and their [RSS] feed.

## Prerequisites

This Python package depends on [bleach] for HTML sanitising
and [markdown] for, well, rendering Markdown to HTML.  It is, however,
not designed to work with HTML emails with all those CSS and Java scripts.

## Installation

It is recommended to install this package from a downstream repository,
such as [Nix] or [IPWHL].

## Usage

```console
$ formbox --help
usage: formbox [-h] mbox id template

format mbox as HTML/XML

positional arguments:
  mbox        path to mbox file
  id          root message ID
  template    path to template

optional arguments:
  -h, --help  show this help message and exit
```

## Copying

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[mbox]: https://en.wikipedia.org/wiki/Mbox
[RSS]: https://www.rssboard.org
[bleach]: https://bleach.readthedocs.io
[markdown]: https://python-markdown.github.io
[Nix]: https://search.nixos.org/packages?channel=unstable&query=formbox
[IPWHL]: https://man.sr.ht/~cnx/ipwhl
