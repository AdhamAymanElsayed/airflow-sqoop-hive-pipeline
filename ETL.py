from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.ssh.operators.ssh import SSHOperator


default_args ={'owner':'Adham',
               'retries':2,
               'retry_delay':timedelta(minutes=1),
               'depends_on_past':False}


with DAG('Sqoop_import_DAG',
         description = 'Sqoop to hive with transformations',
         schedule = '@daily',
         default_args = default_args ,
         start_date = datetime(2025,6,1),
         catchup = False ,
         tags = ['MySQL','Sqoop','HDFS','Hive']) as dag:
    
    
    start = EmptyOperator(task_id = "Start")

    sqoop = SSHOperator(
        task_id='Sqoop_import',
        ssh_conn_id = 'sandbox',
        command="""
        sqoop import \
        --connect "jdbc:mysql://192.168.1.14:3306/world?useSSL=false" \
        --username remote \
        --password 123 \
        --table city \
        --target-dir /user/root/project \
        -m 3
        """
        ,cmd_timeout =600)
    
    creation = SSHOperator(
        task_id = 'Create_Hive_Table',
        ssh_conn_id = 'sandbox',
        command= """hive -e "create table if not exists city (ID int, Name string , country_code string , district string , population int) \
            row format delimited \
            fields terminated by ',' \
            stored as textfile;"\
                  """ ,
            cmd_timeout = 600
    )

    loading = SSHOperator(
        task_id='LOAD_Data_to_Hive',
        ssh_conn_id='sandbox',
        command='sudo -u hdfs hive -e "LOAD DATA INPATH \'/user/root/project/\' INTO TABLE city;"',
        cmd_timeout=600
    )

    validate = SSHOperator(task_id = 'Count_Hive',
                           ssh_conn_id = 'sandbox',
                           command = 'hive -e "select count(*) from city;"',
                           cmd_timeout=600 )
    end = EmptyOperator(task_id = "Stop")

    start >> sqoop >> creation >> loading >> validate >>end