"""2024 week 1: Prep Air's Flow Card

<https://preppindata.blogspot.com/2024/01/2024-week-1-prep-airs-flow-card.html>
"""

import pandas as pd
import pandas.testing as pdt

pd.options.mode.copy_on_write = True

df = pd.read_csv("data/input.csv")
df.head()

# Split the `Flight Details` field to form new fields
split_data = df["Flight Details"].str.split("//", expand=True)
split_data.columns = ["Date", "Flight Number", "From-To", "Class", "Price"]

df = df.assign(**split_data)

# Split the `From-To` field as well
split_data = df["From-To"].str.split("-", expand=True)
split_data.columns = ["From", "To"]

df = df.assign(**split_data)

# Remove and reorder columns
columns = [
    "Date",
    "Flight Number",
    "From",
    "To",
    "Class",
    "Price",
    "Flow Card?",
    "Bags Checked",
    "Meal Type",
]
df = df[columns]

# Cast to appropriate data types
df = df.astype(
    {
        "Date": "datetime64[ns]",
        "Price": float,
    }
)

# Check `Flow Card?` field only has values of 0 or 1
df["Flow Card?"].isin([0, 1]).all()

# Re-encode `Flow Card?` field as "Yes" or "No"
df = df.replace({"Flow Card?": {0: "No", 1: "Yes"}})

# Separate into groups with and without Flow Card
flow_card_groups = df.groupby(by="Flow Card?")

flow_card_yes = flow_card_groups.get_group("Yes").reset_index(drop=True)

flow_card_no = flow_card_groups.get_group("No").reset_index(drop=True)

# Tests
expected_flow_card_yes = pd.read_csv(
    "data/output_flow_card_yes.csv", parse_dates=["Date"], date_format="%d/%m/%Y"
)

expected_flow_card_no = pd.read_csv(
    "data/output_flow_card_no.csv", parse_dates=["Date"], date_format="%d/%m/%Y"
)

pdt.assert_frame_equal(expected_flow_card_yes, flow_card_yes)

pdt.assert_frame_equal(expected_flow_card_no, flow_card_no)
