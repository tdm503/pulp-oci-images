# Build `pulp-minimal` for an intranet

This fork already contains the upstream build definitions. Its CI builds the images in the following order:

1. `images/Containerfile.core.base` -> `pulp/base:latest`
2. `images/pulp-minimal/stable/Containerfile.core` -> `pulp/pulp-minimal:local`

## Build on a machine with dependencies available

Run from the repository root:

```bash
bash scripts/build-pulp-minimal-local.sh
docker image inspect pulp/pulp-minimal:local
```

The build uses `quay.io/centos/centos:stream10`, `ghcr.io/astral-sh/uv:0.11.7`, RPM repositories, Python package indexes, and additional dependencies. **This is not an air-gapped build recipe.** `--pull=false` only avoids explicitly refreshing the base image; Docker and package-manager downloads may still be necessary. For an isolated network, build on an approved connected worker or provide an internal mirror for *all* dependencies.

## Transfer the result to the intranet

On the build machine (use the same CPU architecture as the destination):

```bash
docker save -o pulp-minimal-local.tar pulp/pulp-minimal:local
sha256sum pulp-minimal-local.tar > pulp-minimal-local.tar.sha256
```

Transfer both files using approved channels.

On the target machine:

```bash
sha256sum -c pulp-minimal-local.tar.sha256
docker load -i pulp-minimal-local.tar
docker image inspect pulp/pulp-minimal:local
```

Then override the `image:` references for all Pulp services in your Compose stack to `pulp/pulp-minimal:local`. The Pulp webserver has a separate `pulp/pulp-web` image; this script does not build that image.

## Option: publish to an internal Docker registry

```bash
docker tag pulp/pulp-minimal:local REGISTRY_HOST/pulp/pulp-minimal:local
docker login REGISTRY_HOST
docker push REGISTRY_HOST/pulp/pulp-minimal:local
```

Replace `REGISTRY_HOST` with the actual Docker registry endpoint; it is not necessarily the Nexus web UI URL.

## Security and local Git state

Never commit `.env`, `.env.s3`, database passwords, encryption keys, or Django `SECRET_KEY`. The `compose-s3-test` directory in local working copies may contain secrets and an unfinished rebase; it is **not** included in this build feature.

If your local Git checkout is mid-rebase, inspect `git status` and finish or abort that rebase before switching branches. Do not run `git push --force` to resolve a rebase conflict.
