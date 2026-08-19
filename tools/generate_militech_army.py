"""Generate Militech's 60-division apex infantry starting army."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "mod" / "history" / "units" / "MLT_2069.txt"
LOCATIONS = (10412, 7588, 4740, 12501, 13091, 12586, 12140)


def main() -> None:
    lines = [
        "# AUTO-GENERATED: 60 Militech apex infantry divisions.\n",
        'division_template = {\n\tname = "Militech Apex Combat Division"\n',
        "\tregiments = {\n",
    ]
    for x in range(4):
        for y in range(3):
            lines.append(f"\t\tinfantry = {{ x = {x} y = {y} }}\n")
    for y in range(3):
        lines.append(f"\t\tartillery_brigade = {{ x = 4 y = {y} }}\n")
    lines.extend(
        [
            "\t}\n",
            "\tsupport = {\n",
            "\t\tengineer = { x = 0 y = 0 }\n",
            "\t\trecon = { x = 0 y = 1 }\n",
            "\t\tartillery = { x = 0 y = 2 }\n",
            "\t\tanti_tank = { x = 0 y = 3 }\n",
            "\t\tlogistics_company = { x = 0 y = 4 }\n",
            "\t}\n}\n\n",
            "units = {\n",
        ]
    )
    for index in range(1, 61):
        location = LOCATIONS[(index - 1) % len(LOCATIONS)]
        lines.append(
            f'\tdivision = {{ name = "Militech Apex Division {index:02d}" '
            f'location = {location} division_template = "Militech Apex Combat Division" '
            "start_experience_factor = 1.00 }\n"
        )
    lines.append("}\n")
    OUTPUT.write_text("".join(lines), encoding="utf-8")
    print("Generated exactly 60 Militech apex infantry divisions.")


if __name__ == "__main__":
    main()
