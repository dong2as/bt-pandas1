import pandas as pd

data = {
    'Name': ['An', 'Bình', 'Châu', 'Dũng', 'Hà', 'Hùng', 'Lan', 'Mai', 'Nam', 'Phương'],
    'Age': [20, 21, 22, 20, 23, 21, 22, 20, 21, 23],
    'Gender': ['Nam', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nam', 'Nữ', 'Nữ', 'Nam', 'Nữ'],
    'Score': [8.5, 7.0, 4.5, 6.0, 9.0, 3.5, 5.5, 6.5, 7.5, 4.0]
}

df_students = pd.DataFrame(data)

print("Toàn bộ dữ liệu:")
print(df_students)

print("\n3 dòng đầu tiên:")
print(df_students.head(3))

print("\nIndex = 2, cột Name:")
print(df_students.loc[2, 'Name'])

print("\nIndex = 10, cột Age (sẽ báo lỗi nếu vượt index):")
try:
    print(df_students.loc[10, 'Age'])
except KeyError:
    print("Index 10 không tồn tại trong DataFrame.")

print("\nCác cột Name và Score:")
print(df_students[['Name', 'Score']])

df_students['Pass'] = df_students['Score'] >= 5
print("\nThêm cột Pass:")
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\nSắp xếp theo Score giảm dần:")
print(df_sorted)
