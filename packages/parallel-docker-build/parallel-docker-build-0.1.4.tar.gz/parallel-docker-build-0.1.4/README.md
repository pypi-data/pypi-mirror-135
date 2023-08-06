# parallel-docker-build

Docker image building workflow tool with options for concurrent builds. This
tool was developed after writing similar `make`, `bash` and `python` scripts to
accomplish `docker build` pipelines. The objectives for this tool are:

1. Provide a single cmd line tool for flexible docker image building in repos
   with multiple images.
1. Allow parallel/concurrent builds of these images.
1. Allow image building pipelines to be defined in yaml instead of a bash script
   or Makefile with sequences of commands.

The expected folder structure is as follows:

1. Docker files all begin with `Dockerfile`
1. Docker files build images which name comes from the parent directory.
1. If a `Dockerfile` has suffixes (i.e. `myimage/Dockerfile.focal.x86`) the
   suffixes will be appended to the image name: `myimage_focal_x86`.
1. The suffixes allow multiple `Dockerfiles` to be defined for an image. This
   can be useful for multiple OS, arch, etc.
1. The `build` context is controllable so files can be `COPY`'d to the image
   from locations of your choice. NOTE that if the `Dockerfile` is not within
   the context, an error will be raised.

## Install

```bash
pip3 install parallel-docker-build
```

## Usage

There are two options for building images. Both have global options:

```bash
parallel-docker-build --help
# usage: parallel-docker-build [-h] [-r] [-q] {workflow,dockerfiles} ...

# Utility for building/tagging/pushing docker images.

# optional arguments:
#   -h, --help            show this help message and exit
#   -r, --rebuild         Rebuild with --no-cache option
#   -q, --quiet           Suppress stdout

# mode:
#   {workflow,dockerfiles}
#                         Mode of specifying a build.
```

### Command line args

The first option allows you to specify Dockerfiles or directories containing
Dockerfiles which will be found recursively. This mode is intended to build a
collection of docker files sequentially (--max_num_workers=1) or in parallel
with a max number of works fixed to half of your `cpu_count` from
`multiprocessing`.

```bash
parallel-docker-build dockerfiles --help
# usage: parallel-docker-build dockerfiles [-h] -o ORGANIZATION [-c CONTEXT] [-x] [-p] [-n MAX_NUM_WORKERS] paths [paths ...]

# positional arguments:
#   paths                 Docker image filenames(s) or directories to search.

# optional arguments:
#   -h, --help            show this help message and exit
#   -o ORGANIZATION, --organization ORGANIZATION
#                         Organization for images.
#   -c CONTEXT, --context CONTEXT
#                         Build context. By default the current directory.
#   -x, --allow_cross_platform
#                         Allow cross platform (x86 vs aarch64) building. Default is False.
#   -p, --push            Run docker push on the latest tag. Default is False.
#   -n MAX_NUM_WORKERS, --max_num_workers MAX_NUM_WORKERS
#                         Maximum number of build workers. If >1 multiprocessing is used. Max value is half this computer's cpu count: 64. Default is 1.
```

### Workflow file (yaml)

The second option allows you to specify a workflow file which contains the
options for the `dockerfiles` mode in addition to multiple "stages" which
allow you to build groups of docker images sequentially as if calling
`parallel-docker-build dockerfiles ...` sequentially. It also allows version
control of a workflow to build your images in a multi-image repo.

```bash
parallel-docker-build workflow --help
# usage: parallel-docker-build workflow [-h] workflow

# positional arguments:
#   workflow    Path to workflow yaml file image filenames(s).

# optional arguments:
#   -h, --help  show this help message and exit
```

## TODO

* Add example workflow file
* finish CLI for relative list of docker files
* tagging configuration
* tests
