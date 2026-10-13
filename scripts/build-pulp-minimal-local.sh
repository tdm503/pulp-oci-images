#!/usr/bin/env bash
set -euo pipefail

# Run from the repository root. This script does not modify images/compose.
cd "$(dirname "$0")/.."

TAG="${PULP_LOCAL_TAG:-local}"
BASE_TAG="${PULP_BASE_TAG:-latest}"

echo "Building pulp/base:${BASE_TAG}"
docker build --pull=false \
  -f images/Containerfile.core.base \
  -t "pulp/base:${BASE_TAG}" \
  .

echo "Building pulp/pulp-minimal:${TAG}"
docker build --pull=false \
  --build-arg "FROM_TAG=${BASE_TAG}" \
  -f images/pulp-minimal/stable/Containerfile.core \
  -t "pulp/pulp-minimal:${TAG}" \
  .

echo "Built: pulp/pulp-minimal:${TAG}"
echo "To export: docker save -o pulp-minimal-${TAG}.tar pulp/pulp-minimal:${TAG}"
