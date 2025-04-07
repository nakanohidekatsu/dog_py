from sqlalchemy import create_engine

import os
from dotenv import load_dotenv
from pathlib import Path

# 環境変数の読み込み

base_path = Path(__file__).parents[1]
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# load_certs = os.environ.get("WEBSITE_LOAD_CERTIFICATES", None)
# ssl_args = {}

# if load_certs :
#     # 複数指定されている場合は先頭のサムプリントを使用
#     thumbprint = load_certs.split(",")[0].strip()
    # Azure App Service の Linux コンテナ内で証明書は /var/ssl/certs/<サムプリント>.pem として配置される
#     cert_file = f"/var/ssl/certs/{thumbprint}.pem"
#     ssl_args["ssl"] = {"ca": cert_file}
# else:
#     ssl_args["ssl"] = {"ca": "/var/ssl/certs/DigiCertGlobalRootCA.crt.pem"}

# データベース接続情報
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_SERVER')
DB_PORT = os.getenv('MYSQL_DB_PORT')
DB_NAME = os.getenv('MYSQL_DB')

ssl_cert = str('DigiCertGlobalRootCA.crt.pem')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("nakano DATABASE_URL:",DATABASE_URL)

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl":{
            "ssl_ca":ssl_cert
        }
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

