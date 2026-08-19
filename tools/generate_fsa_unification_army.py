"""Generate Free States wartime mobilization and postwar demobilization OOBs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "mod" / "history" / "units"
LOCATIONS = [1827, 4799, 853, 4860, 4975]


EMERGENCY_TEMPLATE = """division_template = {
\tname = "Free States Emergency Mobilization Division"
\tpriority = 1
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t\tinfantry = { x = 2 y = 0 }
\t\tinfantry = { x = 2 y = 1 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t}
}
"""

POSTWAR_TEMPLATE = """division_template = {
\tname = "Free States Territorial Division"
\tpriority = 1
\tregiments = {
\t\tinfantry = { x = 0 y = 0 }
\t\tinfantry = { x = 0 y = 1 }
\t\tinfantry = { x = 0 y = 2 }
\t\tinfantry = { x = 1 y = 0 }
\t\tinfantry = { x = 1 y = 1 }
\t\tinfantry = { x = 1 y = 2 }
\t\tinfantry = { x = 2 y = 0 }
\t\tinfantry = { x = 2 y = 1 }
\t\tinfantry = { x = 2 y = 2 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t}
}
"""


def division(name: str, location: int, template: str, experience: float) -> str:
    return f"""\tdivision = {{
\t\tname = "{name}"
\t\tlocation = {location}
\t\tdivision_template = "{template}"
\t\tstart_experience_factor = {experience:.2f}
\t}}
"""


def write_mobilization() -> None:
    output = [EMERGENCY_TEMPLATE, "\nunits = {\n"]
    for index in range(70):
        output.append(
            division(
                f"{index + 1:02d} Emergency Mobilization Division",
                LOCATIONS[index % len(LOCATIONS)],
                "Free States Emergency Mobilization Division",
                0.20,
            )
        )
    output.append("}\n")
    (UNITS / "FSA_unification_mobilization.txt").write_text(
        "".join(output), encoding="utf-8"
    )


def write_postwar() -> None:
    output = [POSTWAR_TEMPLATE, "\nunits = {\n"]
    for index in range(20):
        output.append(
            division(
                f"{index + 1:02d} Postwar Territorial Division",
                LOCATIONS[index % len(LOCATIONS)],
                "Free States Territorial Division",
                0.30,
            )
        )
    output.append("}\n")
    (UNITS / "FSA_postwar_2069.txt").write_text(
        "".join(output), encoding="utf-8"
    )


def main() -> None:
    write_mobilization()
    write_postwar()
    print("Generated 70 temporary wartime and 20 postwar Free States divisions.")


if __name__ == "__main__":
    main()
