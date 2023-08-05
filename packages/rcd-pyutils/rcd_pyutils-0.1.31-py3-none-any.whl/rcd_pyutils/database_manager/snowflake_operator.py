import os
import snowflake.connector


class SnowflakeOperator:
    def __init__(self) -> None:
        self.snowflake_user = os.environ.get("SNOWFLAKE_USER")
        self.snowflake_password = os.environ.get("SNOWFLAKE_PASSWORD")
        self.snowflake_account = os.environ.get("SNOWFLAKE_ACCOUNT")

        self.conn = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account
        )

    def truncate(self, database, schema, table):
        sql = f"truncate table {database}.{schema}.{table} ;"
        self.conn.cursor().execute(sql)

    def copy(self, s3_prefix, s3_file, database, schema, table):
        self.conn.cursor().execute(f"""
        COPY INTO {database}.{schema}.{table} 
        FROM s3://{os.environ.get("S3_DATAMART_BUCKET")}/{s3_prefix}/{s3_file}
        CREDENTIALS = (
        aws_key_id='{os.environ.get("AWS_ACCESS_KEY_ID")}',
        aws_secret_key='{os.environ.get("AWS_SECRET_ACCESS_KEY")}'
        )
        FILE_FORMAT=(field_delimiter='|', SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"', NULL_IF=(''))
        FORCE = TRUE
        """)
