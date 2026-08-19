"""Generate China's exact 80-division 2069 starting order of battle."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "mod" / "history" / "units" / "CHI_2069.txt"

# Major cities distributed across the Chinese interior and coast. Every
# province is owned by CHI in the 2069 map.
LOCATIONS = [
    1319, 1047, 7137, 12732, 7186, 10404, 4174, 4709, 5033, 2022,
    10062, 8127, 11771, 7965, 8049, 4973, 1070, 9970, 11822, 11801,
]


def template_block() -> str:
    return """division_template = {
\tname = "People's Defense Division"
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
\t\tartillery = { x = 0 y = 1 }
\t}
}

division_template = {
\tname = "Strategic Mobile Response Division"
\tpriority = 2
\tregiments = {
\t\tmotorized = { x = 0 y = 0 }
\t\tmotorized = { x = 0 y = 1 }
\t\tmotorized = { x = 0 y = 2 }
\t\tmotorized = { x = 1 y = 0 }
\t\tmotorized = { x = 1 y = 1 }
\t\tmotorized = { x = 1 y = 2 }
\t}
\tsupport = {
\t\tengineer = { x = 0 y = 0 }
\t\trecon = { x = 0 y = 1 }
\t}
}

division_template = {
\tname = "Frontier Security Division"
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
\t\trecon = { x = 0 y = 1 }
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


def main() -> None:
    output = [template_block(), "\nunits = {\n"]
    serial = 1

    for index in range(48):
        output.append(
            division(
                f"{serial:02d} People's Defense Division",
                LOCATIONS[index % len(LOCATIONS)],
                "People's Defense Division",
                0.30,
            )
        )
        serial += 1

    for index in range(16):
        output.append(
            division(
                f"{index + 1:02d} Strategic Mobile Response Division",
                LOCATIONS[(index * 3) % len(LOCATIONS)],
                "Strategic Mobile Response Division",
                0.40,
            )
        )

    for index in range(16):
        output.append(
            division(
                f"{index + 1:02d} Frontier Security Division",
                LOCATIONS[(index * 5 + 2) % len(LOCATIONS)],
                "Frontier Security Division",
                0.35,
            )
        )

    output.append("}\n")
    OUTPUT.write_text("".join(output), encoding="utf-8")
    print(f"Generated {OUTPUT} with 80 divisions.")


if __name__ == "__main__":
    main()
