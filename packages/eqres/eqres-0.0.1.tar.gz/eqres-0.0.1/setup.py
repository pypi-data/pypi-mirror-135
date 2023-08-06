from setuptools import setup, find_packages
import eqres

"""
项目打包
python setup.py bdist_egg     # 生成类似 eqres-0.0.1-py2.7.egg，支持 easy_install 
# 使用此方式
python setup.py sdist         # 生成类似 eqres-0.0.1.tar.gz，支持 pip
# twine 需要安装
twine upload dist/eqres-0.0.1.tar.gz
"""

setup(
    name=eqres.__name__,
    version=eqres.__version__,
    keywords=("pip", "eqres", "response", "return"),
    description="response tool",
    long_description="response tool",
    license="MIT Licence",

    url="https://github.com/enqiangjing/eqres.git",
    author="eq",
    author_email="eq_enqiang@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
