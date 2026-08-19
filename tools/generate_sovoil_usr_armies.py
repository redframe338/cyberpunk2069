"""Generate the 2069 SovOil and Neo-Soviet starting armies."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "mod" / "history" / "units"

SVO_LOCATIONS = (4824, 10696, 10536, 3578, 1459, 11523)
USR_LOCATIONS = (6380, 3151, 3529, 3338, 3134, 121, 6338, 418)


def battalion_grid(unit: str, rows: int, columns: int) -> str:
    lines = []
    for x in range(columns):
        for y in range(rows):
            lines.append(f"\t\t{unit} = {{ x = {x} y = {y} }}\n")
    return "".join(lines)


def generate_sovoil() -> str:
    output = [
        "# AUTO-GENERATED: 40 elite SovOil starting divisions.\n",
        'division_template = {\n\tname = "SovOil Mechanized Energy Guard"\n',
        "\tregiments = {\n",
        battalion_grid("mechanized", 3, 4),
        "\t}\n",
        "\tsupport = {\n",
        "\t\tengineer = { x = 0 y = 0 }\n",
        "\t\trecon = { x = 0 y = 1 }\n",
        "\t\tartillery = { x = 0 y = 2 }\n",
        "\t\tmaintenance_company = { x = 0 y = 3 }\n",
        "\t\tlogistics_company = { x = 0 y = 4 }\n",
        "\t}\n}\n\n",
        'division_template = {\n\tname = "SovOil Arctic Assault Guard"\n',
        "\tregiments = {\n",
        battalion_grid("mountaineers", 3, 4),
        "\t}\n",
        "\tsupport = {\n",
        "\t\tengineer = { x = 0 y = 0 }\n",
        "\t\trecon = { x = 0 y = 1 }\n",
        "\t\tartillery = { x = 0 y = 2 }\n",
        "\t\tmaintenance_company = { x = 0 y = 3 }\n",
        "\t\tlogistics_company = { x = 0 y = 4 }\n",
        "\t}\n}\n\n",
        "units = {\n",
    ]
    for index in range(1, 33):
        location = SVO_LOCATIONS[(index - 1) % len(SVO_LOCATIONS)]
        output.append(
            f'\tdivision = {{ name = "{index:02d}th Mechanized Energy Guard" '
            f'location = {location} division_template = "SovOil Mechanized Energy Guard" '
            "start_experience_factor = 0.90 }\n"
        )
    for index in range(1, 9):
        location = SVO_LOCATIONS[(index + 1) % len(SVO_LOCATIONS)]
        output.append(
            f'\tdivision = {{ name = "{index:02d}th Arctic Assault Guard" '
            f'location = {location} division_template = "SovOil Arctic Assault Guard" '
            "start_experience_factor = 0.85 }\n"
        )
    output.append("}\n")
    return "".join(output)


def generate_usr() -> str:
    output = [
        "# AUTO-GENERATED: 50 Neo-Soviet starting divisions.\n",
        'division_template = {\n\tname = "Neo-Soviet Line Rifle Division"\n',
        "\tregiments = {\n",
        battalion_grid("infantry", 3, 3),
        "\t}\n",
        "\tsupport = {\n",
        "\t\tengineer = { x = 0 y = 0 }\n",
        "\t\tartillery = { x = 0 y = 1 }\n",
        "\t}\n}\n\n",
        "units = {\n",
    ]
    for index in range(1, 51):
        location = USR_LOCATIONS[(index - 1) % len(USR_LOCATIONS)]
        output.append(
            f'\tdivision = {{ name = "{index:02d}th Union Rifle Division" '
            f'location = {location} division_template = "Neo-Soviet Line Rifle Division" '
            "start_experience_factor = 0.25 }\n"
        )
    output.append("}\n")
    return "".join(output)


def main() -> None:
    UNITS.mkdir(parents=True, exist_ok=True)
    (UNITS / "SVO_2069.txt").write_text(generate_sovoil(), encoding="utf-8")
    (UNITS / "USR_2069.txt").write_text(generate_usr(), encoding="utf-8")
    print("Generated 40 elite SovOil and 50 Neo-Soviet starting divisions.")


if __name__ == "__main__":
    main()
