FROM lambci/lambda:build-python3.8

ENV ODBCINI=/opt/odbc.ini
ENV ODBCSYSINI=/opt/

# unixODBCのダウンロードとインストール
RUN curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo && \
    yum -y install unixODBC-devel && \
    curl ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.9.tar.gz -O && \
    tar xzvf unixODBC-2.3.9.tar.gz && \
    cd unixODBC-2.3.9 && \
    ./configure --sysconfdir=/opt --disable-gui --disable-drivers --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE --prefix=/opt && \
    make && \
    make install && \
    cd .. && \
    rm -rf unixODBC-2.3.7 unixODBC-2.3.7.tar.gz

## MSSQL 17のODBCドライバをダウンロード、インストール
RUN yum -y install e2fsprogs.x86_64 0:1.43.5-2.43.amzn1 fuse-libs.x86_64 0:2.9.4-1.18.amzn1 libss.x86_64 0:1.43.5-2.43.amzn1 && \
    ACCEPT_EULA=Y yum -y install msodbcsql17 && \
    export CFLAGS="-I/opt/include" && \
    export LDFLAGS="-L/opt/lib" && \
    cd /opt && \
    cp -r /opt/microsoft/msodbcsql17/ . && \
    rm -rf /opt/microsoft/

COPY odbc.ini /opt/odbc.ini

# ドライバーのパス指定を実際の構成に合うよう書き換え
RUN sed -i -e 's/Driver=\/opt\/microsoft/Driver=\/opt/' /opt/odbcinst.ini

# pyodbcパッケージをインストール
RUN mkdir /opt/python && \
    pip install pyodbc -t /opt/python

# Lambda LayerモジュールとしてZIP圧縮
RUN cd /opt && zip -r /opt/lambda-layer.zip ./*
