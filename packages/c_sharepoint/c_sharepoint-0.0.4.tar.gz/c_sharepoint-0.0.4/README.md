

### 使用说明



##### 配置环境

```python
from c_sharepoint import Share_Point

# 初始化类库
# base_url包含网站集,最后结尾无/
# site 是站点名称
share_point=Share_Point(base_url,username,password,site)

```

##### 创建文件夹

```python
# 在【/filearchive/FBAttArchive/test】下创建 【testa】文件夹
folder_path="/filearchive/FBAttArchive/test"
folder_name="testa"
folder_path=share_point.create_folder(folder_path,folder_name)
```

##### 上传文件

```python
# 将【aaa.xlsx】上传到 目录【/filearchive/FBAttArchive/test/testa】下，并命名为 test.xlsx
with open("aaa.xlsx", "rb") as file:
    content=file.read()

file_name="test.xlsx"
folder_path="/filearchive/FBAttArchive/test/testa"
file_path=share_point.file_upload(folder_path,file_name,content)
print(file_path)
# 返回file_path：文件路径：【/filearchive/FBAttArchive/test/testa/test.xlsx】

```

##### 设置权限

```python
# 获取用户ID
user_id=share_point.get_user_id("域\用户名")
# 获取站点所在网站集权限级别列表
role_dict=share_point.get_role_list()
# 获取【完全控制】的role_id
role_id=role_dict['完全控制']

# 如果是文件夹
folder_path="/filearchive/FBAttArchive/test/testa"
uri=share_point.get_floder_uri(folder_path)
# 赋权之前先打断继承
share_point.breakroleinheritance(uri)
# 用户以【完全控制】角色赋予文件夹【"/filearchive/FBAttArchive/test/testa"】的权限
share_point.add_permission(user_id,role_id,uri)

# 如果是文件,用get_file_uri获取资源的uri
file_path="/filearchive/FBAttArchive/test/testa/test.xlsx"
uri=share_point.get_file_uri(file_path)
```

##### 下载文件
```python

#从【"/filearchive/FBAttArchive/test/testa/test.xlsx"】下载文件
file_path="/filearchive/FBAttArchive/test/testa/test.xlsx"
content=share_point.download_file(file_path)

#将文件存入filename
with open(filename, "wb") as f:
    f.write(content)

```