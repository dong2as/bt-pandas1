import pandas as pd
import numpy as np

nhan_vien = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
})

phong_ban = pd.DataFrame({
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
})

# B1: Kiểm tra các ô bị thiếu
print("Số lượng giá trị bị thiếu trong mỗi cột:")
print(nhan_vien.isnull().sum())

# B2: Xoá dòng có hơn 2 giá trị thiếu
nhan_vien = nhan_vien.dropna(thresh=4)

# B3: Điền giá trị thiếu
nhan_vien['Name'] = nhan_vien['Name'].fillna('Chưa rõ')
nhan_vien['Age'] = nhan_vien['Age'].fillna(nhan_vien['Age'].mean())
nhan_vien['Salary'] = nhan_vien['Salary'].fillna(method='ffill')
nhan_vien['Department'] = nhan_vien['Department'].fillna('Unknown')

# B4: Chuyển kiểu dữ liệu Age, Salary về int
nhan_vien['Age'] = nhan_vien['Age'].astype(int)
nhan_vien['Salary'] = nhan_vien['Salary'].astype(int)

# B5: Tạo cột Salary_after_tax
nhan_vien['Salary_after_tax'] = (nhan_vien['Salary'] * 0.9).astype(int)

# B6: Lọc nhân viên phòng IT và tuổi > 25
nhan_vien_it = nhan_vien[(nhan_vien['Department'] == 'IT') & (nhan_vien['Age'] > 25)]
print("\nNhân viên phòng IT tuổi > 25:")
print(nhan_vien_it)

# B7: Sắp xếp theo Salary_after_tax giảm dần
nhan_vien_sorted = nhan_vien.sort_values(by='Salary_after_tax', ascending=False)
print("\nNhân viên sắp xếp theo Salary_after_tax giảm dần:")
print(nhan_vien_sorted)

# B8: Nhóm theo Department và tính lương trung bình
avg_salary_by_dept = nhan_vien.groupby('Department')['Salary'].mean().reset_index()
print("\nLương trung bình theo phòng ban:")
print(avg_salary_by_dept)

# B9: Nối với bảng phòng ban để có Manager
nhan_vien_full = pd.merge(nhan_vien, phong_ban, on='Department', how='left')
print("\nBảng nhân viên có thêm thông tin Manager:")
print(nhan_vien_full)

#B10: Thêm nhân viên mới bằng concat
nhan_vien_moi = pd.DataFrame({
    'ID': [107, 108],
    'Name': ['Mai', 'Tú'],
    'Age': [27, 29],
    'Department': ['Marketing', 'Finance'],
    'Salary': [760, 720]
})
nhan_vien_moi['Salary_after_tax'] = (nhan_vien_moi['Salary'] * 0.9).astype(int)
nhan_vien_moi['Manager'] = np.nan  
columns_order = ['ID', 'Name', 'Age', 'Department', 'Salary', 'Salary_after_tax', 'Manager']
nhan_vien_moi = nhan_vien_moi[columns_order]
nhan_vien_full = nhan_vien_full[columns_order]
nhan_vien_final = pd.concat([nhan_vien_full, nhan_vien_moi], ignore_index=True)
print("\nBảng nhân viên sau khi thêm nhân viên mới:")
print(nhan_vien_final)
