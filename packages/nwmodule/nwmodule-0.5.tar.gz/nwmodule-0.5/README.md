## __Neural Wrappers :: NWModule__

### __Description__:

A generic high level API on top of `torch.nn.module`. Implements faster training pipelines, adding callbacks (model saving, plots), model testing, metrics etc.

### __How to install__:

1. Pip

```
pip install nwmodule
```

2. Manual (for code tweaking and development)

Clone & Add the path to the root directory of this project in PYTHONPATH environment variable.

```
git clone https://gitlab.com/neuralwrappers/nwmodule /path/to/nwmodule
vim ~/.bashrc
(append at end of file)
export PYTHONPATH="$PYTHONPATH:/path/to/nwmodule/
```

### __Structure of this project__:
- README.md - This file
- examples/ - Some examples on how to use the library
	- tutorials/ - Basic tutorials on how to use the library
- nwmodule/ - Core implementation
- test/ - Unit tests. To run use `python -m pytest .` inside the directory.
