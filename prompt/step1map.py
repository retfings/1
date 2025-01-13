from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable
import warnings
from sqlalchemy import exc

# 忽略 SAWarning 警告
warnings.filterwarnings("ignore", category=exc.SAWarning)
# 远程数据库连接信息
remote_db_url = 'mysql+pymysql://root@10.10.104.25:9030/cdm'
remote_engine = create_engine(remote_db_url)

# 创建 MetaData 对象并绑定引擎
metadata = MetaData()
metadata.bind = remote_engine

# 反射数据库表结构
metadata.reflect(bind=remote_engine)

# 创建会话
Session = sessionmaker(bind=remote_engine)
remote_session = Session()

# 打开本地 SQL 文件
with open('output.sql', 'w', encoding='utf-8') as sql_file:
    try:
        # 遍历所有表
        for table_name, table in metadata.tables.items():
            # 导出表结构
            create_table_sql = str(CreateTable(table).compile(remote_engine))
            sql_file.write(f"-- 表结构: {table_name}\n")
            sql_file.write(f"{create_table_sql};\n\n")

            # 导出数据
            sql_file.write(f"-- 数据: {table_name}\n")
            result = remote_session.query(table).all()
            for row in result:
                # 生成 INSERT 语句
                columns = ', '.join(table.columns.keys())
                values = ', '.join(repr(getattr(row, col)) for col in table.columns.keys())
                insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
                sql_file.write(f"{insert_sql}\n")

            sql_file.write("\n")  # 表之间留空行

        print("数据已成功导出到 output.sql 文件！")

    except Exception as e:
        print(f"导出过程中发生错误: {e}")
    finally:
        # 关闭会话
        remote_session.close()