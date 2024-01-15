
## Hướng dẫn sử dụng
Để tạo maze bạn cần làm theo các mẫu có sẵn trong các file text maze.txt. Một maze ví du:

    #####B#
    ##### #
    ####  #
    #### ##
         ##
    A######

    "A": là điểm bắt đầu maze
    "B": là điểm kết thúc maze
    "#": là tường của maze
    " ": là đường đi trong maze


1. **Clone Repository:**
   ```bash
   git clone https://github.com/tranlequocthong313/cs50_ai.git
   ```

2. **Di chuyển vào thư mục Dự án:**
   ```bash
   cd cs50_ai
   ```

3. **Tạo Môi Trường Ảo (Optional, nhưng được khuyến khích):**
   ```bash
   python -m venv venv
   ```

4. **Truy Cập vào Môi Trường Ảo:**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```

   - **Bash:**
     ```bash
     source venv/Scripts/activate
     ```
        hoặc
     ```bash
     source venv/bin/activate
     ```

5. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Đọc hướng dẫn sử dụng:**
   ```bash
   python maze.py --help
   ```

7. **Chạy ứng dụng:**
   ```bash
   python maze.py maze1.txt
   ```
