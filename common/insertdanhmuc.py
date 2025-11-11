from ketnoidb.ketnoi_mysql import connect_mysql
from mysql.connector import Error

def insert_danhmuc(tendm, mota=None):
    """
    ✅ Thêm 1 danh mục mới vào bảng 'danhmuc'
    - tendm: tên danh mục (bắt buộc)
    - mota: mô tả (tùy chọn)
    """
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO danhmuc (tendm, mota) VALUES (%s, %s)"
            values = (tendm, mota)
            cursor.execute(sql, values)
            conn.commit()
            print(f"✅ Đã thêm danh mục mới: {tendm}")
    except Error as e:
        print(f"❌ Lỗi khi thêm danh mục: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()