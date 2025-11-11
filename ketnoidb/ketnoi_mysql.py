import mysql.connector
from mysql.connector import Error

def connect_mysql():
    """
    ✅ Hàm kết nối đến MySQL Database
    Trả về đối tượng connection nếu thành công, hoặc None nếu lỗi.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',      # 🖥️ Tên máy chủ MySQL (mặc định: localhost)
            user='root',           # 👤 Tên đăng nhập (mặc định: root)
            password='',           # 🔑 Mật khẩu (để trống nếu không đặt)
            database='thuocak'    # 🗃️ Tên database bạn đang dùng
        )
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công!")
            return conn
    except Error as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
        return None
