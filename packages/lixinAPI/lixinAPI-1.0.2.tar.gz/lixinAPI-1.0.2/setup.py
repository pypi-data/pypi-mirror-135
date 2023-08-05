from setuptools import setup
import setuptools
# setup(
#     name='ressetAPI',# 需要打包的名字,即本模块要发布的名字
#     version='v0.9.0',#版本
#     description='A  module for test', # 简要描述
#     py_modules=['lixinapi',],   #  需要打包的模块
#     author='zhangq', # 作者名
#     author_email='569535175@qq.com',   # 作者邮件
#     url='https://github.com/vfrtgb158/email', # 项目地址,一般是代码托管的网站
#     # requires=['requests','urllib3'], # 依赖包,如果没有,可以不要
#     license='MIT'
# )
setup(
    name="lixinAPI",
    version="1.0.2",
    author="zhangq",
    author_email="569535175@qq.com",
    description="A small example package",
    url="https://github.com/PepperPapa/xinNotes",
    packages=setuptools.find_packages(),
    install_requires=[ 'requests'],
)

#python setup.py sdist bdist_wheel
#twine upload dist/*