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
print("Số lượng giá trị bị thiếu trong mỗi cột:")
print(nhan_vien.isnull().sum())
nhan_vien = nhan_vien.dropna(thresh=4)
nhan_vien['Name']= nhan_vien['Name'].fillna('chua ro')
nhan_vien['Age']= nhan_vien['Age'].fillna(nhan_vien['Age'].mean())
nhan_vien['Salary']= nhan_vien['Salary'].fillna( method = 'ffill' )
nhan_vien['Department']= nhan_vien['Department'].fillna('Unknown')
print(nhan_vien)
nhan_vien['Age']= nhan_vien['Age'].astype(int)
nhan_vien['Salary']= nhan_vien['Salary'].astype(int)
print(nhan_vien)
nhan_vien['Salary_after_tax'] = (nhan_vien['Salary'] *0.9 ).astype(int)
print(nhan_vien)
nhan_vien_SALARY = nhan_vien.sort_values(by= 'Salary_after_tax', ascending=True)
print(nhan_vien_SALARY)
print(nhan_vien.loc[(nhan_vien['Department'] == 'IT') & (nhan_vien['Age'] >= 25)])
avg_salary_by_dept = nhan_vien.groupby('Department')['Salary'].mean()
print("\nLương trung bình theo phòng ban:")
print(nhan_vien.groupby('Department')['Salary'].mean())
