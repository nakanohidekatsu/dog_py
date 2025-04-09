from sqlalchemy import create_engine
# import sqlalchemy

import os
# uname() error回避
import platform
print("nakano:platform:", platform.uname())


main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
engine = create_engine("sqlite:///CRM.db", echo=True)
