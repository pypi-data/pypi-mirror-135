# lord kelvin

EVM interface

## Quickstart:

- to just build the docker image, type:

```/bin/bash
make dbuild
```

- to run tests, type:

```/bin/bash
make -C tools
```

- or to use a specific ganache port:

```/bin/bash
PORT=1234 make -C tools
```

- to run tests, then get a shell, type:

```/bin/bash
make -C tools sh
```

- or to use a specific ganache port:

```/bin/bash
PORT=1234 make -C tools sh
```

## Using different networks

- Only `ganache` and `kovan` are supported

- To add a network:

- - add a new `env.{NEWORK}.sh` file to tools

- - add a new alias in `tools/aliases`

### Inside docker

- your life is easy, just type the name of the network!

- Examples:

```/bin/bash
ganache
```

```/bin/bash
kovan
```

### Outside docker

- to use ganache (the default), type:

```/bin/bash
source env.sh
```

- to use kovan, type:

```/bin/bash
source env.kovan.sh
```
