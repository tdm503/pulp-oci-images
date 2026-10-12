# Local Pulp with Amazon S3

This is an opt-in Docker Compose override for artifact storage on Amazon S3. It does not change the upstream deployment.

## Requirements

- Docker Engine and Docker Compose v2; Git
- AWS S3 bucket with private access, IAM permissions `s3:ListBucket` and `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`.
- Network access from the Pulp containers to the S3 endpoint (HTTPS/443).
- `django-storages` and `boto3` installed in the Pulp images. **Check this first:** the stock upstream image may need to be extended.

## Configure

```bash
git clone https://github.com/tdm503/pulp-oci-images.git
cd pulp-oci-images/images/compose
cp .env.s3.example .env.s3
# edit .env.s3 with your bucket, region, and AWS credentials
docker run --rm --entrypoint python pulp/pulp-minimal:latest -c "import storages, boto3; print('S3 dependencies OK')"
docker compose -f compose.yml -f compose.s3.yml config --quiet
docker compose -f compose.yml -f compose.s3.yml up -d
docker compose -f compose.yml -f compose.s3.yml ps
```

If the dependency check fails, build an image based on `pulp/pulp-minimal` with compatible `django-storages[s3]`, then change the Pulp service image references. Avoid runtime `pip install` inside containers.

Check the API at `http://localhost:8080/pulp/api/v3/status/` and upload a test artifact. A successful status response alone does **not** verify S3 writes: check the bucket and download the artifact.

## Important notes

- `.env.s3` is ignored by Git, but credentials still need to be secured locally.
- `settings.s3.py` duplicates the upstream example settings to keep the override self-contained; reconcile changes after upstream updates.
- This proof-of-concept inherits upstream example passwords and is **not** production-ready.
- The Compose override replaces the `/etc/pulp/settings.py` bind-mount for each Pulp service, retaining other inherited volumes.
- If S3 credentials come from an IAM role, adapt `env_file` and credential provisioning accordingly.
- This configuration targets AWS S3, not an S3-compatible endpoint such as MinIO.
