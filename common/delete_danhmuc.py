from mysql.connector import Error

from ketnoidb.ketnoi_mysql import connect_mysql


def delete_danhmuc(madm):
    """
    ✅ Xóa một danh mục khỏi bảng 'danhmuc' theo mã danh mục (madm)
    - madm: ID của danh mục cần xóa
    """
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM danhmuc WHERE madm = %s"
            cursor.execute(sql, (madm,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"🗑️ Đã xóa danh mục có mã {madm} thành công.")
            else:
                print(f"⚠️ Không tìm thấy danh mục có mã {madm}.")
    except Error as e:
        print(f"❌ Lỗi khi xóa danh mục: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
