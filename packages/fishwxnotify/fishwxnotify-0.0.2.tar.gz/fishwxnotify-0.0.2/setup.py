import setuptools

setuptools.setup(
    name="fishwxnotify",
    version="0.0.2",
    author="DomineCore",
    author_email="Fengyafei0405@163.com",
    description="服务号发送通知",
    long_description="fishwxnotify用于向微信服务号发送模板消息等类型通知",
    long_description_content_type="text/markdown",
    url="https://github.com/DomineCore/wxnotify",
    packages=setuptools.find_packages("fishwxnotify"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
