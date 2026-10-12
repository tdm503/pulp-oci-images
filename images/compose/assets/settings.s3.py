SECRET_KEY = "aabbcc"
CONTENT_ORIGIN = "http://pulp_content:24816"
DATABASES = {"default": {"HOST": "postgres", "ENGINE": "django.db.backends.postgresql", "NAME": "pulp", "USER": "pulp", "PASSWORD": "password", "PORT": "5432", "CONN_MAX_AGE": 0, "OPTIONS": {"sslmode": "prefer"}}}
CACHE_ENABLED = True
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
ANSIBLE_API_HOSTNAME = "http://pulp_api:24817"
ANSIBLE_CONTENT_HOSTNAME = "http://pulp_content:24816/pulp/content"
ALLOWED_IMPORT_PATHS = ["/tmp"]
ALLOWED_EXPORT_PATHS = ["/tmp"]
TOKEN_SERVER = "http://pulp_api:24817/token/"
TOKEN_AUTH_DISABLED = False
TOKEN_SIGNATURE_ALGORITHM = "ES256"
PUBLIC_KEY_PATH = "/etc/pulp/keys/container_auth_public_key.pem"
PRIVATE_KEY_PATH = "/etc/pulp/keys/container_auth_private_key.pem"
ANALYTICS = False
STATIC_ROOT = "/var/lib/operator/static/"

# S3 artifact storage. Keep this file free of credentials.
import os

MEDIA_ROOT = ""
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ["AWS_STORAGE_BUCKET_NAME"],
            "region_name": os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-1"),
            "default_acl": "private",
            "signature_version": "s3v4",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# When clients cannot reach S3 directly, serve downloads via Pulp.
REDIRECT_TO_OBJECT_STORAGE = False
