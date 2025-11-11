from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def get_all_danhmuc():
    """
    ✅ Lấy toàn bộ danh sách danh mục từ bảng 'danhmuc'
    Trả về list các dict chứa thông tin danh mục
    """
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM danhmuc"
            cursor.execute(sql)
            result = cursor.fetchall()

            if result:
                print("📋 Danh sách danh mục:")
                for row in result:
                    print(f"👉 Mã: {row['madm']} | Tên: {row['tendm']} | Mô tả: {row['mota']}")
            else:
                print("⚠️ Chưa có danh mục nào trong cơ sở dữ liệu.")
            return result

    except Error as e:
        print(f"❌ Lỗi khi lấy danh sách danh mục: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
