# 带带弟弟小工具

1.功能

- 爬虫基类
- 爬虫基类2（selenium）
- mail
- ftp 下载；删除
- retry 重试器，只支持在类中使用
- mysql 操作类
---

2. 使用
    ```shell
    pip install -i https://pypi.org/simple/ dddd-utils
    ```

3. 打包
    ```shell
    python3 -m build

    python3 -m twine upload --repository testpypi dist/*
    
    python3 -m twine upload --repository pypi dist/*
    ```
