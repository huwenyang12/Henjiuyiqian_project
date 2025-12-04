#-*- coding:utf-8 -*-
from datetime import datetime
from datetime import timedelta
import os,sys
import MySQLdb
import MySQLdb.cursors as cors
import pandas as pd
import uuid
import traceback
import warnings
from feishu import FeiShu
import traceback
from log import logger


warnings.filterwarnings('ignore')


def get_year(start_date, end_date):
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    month_dict = {}
    query_days = []
    while start_date_dt <= end_date_dt:
        date_str = start_date_dt.strftime("%Y-%m-%d")
        query_days.append(date_str)
        last_month = start_date_dt.month
        if last_month not in month_dict.keys():
            month_dict[last_month] = start_date_dt.year
        start_date_dt = start_date_dt + timedelta(days=1)    
    #month_dict[9] = 2023
    return month_dict, query_days

def insert_db(params):
    
    sql = "insert into yongyou_data values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    retry_times = 3
    while True:
        if retry_times < 0:
            raise Exception("入库失败，已重试3次")
        # conn = MySQLdb.connect("localhost", "root", "root", "bt_console", cursorclass = cors.DictCursor)
        conn = MySQLdb.connect("rm-2zetkwh4s22am33a0lo.mysql.rds.aliyuncs.com", "esznkj", "esznkj20231027@", "yongyou_data", cursorclass = cors.DictCursor)
        cur = conn.cursor()

        try:            
            # 批量插入  
            cur.executemany(sql, params)  
            conn.commit()
            break
        except Exception as e:  
            logger.error("插入失败，" + traceback.format_exc())
            conn.rollback()
        finally:
            if cur:
                cur.close()

            if conn:
                conn.close()     

def remove_repeat_days_db(query_days):
    logger.info("开始删除重复数据...")
    for query_date in query_days:        
        date_parts = query_date.split("-")
        query_year = int(date_parts[0])
        query_month = int(date_parts[1])
        query_day = int(date_parts[2])

        retry_times = 3
        while True:
            if retry_times < 0:
                raise Exception("删除重复数据失败，已重试3次")
            # conn = MySQLdb.connect("localhost", "root", "root", "bt_console", cursorclass = cors.DictCursor)
            conn = MySQLdb.connect("rm-2zetkwh4s22am33a0lo.mysql.rds.aliyuncs.com", "esznkj", "esznkj20231027@", "yongyou_data", cursorclass = cors.DictCursor)
            cur = conn.cursor()
            query_sql = 'select * from yongyou_data where year = %s and month = %s and day = %s limit 1'%(query_year, query_month, query_day)
            sql = 'delete from yongyou_data where year = %s and month = %s and day = %s '%(query_year, query_month, query_day)

            try:     
                query_r = cur.execute(query_sql)
                if query_r == 0 or query_r is None:
                    break                 
                logger.info(f"正在删除重复数据：{query_date}...")       
                cur.execute(sql)  
                conn.commit()
                break
            except Exception as e:  
                logger.error("删除重复数据失败，" + traceback.format_exc())
                conn.rollback()
            finally:
                if cur:
                    cur.close()

                if conn:
                    conn.close() 

    logger.info("删除重复数据完成")

def main(data_folder, download_time, start_date, end_date):
    try:
        month_dict, query_days = get_year(start_date, end_date)
        remove_repeat_days_db(query_days)

        download_time = datetime.strptime(download_time, '%Y%m%d%H%M%S')
        create_date = download_time.strftime("%Y%m%d")
        data_files = os.listdir(data_folder)
        # FeiShu().send_message(f"文件需要录入数量为{len(data_files)}")
        for data_file in data_files:
            f_file = os.path.join(data_folder, data_file)
            if 'part' not in data_file:
                df = pd.read_excel(f_file, skiprows=13, dtype=str)
                start_row_index = 16
            else:
                df = pd.read_excel(f_file, skiprows=1, dtype=str)
                start_row_index = 3
            
            batch = len(df) // 1000 + 1
            logger.info(f"文件: {f_file}, 开始分 {batch} 批次录入...")
            # FeiShu().send_message(f"文件: {f_file}, 开始分 {batch} 批次录入...")
            for index in range(batch):
                
                start_row = index * 1000
                end_row = index * 1000 + 1000 if index * 1000 + 1000 < len(df) else len(df)
                count = end_row - start_row
                if count == 0:
                    break
                select_df = df[start_row:end_row]
                print(f"开始录入第{start_row + start_row_index}行到第{end_row + start_row_index - 1}行...")
                params = []
                for row_index, row in select_df.iterrows():
                    if pd.isnull(row[0]):
                        continue
                    main_account = "" if pd.isnull(row[2]) else row[2]
                    bill_date = row[4]  # '2025-11-01'
                    year, month, day = bill_date.split("-")
                    voucher_no = "" if pd.isnull(row[5]) else row[5]
                    entry_no = "" if pd.isnull(row[6]) else row[6]
                    summary = "" if pd.isnull(row[7]) else row[7]
                    subject_code = "" if pd.isnull(row[8]) else row[8]
                    subject_name = "" if pd.isnull(row[9]) else row[9]
                    additional = "" if pd.isnull(row[53]) else row[53]
                    currency = "" if pd.isnull(row[55]) else row[55]
                    debit_original = float(row[59]) if not pd.isnull(row[59]) else 0.0
                    debit_local    = float(row[60]) if not pd.isnull(row[60]) else 0.0
                    credit_original = float(row[62]) if not pd.isnull(row[62]) else 0.0
                    credit_local    = float(row[63]) if not pd.isnull(row[63]) else 0.0
                    maker = "" if pd.isnull(row[65]) else row[65]
                    reviewer = "" if pd.isnull(row[66]) else row[66]
                    accounter = "" if pd.isnull(row[67]) else row[67]
                    subject_fee = ""
                    verification_info = ""
                    bill_info = ""
                    inner_trade_info = ""
                    signer = ""
                    params.append((uuid.uuid4().hex, create_date, datetime.now(), download_time, main_account, year, month, day, voucher_no, entry_no, summary, subject_code, subject_name, additional, currency, debit_original, debit_local, credit_original, credit_local, subject_fee, verification_info, bill_info, inner_trade_info, maker, reviewer, accounter, signer ))
                insert_db(params)
                logger.info(f"第{start_row + start_row_index}行到第{end_row + start_row_index - 1}行录入完成")
        # FeiShu().send_message(f"录入数据库完成")
    except:
        # FeiShu().send_message(f"入库失败，{traceback.format_exc()}")
        pass

if __name__ == "__main__":
    
    # datafolder = sys.argv[1]
    # download_time = sys.argv[2]
    # start_date = sys.argv[3]
    # end_date = sys.argv[4]
    download_time = '20251126120000' # %Y%m%d%H%M%S
    datafolder = r"D:\qcyq\很久以前\20251126101538"
    start_date = "2025-11-01"     
    end_date   = "2025-11-30"
    logger.info("开始入库...")
    main(datafolder, download_time, start_date, end_date)
    logger.info("入库完成")
