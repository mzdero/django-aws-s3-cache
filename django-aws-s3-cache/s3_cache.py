import hashlib
import json
import time

from django.core.cache.backends.base import BaseCache
from django.utils.encoding import force_bytes

import boto3


class S3CacheBackend(BaseCache):
    """
    Simplified S3 cache backend implementation. Uses a separate bucket with a
    lifecycle policy and supports expiration. Doesn't delete expired objects.
    """

    def __init__(self, bucket, params):
        super().__init__(params)
        self.bucket_name = bucket
        self.client = boto3.client("s3")

    def make_key(self, key, version=None):
        key = super().make_key(key, version)
        return hashlib.md5(force_bytes(key)).hexdigest()

    def add(self, raw_key, value, timeout=None, version=None):
        if self.get(raw_key, version=version) is None:
            self.set(raw_key, value, timeout, version)
            return True
        return False

    def get(self, raw_key, default=None, version=None):
        key = self.make_key(raw_key, version)
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.loads(response["Body"].read())
            if data["expiry"] and data["expiry"] < time.time():
                self.delete(raw_key, version=version)
                return default
            return data["value"]
        except self.client.exceptions.NoSuchKey:
            return default

    def set(self, raw_key, value, timeout=None, version=None):
        key = self.make_key(raw_key, version)
        expiry = time.time() + timeout if timeout else None
        data = {
            "value": value,
            "expiry": expiry,
        }
        self.client.put_object(
            Bucket=self.bucket_name, Key=key, Body=json.dumps(data)
        )

    def delete(self, raw_key, version=None):
        key = self.make_key(raw_key, version)
        self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def clear(self):
        paginator = self.client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name)

        delete_us = dict(Objects=[])
        for item in pages.search("Contents"):
            delete_us["Objects"].append(dict(Key=item["Key"]))

            # Flush once we hit 1000 keys
            if len(delete_us["Objects"]) >= 1000:
                self.client.delete_objects(
                    Bucket=self.bucket_name, Delete=delete_us
                )
                delete_us = dict(Objects=[])

        # Flush the final batch
        if len(delete_us["Objects"]):
            self.client.delete_objects(
                Bucket=self.bucket_name, Delete=delete_us
            )

    def touch(self, raw_key, timeout=None, version=None):
        key = self.make_key(raw_key, version)
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.loads(response["Body"].read())
            if data["expiry"] and data["expiry"] < time.time():
                self.delete(raw_key, version=version)
                return False
            data["expiry"] = time.time() + timeout if timeout else None
            self.client.put_object(
                Bucket=self.bucket_name, Key=key, Body=json.dumps(data)
            )
            return True
        except self.client.exceptions.NoSuchKey:
            return False
