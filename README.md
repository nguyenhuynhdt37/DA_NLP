
# Đồ án 11: Hệ thống phân loại nội dung bài đăng diễn đàn

## Phần 1. Kiến thức lập trình Python cơ bản — 2 điểm

- Khai báo hoặc nhập danh sách ít nhất 10 văn bản/câu ngắn phù hợp với bài toán.
- In ra số lượng văn bản trong danh sách.
- Đếm số từ trong từng văn bản.
- Viết hàm chuẩn hóa văn bản về chữ thường.
- Viết hàm loại bỏ dấu câu hoặc khoảng trắng thừa.
- Viết hàm đếm tần suất từ trong một văn bản và in kết quả.

## Phần 2. Bài toán ứng dụng xử lý ngôn ngữ tự nhiên — 8 điểm

Một diễn đàn trực tuyến muốn phân loại bài đăng của người dùng vào các chuyên mục như học tập, giải trí, hỏi đáp hoặc mua bán.

- Chuẩn bị tập dữ liệu nhỏ gồm văn bản mẫu và nhãn/nhóm tương ứng.
- Nhập hoặc khai báo một văn bản mới cần xử lý.
- Tiền xử lý văn bản: chuẩn hóa chữ thường, xóa dấu câu, xóa khoảng trắng thừa, tách từ.
- Xây dựng danh sách từ đặc trưng từ tập dữ liệu mẫu.
- Biểu diễn văn bản thành dạng dữ liệu có thể tính toán.
- Tính điểm hoặc xác suất của văn bản mới đối với từng nhóm.
- In ra điểm hoặc xác suất của từng nhóm.
- In ra nhóm/nhãn được dự đoán và nhận xét ngắn gọn.
- Không sử dụng thư viện học máy hoặc NLP có sẵn.

# He thong phan loai noi dung bai dang dien dan

Web demo dung Flask. Phan xu ly ngon ngu va phan loai duoc tu cai dat, khong dung thu vien ML/NLP co san.

## Muc tieu

He thong nhan vao mot bai dang dien dan va phan loai vao 1 trong 4 nhom:

- Hoc tap
- Giai tri
- Hoi dap
- Mua ban

Du lieu mau hien co:

- 16 van ban mau de thu nhanh tren giao dien.
- 108 van ban huan luyen co nhan, moi nhan co 27 van ban.
- 348 tu/cum trong tap tu vung dac trung sau tien xu ly.
- 236 cum tu trong tu dien ngu nghia va 33 tu don dac trung de ho tro fallback.

## Cai dat

```powershell
cd C:\Users\Admin\DA_NLP
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Chay chuong trinh

```powershell
.\venv\Scripts\python.exe app.py
```

Mo trinh duyet tai:

```text
http://127.0.0.1:8001
```

## Chay bao cao terminal

Lenh nay in ra dung cac thong ke co ban trong de bai: so luong van ban, so tu tung van ban, tan suat tu, tap du lieu co nhan, tu/cum dac trung va demo phan loai.
Bao cao cung co muc debug tach tu/cum, tu/cum dac trung theo tung nhan, danh gia leave-one-out va ma tran nham lan.

```powershell
.\venv\Scripts\python.exe report.py
```

## Thu vien su dung

- Flask: tao web.
- Khong dung scikit-learn, pandas, numpy, nltk, underthesea, pyvi, transformers.

## Cau truc

```text
app.py                 Server web bang Flask
data.py                Van ban mau va tap du lieu huan luyen
text_processing.py     Chuan hoa, tach tu bang tu dien, dem tan suat, Naive Bayes tu cai dat
report.py              In thong ke va ket qua phan loai ra terminal
templates/index.html   Giao dien HTML
static/style.css       CSS
requirements.txt       Thu vien can cai
```

## Cach xu ly

1. Chuan hoa van ban:
   - Dua ve chu thuong.
   - Giu dau tieng Viet de tranh mat nghia.
   - Xoa dau cau, ky tu dac biet.
   - Xoa khoang trang thua.

2. Tach tu/cum tu:
   - Tach theo khoang trang sau khi chuan hoa.
   - Ghep cac cum co nghia bang tu dien cum tu tieng Viet, vi du: `lập trình python`, `tài liệu`, `mua bán`, `đăng nhập`.
   - Dung maximum matching: uu tien cum dai nhat co trong tu dien.
   - Khi gap cum dai, he thong van bo sung cac cum con co nghia de tinh xac suat, giup tu dien rong nhung khong lam mat tin hieu phan loai.

3. Dem tan suat:
   - Dung `Counter` de dem so lan xuat hien cua tung tu/cum.
   - Tao danh sach tu/cum dac trung tu tap huan luyen.

4. Phan loai:
   - Dung Naive Bayes tu cai dat.
   - Tinh xac suat tien nghiem cua tung nhan.
   - Tinh xac suat tu/cum theo tung nhan.
   - Dung Laplace smoothing de xu ly tu chua gap.
   - Nhan cac xac suat thanh phan de tinh diem cho tung nhan theo cong thuc Naive Bayes co ban.

5. Giai thich ket qua:
   - Hien thi van ban da tach tu/cum theo ngu nghia.
   - Hien thi cac dac trung duoc dung de tinh xac suat.
   - Hien thi tu/cum trung voi tap huan luyen va tan suat cua chung trong nhan du doan.

6. Danh gia mo hinh:
   - Dung leave-one-out: moi lan lay 1 van ban lam mau kiem thu, 107 van ban con lai lam tap huan luyen.
   - Tinh do chinh xac, precision, recall va ma tran nham lan.
   - Ket qua hien tai tren tap du lieu mau: 108/108 du doan dung, do chinh xac 100%.
   - Tat ca phep tinh deu tu cai dat bang Python co ban.

## Doi chieu voi yeu cau de bai

| Yeu cau | Trang thai |
|---|---|
| Khai bao it nhat 10 van ban | Dat: co 16 van ban mau |
| In ra so luong van ban | Dat: giao dien va `report.py` |
| Dem so tu trong tung van ban | Dat |
| Chuan hoa van ban ve chu thuong | Dat |
| Loai bo dau cau/khoang trang thua | Dat |
| Dem tan suat tu trong van ban | Dat |
| Co tap du lieu van ban mau va nhan | Dat: 108 mau, 4 nhan |
| Nhap van ban moi de phan loai | Dat |
| Tien xu ly van ban | Dat |
| Xay dung danh sach tu dac trung | Dat |
| Bieu dien van ban thanh dang tinh toan | Dat |
| Tinh xac suat van ban moi doi voi tung nhom | Dat |
| In nhan co xac suat cao nhat | Dat |
| In xac suat tung nhom | Dat |
| Khong dung thu vien ML/NLP co san | Dat |

## Diem vuot yeu cau

- Co tu dien cum tu ngu nghia tieng Viet va maximum matching tu cai dat.
- Giu dau tieng Viet de tranh mat nghia.
- Co fallback cum con de tu dien rong nhung van khong mat tin hieu phan loai.
- Co bang tu/cum dac trung rieng cho tung nhan.
- Co giai thich vi sao he thong chon nhan du doan.
- Co danh gia leave-one-out va ma tran nham lan, khong dung thu vien ML.

## Ly thuyet can nam

- Python co ban: list, tuple, dict, set, ham, vong lap, dieu kien.
- Xu ly chuoi: lowercase, regular expression, xoa ky tu dac biet.
- Tien xu ly ngon ngu tu nhien: tach tu, stop words, chuan hoa van ban.
- Bag of Words: bieu dien van ban bang tan suat tu.
- Naive Bayes: prior, likelihood, Laplace smoothing, nhan xac suat thanh phan.
