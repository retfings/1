from scihub_cn.scihub import SciHub
sh = SciHub()
# 设置is_translate_title可将paper's title进行翻译后下载存储
result = sh.download({"doi": '10.1109/ACC.1999.786344'})



# data = open("sci-hub-doi-2022-02-12.txt",encoding='utf-8',errors='ignore').readlines()


# 88343822
# ['10.1086/284248\n', '10.14233/ajchem.2014.15859\n', '10.1152/jn.2000.84.1.558\n', '10.1140/epjb/e2018-90281-7\n', '10.1007/s00204-017-2048-0\n']

# print(len(data))
# print(data[-5:])