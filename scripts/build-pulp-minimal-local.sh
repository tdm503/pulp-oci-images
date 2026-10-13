#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

TAG="${PULP_LOCAL_TAG:-local}"
BASE_TAG="${PULP_BASE_TAG:-latest}"
BASE_DOCKERFILE="${PULP_BASE_DOCKERFILE:-images/Containerfile.core.base}"

echo "Building pulp/base:${BASE_TAG} from ${BASE_DOCKERFILE}"
docker build \
  -f "${BASE_DOCKERFILE}" \
  -t "pulp/base:${BASE_TAG}" \
  .

echo "Building pulp/pulp-minimal:${TAG}"
docker build \
  --build-arg "FROM_TAG=${BASE_TAG}" \
  -f images/pulp-minimal/stable/Containerfile.core \
  -t "pulp/pulp-minimal:${TAG}" \
  .

echo "Built: pulp/pulp-minimal:${TAG}"
echo "Export: docker save -o pulp-minimal-${TAG}.tar pulp/pulp-minimal:${TAG}"
