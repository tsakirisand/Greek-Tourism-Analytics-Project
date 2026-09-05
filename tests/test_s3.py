import os
import pandas as pd
from s3_client import S3Client, upload_to_s3



def test_s3_client_local_fallback(tmp_path):
    local_dir = os.path.join(tmp_path, "s3_test_bucket")
    client = S3Client(bucket_name="test-bucket", local_dir=local_dir)

    raw_data = [
        {
            "geo": "EL30",
            "geo_label": "Attica",
            "year": 2023,
            "hotels_total_arrivals": 1000,
        }
    ]
    df = pd.DataFrame(raw_data)

    json_path = client.upload_raw_json(raw_data, key="raw/test_data.json")
    csv_path = client.upload_raw_csv(df, key="raw/test_data.csv")

    assert os.path.exists(json_path)
    assert os.path.exists(csv_path)

    downloaded = client.download_raw_json(key="raw/test_data.json")
    assert len(downloaded) == 1
    assert downloaded[0]["geo"] == "EL30"


def test_upload_to_s3_helper(tmp_path):
    raw_data = [{"geo": "EL42", "geo_label": "South Aegean", "year": 2022}]
    df = pd.DataFrame(raw_data)

    res = upload_to_s3(raw_data, df)
    assert "json_path" in res
    assert "csv_path" in res
