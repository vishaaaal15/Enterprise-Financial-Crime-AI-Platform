import pandas as pd

# Read the original dataset
df = pd.read_csv("data/transactions_v2.csv")

# Randomly select 20,000 rows
demo_df = df.sample(n=20000, random_state=42)

# Save the demo dataset
demo_df.to_csv("data/transactions_demo.csv", index=False)

print("Demo dataset created successfully!")