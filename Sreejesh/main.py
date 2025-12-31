

df['date'] = pd.to_datetime(df['date'])
print(f"✓ Converted 'date' to datetime format")


df = df.sort_values(['household_id', 'date']).reset_index(drop=True)
print(f" Sorted data by household_id and date")

duplicates = df.duplicated().sum()
print(f" Duplicate rows found: {duplicates}")
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"  Removed {duplicates} duplicate rows")

missing_before = df.isnull().sum().sum()
if missing_before > 0:
    print(f"\n Handling missing values ({missing_before} total)...")

df['units_consumed_kwh'].fillna(method='ffill', inplace=True)
df['units_consumed_kwh'].fillna(method='bfill', inplace=True)

df['estimated_bill_rs'].fillna(method='ffill', inplace=True)
df['estimated_bill_rs'].fillna(method='bfill', inplace=True)

df['peak_usage_flag'].fillna(df['peak_usage_flag'].mode()[0], inplace=True)
df['remarks'].fillna('Normal', inplace=True)

print(f"  Missing values after cleaning: {df.isnull().sum().sum()}")

Q1 = df['units_consumed_kwh'].quantile(0.25)
Q3 = df['units_consumed_kwh'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR  # Using 3*IQR for less aggressive outlier removal
upper_bound = Q3 + 3 * IQR

outliers = ((df['units_consumed_kwh'] < lower_bound) |
            (df['units_consumed_kwh'] > upper_bound)).sum()
print(f"\n✓ Outliers detected: {outliers}")
print(f"  Consumption range: [{lower_bound:.2f}, {upper_bound:.2f}] kWh")


