from pathlib import Path

from hamilton import driver
from hamilton.io.materialization import from_

from preppin_data import DATA_FOLDER, DIAGRAMS_FOLDER
from preppin_data.y2024.w01 import pd_2024_01


def main() -> None:
    source_data_path = DATA_FOLDER / "y2024" / "w01" / "input.csv"
    materializers = [
        from_.csv(
            target="source_data",
            path=str(source_data_path),
        ),
    ]

    dr = (
        driver.Builder()
        .with_modules(pd_2024_01)
        .with_materializers(*materializers)
        .build()
    )

    dag_path = DIAGRAMS_FOLDER / "pd_2024_01.png"
    dr.display_all_functions(
        output_file_path=dag_path,
        deduplicate_inputs=True,
    )

    final_vars = [
        "source_data",
        "split_flight_details",
        "split_from_to",
        "flow_card_yes_or_no",
        "combined_data",
        "split_into_groups_by_flow_card",
    ]
    inputs = {}
    results = dr.execute(
        final_vars=list(final_vars),
        inputs=inputs,
    )
    for v in results.values():
        print(v)


if __name__ == "__main__":
    main()
