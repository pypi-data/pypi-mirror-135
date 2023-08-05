""" This module implement data functionality  """
import json
import re
from typing import Dict
from typing import List
from typing import Optional

import boto3
import google
import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account as GCPServiceAccount

from superwise import Config
from superwise.controller.base import BaseController
from superwise.controller.exceptions import SuperwiseException
from superwise.controller.exceptions import SuperwiseStorageDownloadGCSError
from superwise.controller.exceptions import SuperwiseStorageDownloadS3Error
from superwise.controller.exceptions import SuperwiseStorageUploadGCSError
from superwise.controller.exceptions import SuperwiseValidationException
from superwise.models.transaction import Transaction


class TransactionController(BaseController):
    """Transaction Controller is in-charge for create transaction using file or batch request """

    def __init__(self, client, sw):
        """

        ### Args:

        `client`: superwise client object

        `sw`: superwise  object

        """
        super().__init__(client, sw)
        self.path = "gateway/v1/transaction"
        self.model_name = None
        _bucket_name = "superwise-{}-{}".format(self.client.tenant_id, Config.ENVIRONMENT)
        self._gcs_internal_bucket = self._create_gcs_bucket_connection(
            bucket_name=_bucket_name, service_account=self.client.service_account
        )

    def _create_gcs_bucket_connection(self, bucket_name, service_account):

        """
        ### Description:

        get connection to gcs bucket

        ### Args:

        `bucket_name`: gcs bucket name

        `service_account`: superwise service account object

        """
        try:
            self.logger.debug(f"Create connection to superwise bucket {bucket_name}")
            credentials = GCPServiceAccount.Credentials.from_service_account_info(service_account)
            gcs_client = storage.Client(credentials=credentials)
            return gcs_client.bucket(bucket_name)
        except Exception as e:
            self.logger.error(f"Error create connection to superwise bucket {bucket_name}")
            raise Exception(f"Error create connection to superwise bucket {bucket_name}")

    def _extract_directory(self, url: str):
        bucket = url.split("/")[2]
        prefix = "/".join(url.split("/")[3:])
        return bucket, prefix

    def _upload_string_to_internal_bucket(self, data, file_name):
        try:
            self.logger.debug(f"Upload file to superwise bucket {file_name}")
            blob = self._gcs_internal_bucket.blob(f"landing/{file_name}")
            blob.upload_from_string(data=data)
            return f"gs://{self._gcs_internal_bucket.name}/landing/{file_name}"
        except google.api_core.exceptions.Forbidden as e:
            if "does not have storage.objects.delete access" in e.message:
                self.logger.error(f"Failed upload file to superwise bucket because {file_name} already exist")
                raise SuperwiseStorageUploadGCSError(
                    f"Failed upload file to superwise bucket because {file_name} already exist"
                )
            raise SuperwiseStorageUploadGCSError(f"Failed upload file to superwise storage {file_name} with ext {e}")
        except Exception as e:
            self.logger.error(f"Failed upload file to superwise storage {file_name} with ext {e}")
            raise SuperwiseStorageUploadGCSError(f"Failed upload file to superwise storage {file_name} with ext {e}")

    def log_records(self, model_id: str, records: List[dict], version_id: Optional[str] = None):
        """
        ### Description:

        Send list of records

        ### Args:

        `model_id`:  string - model id

        `version_id`:  string - version id  of the model -   Optional[for prediction recor

        `records`:  List[dict] - list of records of data,  each record is a dict.

        `transaction_id`:  string - uuid of the log operation

        """

        self.logger.info(f"Send records with params : model_id={model_id}, version_id={version_id}")
        records_df = pd.DataFrame(records)
        records = json.loads(records_df.to_json(orient="records", date_format="iso"))
        payload = dict(records=records, model_id=model_id)
        if version_id is not None:
            payload["version_id"] = version_id
        r = self.client.post(self.build_url("{}".format(self.path + "/records")), payload)
        self.logger.info("file_log server response: {}".format(r.content))
        return r.json()

    def _create_s3_client(self, aws_access_key_id: str, aws_secret_access_key: str, role_arn: str):
        try:
            if role_arn is not None:
                self.logger.debug("Create S3 client from role_arn")
                sts_client = boto3.client("sts")
                assumed_role_object = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="superwise-session")
                credentials = assumed_role_object["Credentials"]

                return boto3.client(
                    "s3",
                    aws_access_key_id=credentials["AccessKeyId"],
                    aws_secret_access_key=credentials["SecretAccessKey"],
                    aws_session_token=credentials["SessionToken"],
                )
            elif aws_access_key_id is not None and aws_secret_access_key is not None:
                self.logger.debug("Create S3 client with aws access key and secret key")
                return boto3.client(
                    "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
                )

            else:
                self.logger.debug("Create s3 client with out any params")
                return boto3.client("s3")
        except Exception as e:
            self.logger.error(f"Error create s3 client, ext {e}")
            raise SuperwiseException("Error create s3 client - role arn or access and secret keys not provided")

    def log_from_s3(
        self,
        file_path: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        role_arn: Optional[str] = None,
    ):

        """
        ### Description:

        Upload file from s3 bucket to superwise bucket.</br>
        The permission for the client s3 bucket should be by providing aws_access_key_id and aws_secret_access_key or

        ### Args:

        `file_path`:  s3 url path

        `aws_access_key_id`:

        `aws_secret_access_key`: .

        `role_arn`:  AWS Role arn


        """
        if not str(file_path).startswith("s3://"):
            self.logger.error(f"Failed upload file to superwise storage {file_path}")
            raise Exception("file_path must start with 's3://'")
        try:
            self.logger.info("Download file {} from s3".format(file_path))
            bucket, key = self._extract_directory(file_path)
            s3_client = self._create_s3_client(
                aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, role_arn=role_arn
            )
            resp = s3_client.get_object(Bucket=bucket, Key=key)
            content = resp["Body"]
        except Exception as e:
            self.logger.error(f"Error download file from customer s3 bucket {file_path} with ext {e}")
            raise SuperwiseStorageDownloadS3Error(f"Error download file from customer s3 bucket {file_path}")
        superwise_file_path = self._upload_string_to_internal_bucket(data=content.read(), file_name=key)
        return self.log_file(file_path=superwise_file_path, _origin_path=file_path)

    def log_from_gcs(self, file_path: str, service_account: Dict):
        """
        ### Description:

        Upload file from gcs bucket to superwise bucket

        ### Args:

        `file_path`:  gcs file path

        `service_account`: dict of the service account.

        `transaction_id`: string - uuid of the log operation

        """

        if not str(file_path).startswith("gs://"):
            self.logger.error("Failed upload file to superwise storage")
            raise Exception("file_path must start with 'gs://'")
        self.logger.info("Download file {} from gcs".format(file_path))
        bucket, key = self._extract_directory(file_path)
        try:
            customer_bucket = self._create_gcs_bucket_connection(bucket, service_account)
            blob = customer_bucket.blob(key)
            data = blob.download_as_string()
        except Exception as e:
            self.logger.error(f"Error download file {file_path} from gcs with ext{e}")
            raise SuperwiseStorageDownloadGCSError(f"Error download file {file_path} from gcs")
        superwise_file_path = self._upload_string_to_internal_bucket(data=data, file_name=key)
        return self.log_file(file_path=superwise_file_path, _origin_path=file_path)

    def log_file(self, file_path: str, _origin_path: Optional[str] = None):

        """
        ### Description:

        Stream data of a given file path

        ### Args:

        `file_path`:  url for file stored in cloud str

        `transaction_id`: string - uuid of the log operation

        ### Return:

        json object  represent the transaction from server
        """

        self.logger.info(f"Log file {file_path}")
        pattern = "(s3|gs)://.+"
        if not re.match(pattern, file_path):
            raise SuperwiseValidationException(
                "transaction file failed because of wrong file path. file path should be gcs or s3 path."
            )
        params = {"file": file_path}
        if _origin_path is not None:
            params["origin_path"] = _origin_path
        r = self.client.post(url=self.build_url("{}".format(self.path + "/file")), params=params)
        self.logger.info("transaction file server response: {}".format(r.content))
        return r.json()

    def get(self, transaction_id: str):
        """
         ### Description:

         Get transaction by transaction id

         ### Args:

         `transaction_id`:  string - transaction_id to fetch from server

         ### Return:

         Transaction object
         """

        self.logger.info(f"Get transaction by transaction id {transaction_id}")
        response = self.client.get(
            url=self.build_url("{}".format("integration/v1/transactions" + f"/{transaction_id}"))
        )
        self.logger.info("transaction file server response: {}".format(response.content))
        transaction = self.parse_response(response, "Transaction", is_return_model=True)
        return transaction
