"""
S3 Storage integration module for raw JSON/CSV payload staging and cloud backup.

Supports AWS S3 via boto3 with seamless fallback to local S3 bucket emulation
when AWS credentials or cloud services are not configured.
"""

import json
import os
from typing import Any, Dict, List, Optional
import pandas as pd

from logger import logger

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


class S3Client:
    """Client for uploading and retrieving raw tourism datasets to S3 or local bucket staging."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        region_name: Optional[str] = None,
        local_dir: str = "data/s3_bucket",
    ):
        self.bucket_name = bucket_name or os.getenv(
            "S3_BUCKET_NAME", "greek-tourism-raw-bucket"
        )
        self.local_dir = local_dir
        os.makedirs(self.local_dir, exist_ok=True)

        self.s3 = None
        if BOTO3_AVAILABLE:
            access_key = aws_access_key or os.getenv("AWS_ACCESS_KEY_ID")
            secret_key = aws_secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")
            region = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
            endpoint_url = os.getenv("S3_ENDPOINT_URL")  # LocalStack / MinIO support

            if access_key and secret_key:
                try:
                    self.s3 = boto3.client(
                        "s3",
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        region_name=region,
                        endpoint_url=endpoint_url,
                    )
                    logger.info(
                        f"Initialized S3 Client for bucket '{self.bucket_name}'"
                    )
                except Exception as e:
                    logger.warning(
                        f"Failed to initialize boto3 S3 client: {e}. Falling back to local storage."
                    )

    def upload_raw_json(
        self, data: List[Dict[str, Any]], key: str = "raw/tourism_data.json"
    ) -> str:
        """Uploads raw JSON API payload to S3 or local bucket.

        Args:
            data: List of dict raw API records.
            key: Target object key path in bucket.

        Returns:
            str: Location path or URI of stored object.
        """
        payload = json.dumps(data, indent=2, ensure_ascii=False)

        if self.s3:
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=payload.encode("utf-8"),
                    ContentType="application/json",
                )
                s3_uri = f"s3://{self.bucket_name}/{key}"
                logger.info(f"Successfully uploaded JSON data to S3: {s3_uri}")
                return s3_uri
            except (BotoCoreError, ClientError) as e:
                logger.warning(f"S3 upload failed: {e}. Storing locally.")

        # Local bucket fallback
        local_path = os.path.join(self.local_dir, key.replace("/", "_"))
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(payload)
        logger.info(f"Raw JSON stored in local bucket fallback at: {local_path}")
        return local_path

    def upload_raw_csv(
        self, df: pd.DataFrame, key: str = "raw/tourism_data.csv"
    ) -> str:
        """Uploads raw CSV payload to S3 or local bucket.

        Args:
            df: Dataframe of raw records.
            key: Target object key path in bucket.

        Returns:
            str: Location path or URI of stored object.
        """
        csv_buffer = df.to_csv(index=False)

        if self.s3:
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=csv_buffer.encode("utf-8"),
                    ContentType="text/csv",
                )
                s3_uri = f"s3://{self.bucket_name}/{key}"
                logger.info(f"Successfully uploaded CSV data to S3: {s3_uri}")
                return s3_uri
            except (BotoCoreError, ClientError) as e:
                logger.warning(f"S3 upload failed: {e}. Storing locally.")

        local_path = os.path.join(self.local_dir, key.replace("/", "_"))
        df.to_csv(local_path, index=False, encoding="utf-8")
        logger.info(f"Raw CSV stored in local bucket fallback at: {local_path}")
        return local_path

    def download_raw_json(
        self, key: str = "raw/tourism_data.json"
    ) -> List[Dict[str, Any]]:
        """Downloads raw JSON API payload from S3 or local bucket.

        Args:
            key: Object key path.

        Returns:
            List[Dict[str, Any]]: Parsed JSON list.
        """
        if self.s3:
            try:
                response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
                content = response["Body"].read().decode("utf-8")
                return json.loads(content)
            except Exception as e:
                logger.warning(f"Failed to fetch from S3: {e}. Attempting local read.")

        local_path = os.path.join(self.local_dir, key.replace("/", "_"))
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                return json.load(f)

        logger.error(f"Raw JSON object not found at {key} or {local_path}")
        return []


def upload_to_s3(
    data: List[Dict[str, Any]], df: Optional[pd.DataFrame] = None
) -> Dict[str, str]:
    """Convenience helper to stage raw JSON and CSV into S3 bucket.

    Args:
        data: List of raw dictionaries.
        df: Optional dataframe representation.

    Returns:
        Dict[str, str]: Map of uploaded locations.
    """
    client = S3Client()
    json_path = client.upload_raw_json(data)
    results = {"json_path": json_path}

    if df is not None and not df.empty:
        csv_path = client.upload_raw_csv(df)
        results["csv_path"] = csv_path
    return results
