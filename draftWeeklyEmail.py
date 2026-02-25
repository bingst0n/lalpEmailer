import pandas as pd
from datetime import datetime, timedelta

curr_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
next_monday = curr_date + timedelta(days=5)

awareness_df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1ss6kHQD9Ikj8PFT5Gh9pIAagwK6q1ELeSaIJrav99kg/export?format=csv")
readaloud_df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1g1x3YABvaai-T7W3Mtf1ab3Vnfnx5zcQFnb7GudFHgM/export?format=csv")

def is_full_awareness(row):
    filled = row.iloc[6:10].notna().sum()
    return filled >= 3

def is_full_readaloud(row):
    filled = row.iloc[5:8].notna().sum()
    return filled >= 3

awareness = [row.iloc[0] for _, row in awareness_df.iterrows() 
             if pd.notna(row.iloc[0]) 
             and datetime.strptime(row.iloc[0], "%m/%d/%Y") >= next_monday 
             and not is_full_awareness(row)]
readaloud = [row.iloc[0] for _, row in readaloud_df.iterrows() 
             if pd.notna(row.iloc[0]) 
             and datetime.strptime(row.iloc[0], "%m/%d/%Y") >= next_monday 
             and not is_full_readaloud(row)]

awareness_presentations = len([d for d in awareness if datetime.strptime(d, "%m/%d/%Y") <= next_monday + timedelta(days=4)])
readaloud_presentations = len([d for d in readaloud if datetime.strptime(d, "%m/%d/%Y") <= next_monday + timedelta(days=4)]) 

draft = f"""Hello everyone,

We hope you're having a great week! We are reaching out today to let you know about upcoming Awareness Presentation and Read Aloud opportunities. You can sign up for either below:

Awareness Presentations ({len(awareness)} available): https://docs.google.com/spreadsheets/d/1ss6kHQD9Ikj8PFT5Gh9pIAagwK6q1ELeSaIJrav99kg/edit?gid=1193248894#gid=1193248894
Read Alouds ({len(readaloud)} available): https://docs.google.com/spreadsheets/d/1g1x3YABvaai-T7W3Mtf1ab3Vnfnx5zcQFnb7GudFHgM/edit?gid=1444627900#gid=1444627900

Have a great week!

Warmly,
The LaLP Leaders
"""

print(draft)