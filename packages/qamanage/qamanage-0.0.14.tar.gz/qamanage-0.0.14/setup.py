from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "qamanage",    #这里是pip项目发布的名称
    version = "0.0.14",    #版本号，数值大的会优先被pip，每次更新需要修改这个为更高的版本
    keywords = ("qamanage"),
    description = "A public script library",
    long_description = "Public Script Library of quality management department",
    license = "Apache License 2.0",

    url = "https://github.com/lin54241930/qamanage.git",     #项目相关文件地址，一般是github
    author = "Linxu",
    author_email = "lin54241930@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","opencv-python","requests"]          #这个项目需要的第三方库
)