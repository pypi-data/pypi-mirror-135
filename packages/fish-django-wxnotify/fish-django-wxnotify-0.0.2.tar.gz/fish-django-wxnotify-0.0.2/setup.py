import setuptools

setuptools.setup(
    name="fish-django-wxnotify",
    version="0.0.2",
    author="DomineCore",
    author_email="Fengyafei0405@163.com",
    description="微信小程序发送通知",
    long_description="一个简单的 PyPI 上传测试",
    long_description_content_type="text/markdown",
    url="https://github.com/DomineCore/wxnotify",
    packages=setuptools.find_packages("fishwxnotify"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
