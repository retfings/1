from fabric import Connection

def backup_remote_mysql_with_fabric(ssh_host, ssh_user, ssh_password, mysql_user, mysql_password, database, output_file):
    try:
        # 创建 SSH 连接
        conn = Connection(host=ssh_host, user=ssh_user, connect_kwargs={'password': ssh_password})

        # 在远程服务器上执行 mysqldump 命令
        dump_command = f"mysqldump -u{mysql_user} -p{mysql_password} {database}"
        result = conn.run(dump_command, hide=True)

        # 将备份内容写入本地文件
        with open(output_file, 'w') as f:
            f.write(result.stdout)

        print(f"备份成功！文件已保存到 {output_file}")
    except Exception as e:
        print(f"备份失败: {e}")

# 示例调用
backup_remote_mysql_with_fabric(
    ssh_host='10.10.104.25',  # 远程服务器地址
    ssh_user='root',  # SSH 用户名
    ssh_password='',  # SSH 密码
    mysql_user='root',  # 数据库用户名
    mysql_password='',  # 数据库密码
    database='cdm',  # 数据库名称
    output_file='backup.sql'  # 本地备份文件路径
)