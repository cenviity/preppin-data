"""2024 week 1: Prep Air's Flow Card

<https://preppindata.blogspot.com/2024/01/2024-week-1-prep-airs-flow-card.html>
"""

from __future__ import annotations

import pandas as pd
import pandas.testing as pdt
from h11 import Data
from hamilton.function_modifiers import extract_columns, extract_fields
from pandas import DataFrame, Series

pd.options.mode.copy_on_write = True

source_columns = [
    "flight_details",
    "flow_card",
    "bags_checked",
    "meal_type",
]


@extract_columns(*source_columns)
def rename_source_fields(source_data: DataFrame) -> DataFrame:
    return source_data.rename(
        columns={
            "Flight Details": "flight_details",
            "Flow Card?": "flow_card",
            "Bags Checked": "bags_checked",
            "Meal Type": "meal_type",
        }
    )


flight_details_columns = [
    "date",
    "flight_number",
    "from_to",
    "class_",  # Add underscore since `class` is a Python keyword
    "price",
]


@extract_columns(*flight_details_columns)
def split_flight_details(flight_details: Series) -> DataFrame:
    # Split the `Flight Details` field to form new fields
    split_data = flight_details.str.split("//", expand=True)
    split_data.columns = flight_details_columns
    return split_data.astype(
        {
            "date": "datetime64[ns]",
            "price": float,
        }
    )


from_to_columns = [
    "from_",  # Add underscore since `from` is a Python keyword
    "to",
]


@extract_columns(*from_to_columns)
def split_from_to(from_to: Series) -> DataFrame:
    # Split the `from_to` field as well
    split_data = from_to.str.split("-", expand=True)
    split_data.columns = from_to_columns
    return split_data


# # Remove and reorder columns
# columns = [
#     "Date",
#     "Flight Number",
#     "From",
#     "To",
#     "Class",
#     "Price",
#     "Flow Card?",
#     "Bags Checked",
#     "Meal Type",
# ]
# df = df[columns]


# # Check `Flow Card?` field only has values of 0 or 1
# df["Flow Card?"].isin([0, 1]).all()


def flow_card_yes_or_no(flow_card: Series) -> Series:
    # Re-encode `flow_card` field as "Yes" or "No"
    return flow_card.map({0: "No", 1: "Yes"})


def combined_data(  # noqa: PLR0913
    date: Series,
    flight_number: Series,
    from_: Series,
    to: Series,
    class_: Series,
    price: Series,
    flow_card_yes_or_no: Series,
    bags_checked: Series,
    meal_type: Series,
) -> DataFrame:
    return DataFrame(
        {
            "date": date,
            "flight_number": flight_number,
            "from_": from_,
            "to": to,
            "class_": class_,
            "price": price,
            "flow_card": flow_card_yes_or_no,
            "bags_checked": bags_checked,
            "meal_type": meal_type,
        }
    )


@extract_fields(
    {
        "flow_card_yes": DataFrame,
        "flow_card_no": DataFrame,
    }
)
def split_into_groups_by_flow_card(combined_data: DataFrame) -> dict[str, DataFrame]:
    # Separate into groups with and without Flow Card
    flow_card_groups = combined_data.groupby("flow_card")
    flow_card_yes = flow_card_groups.get_group("Yes").reset_index(drop=True)
    flow_card_no = flow_card_groups.get_group("No").reset_index(drop=True)
    return {
        "flow_card_yes": flow_card_yes,
        "flow_card_no": flow_card_no,
    }


# # Tests
# expected_flow_card_yes = pd.read_csv(
#     "data/output_flow_card_yes.csv", parse_dates=["Date"], date_format="%d/%m/%Y"
# )

# expected_flow_card_no = pd.read_csv(
#     "data/output_flow_card_no.csv", parse_dates=["Date"], date_format="%d/%m/%Y"
# )

# pdt.assert_frame_equal(expected_flow_card_yes, flow_card_yes)

# pdt.assert_frame_equal(expected_flow_card_no, flow_card_no)
