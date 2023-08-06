from setuptools import setup, find_packages

setup(
    name='uchida1512testpackage',
    version='1.0.0',

    # distutils が操作する Python パッケージのリスト
    packages=find_packages(),

    author='uchida1512',
    author_email='uchida1512@gmail.com',

    url='https://github.com/s3project2020/uchida1512_a-practical-introduction-to-python',

    description='This is a test package for uchida',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    python_requires='~=3.6',

    # PyPI 上での検索、閲覧のために利用されるカテゴリのリスト
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],

    # 依存しているパッケージのリスト
    install_requires=[
        'click~=7.0',


        # sampleproject をコミットを指定して取得（これは上手くいかなかった）
        # 'sampleproject@git+https://github.com/pypa/sampleproject#sha1=87c524aec9586b92932dc261923dc8686dcfa019',

        # なお、これ↓でも上手くいかない模様。アップロードはできるが、インストールができない。
        # 'sampleproject~=2.0',

    ],

    # pip install testpackage [ s3 (または gcs )] を実行すると、指定したものをインストールできる
    extras_require={
        's3': ['boto3~=1.10.0'],
        'gcs': ['google-cloud-storage~=1.23.0'],
    },

    # 設定ファイルや画像ファイルなどの Python モジュール以外のファイルを指定
    package_data={'testpackage': ['data/*']}
)