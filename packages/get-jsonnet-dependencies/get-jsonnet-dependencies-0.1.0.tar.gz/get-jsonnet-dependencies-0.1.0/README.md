# get-jsonnet-dependencies

Extracts import dependencies from a Jsonnet file

## Usage

```sh
> pip install get-jsonnet-dependencies
> get-jsonnet-dependencies -
> local thing = import "thing.jsonnet";
thing.jsonnet
> local amoguise = import @"C:\Users\sus\Documents\amoguise.libsonnet";
C:\Users\sus\Documents\amoguise.libsonnet
> local a = import "a.jsonnet"; local b = importstr "b.txt";
a.jsonnet
b.txt
```

Pass a list of files to extract dependencies from

Passing - means to take extract dependencies from stdin

No arguments means `get-jsonnet-dependencies -`

Note that imports spanning multiple lines won't be found by this script
