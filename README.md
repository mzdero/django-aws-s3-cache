# Django AWS S3 Cache Backend

A Django cache backend implementation that uses Amazon AWS S3 as the storage backend. This backend stores cache items as JSON in an S3 bucket, with each item including an expiry timestamp. Items are retrieved from the cache only if they haven't expired. Expired items remain in the bucket and are not automatically deleted by this backend.

## Installation

Install the package via pip:

```sh
pip install django-aws-s3-cache
```

## Configuration

In your Django settings, define the CACHES and point to the S3 backend class. It can be used as the only cache or alongside other cache backends.

### Using S3 as the Default Cache

```python
CACHES = {
    "default": {
        "BACKEND": "django_aws_s3_cache.S3CacheBackend",
        "LOCATION": "S3_CACHE_BUCKET_NAME",
        "OPTIONS": {
            "BUCKET_NAME": "your-s3-bucket-name",
        }
    }
}
```

### Using S3 Alongside Other Caches

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
    },
    "s3": {
        "BACKEND": "django-aws-s3-cache.S3CacheBackend",
        "LOCATION": S3_CACHE_BUCKET_NAME,
    }
}
```

## Example Usage

Here's how to use the S3 cache in your Django application:

```python
from django.core.cache import caches

# Access the S3 cache
s3_cache = caches["s3"]

# Set a value in the cache
s3_cache.set("my_key", "my_value", timeout=60*15)  # 15 minutes

# Get a value from the cache
value = s3_cache.get("my_key")

# Delete a value from the cache
s3_cache.delete("my_key")

# Clear the entire cache
s3_cache.clear()
```

### Using the Default Cache
If you have configured the S3 cache as the default cache, you can use it directly from the cache module:

```python
from django.core.cache import cache

# Set a value in the cache
cache.set("my_key", "my_value", timeout=60*15)  # 15 minutes

# Get a value from the cache
value = cache.get("my_key")

# Delete a value from the cache
cache.delete("my_key")

# Clear the entire cache
cache.clear()
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
