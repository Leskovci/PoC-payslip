from azure.storage.blob import BlobServiceClient
from config import AZURE_CONNECTION_STRING
from io import BytesIO

CONTAINER_NAME = "payslipfiles"
INPUT_PREFIX = "inputfiles"
OUTPUT_PREFIX = "outputfiles"

blob_service = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)


def upload_input_blob(file_bytes, filename):
    try:
        blob_path = f"{INPUT_PREFIX}/{filename}"
        blob_client = blob_service.get_blob_client(CONTAINER_NAME, blob_path)
        blob_client.upload_blob(file_bytes, overwrite=True)
        print(f"[Azure] Uploaded INPUT: {blob_path}")
        return True
    except Exception as e:
        print(f"[Azure ERROR] Input upload failed: {e}")
        return False


def upload_output_blob(file_bytes, filename):
    try:
        blob_path = f"{OUTPUT_PREFIX}/{filename}"
        blob_client = blob_service.get_blob_client(CONTAINER_NAME, blob_path)
        blob_client.upload_blob(file_bytes, overwrite=True)
        print(f"[Azure] Uploaded OUTPUT: {blob_path}")
        return True
    except Exception as e:
        print(f"[Azure ERROR] Output upload failed: {e}")
        return False


def delete_blob(blob_path):
    try:
        blob_client = blob_service.get_blob_client(CONTAINER_NAME, blob_path)
        blob_client.delete_blob()
        print(f"[Azure] Deleted: {blob_path}")
        return True
    except Exception as e:
        print(f"[Azure ERROR] Delete failed: {e}")
        return False


def list_input_files():
    try:
        container = blob_service.get_container_client(CONTAINER_NAME)
        blobs = container.list_blobs(name_starts_with=f"{INPUT_PREFIX}/")
        return [b.name for b in blobs if not b.name.endswith("/")]
    except:
        return []


def list_output_files():
    try:
        container = blob_service.get_container_client(CONTAINER_NAME)
        blobs = container.list_blobs(name_starts_with=f"{OUTPUT_PREFIX}/")
        return [b.name for b in blobs if not b.name.endswith("/")]
    except:
        return []


def download_input_blob(blob_name):
    try:
        blob_client = blob_service.get_blob_client(CONTAINER_NAME, blob_name)
        return blob_client.download_blob().readall()
    except:
        return None


def read_input_blob(blob_name):
    try:
        blob_client = blob_service.get_blob_client(CONTAINER_NAME, blob_name)
        data = blob_client.download_blob().readall()
        return BytesIO(data)
    except:
        return None
