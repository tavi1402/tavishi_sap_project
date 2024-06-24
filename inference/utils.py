from google.cloud import storage

storage_client = storage.Client()

def get_latest_model_version_from_gcs(bucket_name, model_name):
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f"models/{model_name}_")
    version_numbers = [
        int(blob.name.split(f"{model_name}_v")[1].split('.')[0]) for blob in blobs
    ]
    latest_version = max(version_numbers, default=None)
    return latest_version

def download_model_from_gcs(bucket_name, gcs_path, local_model_path):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.download_to_filename(local_model_path)