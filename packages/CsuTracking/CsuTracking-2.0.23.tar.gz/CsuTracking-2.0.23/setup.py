from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="CsuTracking",  # 这里是pip项目发布的名称
    version="2.0.23",  # 版本号，数值大的会优先被pip
    keywords=("pip", "Tracking"),
    # description="An feature extraction algorithm",
    # long_description="An feature extraction algorithm, improve the FastICA",
    license="MIT Licence",

    # url="https://github.com/LiangjunFeng/SICA",  # 项目相关文件地址，一般是github
    author="CSU_YWJ",
    # author_email="zhumavip@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["CsuSort==1.0.14"]  # 这个项目需要的第三方库
)
