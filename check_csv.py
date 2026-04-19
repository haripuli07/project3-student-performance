import pandas as pd
df = pd.read_csv('StudentPerformanceFactors.csv')
print(f'Total rows: {len(df)}')
print(f'Unique roll_no: {df.roll_no.nunique()}')
dupes = df[df.roll_no.duplicated(keep=False)].sort_values('roll_no')
print(f'Duplicate rows: {len(dupes)}')
if len(dupes) > 0:
    print("\nFirst 10 duplicate entries:")
    print(dupes[['roll_no', 'name']].head(10))
else:
    print("No duplicates in CSV file")
