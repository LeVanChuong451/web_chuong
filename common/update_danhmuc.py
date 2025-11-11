from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def update_danhmuc(madm, tendm=None, mota=None):
    """
    ✅ Cập nhật thông tin danh mục trong bảng 'danhmuc'
    - madm: ID của danh mục cần cập nhật
    - tendm: tên danh mục mới (tùy chọn)
    - mota: mô tả mới (tùy chọn)
    """
    try:
        conn = connect_mysql()
        if conn:
            cursor = conn.cursor()

            # Tạo câu lệnh động tùy theo giá trị được truyền
            updates = []
            values = []
            if tendm:
                updates.append("tendm = %s")
                values.append(tendm)
            if mota:
                updates.append("mota = %s")
                values.append(mota)

            if not updates:
                print("⚠️ Không có dữ liệu nào để cập nhật.")
                return

            sql = f"UPDATE danhmuc SET {', '.join(updates)} WHERE madm = %s"
            values.append(madm)

            cursor.execute(sql, tuple(values))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"✅ Đã cập nhật danh mục có mã {madm} thành công.")
            else:
                print(f"⚠️ Không tìm thấy danh mục có mã {madm}.")
    except Error as e:
        print(f"❌ Lỗi khi cập nhật danh mục: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
