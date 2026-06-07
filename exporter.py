import sqlite3
import pandas as pd
import os
from datetime import datetime

# تحديد المسار الرئيسي للمشروع ديناميكياً لضمان عدم حدوث أخطاء مسارات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def export_sql_table_to_excel(db_path, table_name, output_folder):
    """
    تقوم هذه الدالة بالاتصال بقاعدة البيانات وسحب الجدول وتحويله إلى ملف إكسيل
    """
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(db_path)
        print(f"[*] Connected successfully to database: {db_path}")
        
        # استعلام SQL لجلب البيانات
        query = f"SELECT * FROM {table_name}"
        
        # قراءة البيانات وتحويلها إلى Dataframe
        df = pd.read_sql_query(query, conn)
        print(f"[*] Retrieved {len(df)} rows from table '{table_name}'.")
        
        # تجهيز اسم ملف الإكسيل مع إضافة ختم زمني لمنع التكرار
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = os.path.join(output_folder, f"{table_name}_export_{timestamp}.xlsx")
        
        # تصدير البيانات إلى ملف Excel
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"[+] Success! Data exported to: {excel_filename}")
        
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # تحديد مسار قاعدة البيانات ومجلد المخرجات بناءً على المسار الرئيسي ديناميكياً
    db_file = os.path.join(BASE_DIR, "Database", "mock_company.db")
    output_dir = BASE_DIR
    
    # تأكيد إنشاء مجلد Database لو لم يكن موجوداً لمنع خطأ الـ OperationalError
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    # إنشاء جدول وهمي للاختبار
    test_conn = sqlite3.connect(db_file)
    cursor = test_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary REAL
        )
    """)
    cursor.execute("DELETE FROM employees")
    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", [
        (1, 'Ahmed', 'Data Engineering', 9500),
        (2, 'Sara', 'BI Analytics', 8000),
        (3, 'Mohamed', 'DevOps', 9000)
    ])
    test_conn.commit()
    test_conn.close()
    
    # تشغيل الدالة وتصدير جدول الموظفين
    export_sql_table_to_excel(db_path=db_file, table_name="employees", output_folder=output_dir)
