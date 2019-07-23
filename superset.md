# 官方教程
[官方教程](https://superset.incubator.apache.org/)
1. 支持3.6版本以上的python（建议在新的虚拟环境中操作）  
2. 升级安装工具  
```
pip install –upgrade setuptools pip
```
3. 安装相应的库[requirement](./superset_requirement.txt)  
```
pip install -r requirements.txt
```
4. 安装superset  
```
pip install superset
```
5. 创建管理帐户
```
$ export FLASK_APP=superset
flask fab create-admin
```
6. 加载例子数据  
```
superset load_examples
```
7. 创建角色和权限
```
superset init
```
8. 开启superset
```
superset run -p 8080 --with-threads --reload --debugger
```
# 三方python包及连接url前缀

|Database|Package|SQLAlchemy URI prefix|
|  ----  | ----  | ----  |
|database|pypi package|SQLAlchemy URI prefix|
|MySQL|pip install mysqlclient|mysql://|
|Postgres|pip install psycopg2|postgresql+psycopg2://|
|Presto|pip install pyhive|presto://|
|Hive|pip install pyhive|hive://|
|Oracle|pip install cx_Oracle|oracle://|
|sqlite||sqlite://|
|Snowflake|pip install snowflake-sqlalchemy|snowflake://|
|Redshift|pip install sqlalchemy-redshift|redshift+psycopg2://|
|MSSQL|pip install pymssql|mssql://|
|Impala|pip install impyla|impala://|
|SparkSQL|pip install pyhive|jdbc+hive://|
|Greenplum|pip install psycopg2|postgresql+psycopg2://|
|Athena|pip install "PyAthenaJDBC>1.0.9"|awsathena+jdbc://|
|Athena|pip install "PyAthena>1.2.0"|awsathena+rest://|
|Vertica|pip install sqlalchemy-vertica-python|vertica+vertica_python://|
|ClickHouse|pip install sqlalchemy-clickhouse|clickhouse://|
|Kylin|pip install kylinpy|kylin://|
|BigQuery|pip install pybigquery|bigquery://|
|Teradata|pip install sqlalchemy-teradata|teradata://|
|Pinot|pip install pinotdb|pinot+http://controller:5436/ query?server=http://controller:5983/|

# 分享图表不需要登陆即可查看
+ /superset/config.py第127行
```
# ---------------------------------------------------
# Roles config
# ---------------------------------------------------
# Grant public role the same set of permissions as for the GAMMA role.
# This is useful if one wants to enable anonymous users to view
# dashboards. Explicit grant on specific datasets is still required.
PUBLIC_ROLE_LIKE_GAMMA = False
```
>将PUBLIC_ROLE_LIKE_GAMMA改为True，  
【注释意思】  
授予公共角色与GAMMA角色相同的权限集。  
如果想让匿名用户查看，可以设置这里  
在仪表盘对特定数据集的授权显示，也在这里设置。  
+ 加入数据库权限这里加入所有数据库权限  
>安全 👉 角色列表 👉 Public 👉 编辑记录  
>>can explore on Superset为导出图表  
can explore json on Superset为导出图表json  
all database access on all_database_access访问所有数据库权限，也可以设置单个  
  
# MAXBOX配置
+ 申请key  
[MAPBOX](https://account.mapbox.com/)
+ 修改superset配置(\superset\Lib\site-packages\superset\config.py)
```
# Set this API key to enable Mapbox visualizations
# MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY', '')
MAPBOX_API_KEY = 'pk.eyJ…'
```

#Error
## Error1
+ 运行 ```$ fabmanager create-admin --app superset 提示错误 Was unable to import superset Error: cannot import name 'quoted_name'```
+ 解决方案：  
```pip install -r requirements.txt```

## Error2
+ 提示
```
"Can't determine which FROM clause to join "
sqlalchemy.exc.InvalidRequestError: Can't determine which FROM clause to join from, there are multiple FROMS which can join to this entity. Try adding an explicit ON clause to help resolve the ambiguity.
```
+ 解决方案
```
pip install sqlalchemy==1.2.18
python superset db upgrad
```

## Error3
+ 提示   
```
(superset) [root@superset opt]# fabmanager create-admin --app superset
Username [admin]: admin
User first name [admin]: admin
User last name [user]: admin
Email [admin@fab.org]: admin@qq.com
Password:
Repeat for confirmation:
Was unable to import superset Error: cannot import name '_maybe_box_datetimelike'
```
+ 解决方案   
```
pip install pandas==0.23.4
```

## Error4
+ ```module ‘signal’ has no attribute 'SIGALRM'```
+ 解决方案：注释utils.py中类timeout函数的__enter__，并增加pass
```
class timeout(object):
"""
To be used in a ``with`` block and timeout its content.
"""

def __init__(self, seconds=1, error_message='Timeout'):
    self.seconds = seconds
    self.error_message = error_message

def handle_timeout(self, signum, frame):
    logging.error('Process timed out')
    raise SupersetTimeoutException(self.error_message)

def __enter__(self):
    try:
        # signal.signal(signal.SIGALRM, self.handle_timeout)
        # signal.alarm(self.seconds)
        pass
    except ValueError as e:
        logging.warning("timeout can't be used in the current context")
        logging.exception(e)

def __exit__(self, type, value, traceback):
    try:
        # signal.alarm(0)
        pass
    except ValueError as e:
        logging.warning("timeout can't be used in the current context")
        logging.exception(e)
```

## Error5
+ superset与redshift兼容性问题（由于redshift通过sql查询大写变成小写，导致pandas keyerror）  

+ 解决方案一：修改代码

```superset\viz.py```中的```get_data```函数
```
def get_data(self, df):
    if (
            self.form_data.get('granularity') == 'all' and
            DTTM_ALIAS in df):
        del df[DTTM_ALIAS]
    try:
        df = df.pivot_table(
            index=self.form_data.get('groupby'),
            columns=self.form_data.get('columns'),
            values=[self.get_metric_label(m) for m in self.form_data.get('metrics')],
            aggfunc=self.form_data.get('pandas_aggfunc'),
            margins=self.form_data.get('pivot_margins'),
        )
    except: #解决redshift查询后列名变小写的问题
        df = df.pivot_table(
            index=self.form_data.get('groupby'),
            columns=self.form_data.get('columns'),
            values=[self.get_metric_label(m).lower() for m in self.form_data.get('metrics')],
            aggfunc=self.form_data.get('pandas_aggfunc'),
            margins=self.form_data.get('pivot_margins'),
        )
    # Display metrics side by side with each column
    if self.form_data.get('combine_metric'):
        df = df.stack(0).unstack()
    return dict(
        columns=list(df.columns),
        html=df.to_html(
            na_rep='',
            classes=(
                'dataframe table table-striped table-bordered '
                'table-condensed table-hover').split(' ')),
    )
```

+ 解决方案2   
>[https://github.com/apache/incubator-superset/issues/5308](https://github.com/apache/incubator-superset/issues/5308)
+ 解决方案3   
>使用的时候在网页端生成字段 Datasource 👉 Metrics 👉 Label【使用小写的名字】

## Error6
+ ```Failed building wheel for sasl```
+ 解决方案
执行以下命令解决：
```sudo apt-get install libsasl2-dev```

## Error7
+ 问题
```
error: could not create 'build\bdist.win-amd64\wheel.\superset\static\assets\dist\vendors-deckgl\
layers\arc-deckgl\layers\geojson-deckgl\layers\grid-deckgl\layers\hex-deckgl\layers
\p-39b91eb9.81565bc93ff56be4e334.chunk.js': No such file or directory
```
+ 解决方案
```
set TMPDIR=d:\tmp
```