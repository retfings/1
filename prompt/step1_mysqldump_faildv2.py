import subprocess

def backup_remote_mysql(host, port, user, database, output_file):
    try:
        # 构建 mysqldump 命令
        command = [
            'mysqldump',
            f'-h{host}',  # 远程数据库地址
            f'-P{port}',  # 远程数据库端口
            f'-u{user}',  # 数据库用户名
            database  # 数据库名称
        ]

        # 执行命令并将输出写入本地文件
        with open(output_file, 'w') as f:
            subprocess.run(command, stdout=f, check=True)

        print(f"备份成功！文件已保存到 {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"备份失败: {e}")

# 示例调用
backup_remote_mysql(
    host='10.10.104.25',  # 远程数据库地址
    port=9030,  # 远程数据库端口
    user='root',  # 数据库用户名
    database='cdm',  # 数据库名称
    output_file='backup.sql'  # 本地备份文件路径
)