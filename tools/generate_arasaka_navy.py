"""Generate Arasaka's performance-safe 2,000-vessel-equivalent starting navy."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "mod" / "history" / "units"
BASE = 11932

SURFACE_COMPOSITION = (
    ("carrier", "ship_hull_carrier_3", "Mikoshi Class", 1, "CV"),
    ("battleship", "ship_hull_heavy_4", "Kusanagi Class", 2, "BB"),
    ("heavy_cruiser", "ship_hull_cruiser_4", "Oni Class", 4, "CA"),
    ("light_cruiser", "ship_hull_cruiser_4", "Kitsune Class", 8, "CL"),
    ("destroyer", "ship_hull_light_4", "Shinobi Class", 35, "DD"),
)
LEGACY_EQUIPMENT = {
    "carrier": "carrier_3",
    "battleship": "battleship_3",
    "heavy_cruiser": "heavy_cruiser_3",
    "light_cruiser": "light_cruiser_3",
    "destroyer": "destroyer_2",
    "submarine": "submarine_3",
}


def ship_line(
    definition: str,
    equipment: str,
    name: str,
    version: str | None,
    pride: bool = False,
) -> str:
    version_text = f' version_name = "{version}"' if version else ""
    pride_text = " pride_of_the_fleet = yes" if pride else ""
    return (
        f'\t\t\tship = {{ name = "{name}" definition = {definition}'
        f"{pride_text} start_experience_factor = 1.0 equipment = {{ {equipment} = "
        f"{{ amount = 1 owner = ARK{version_text} }} }} }}\n"
    )


def generate(mtg: bool) -> str:
    output = [
        "# AUTO-GENERATED: Arasaka Corporate Oceanic Security Command\n",
        "# 400 flotilla counters represent a 2,000-vessel navy without exhausting startup RAM.\n",
        "units = {\n",
    ]
    serials: dict[str, int] = {code: 0 for *_, code in SURFACE_COMPOSITION}
    serials["SS"] = 0

    for fleet_index in range(1, 5):
        output.extend(
            [
                "\tfleet = {\n",
                f'\t\tname = "Arasaka Expeditionary Fleet {fleet_index:02d}"\n',
                f"\t\tnaval_base = {BASE}\n",
                "\t\ttask_force = {\n",
                f'\t\t\tname = "Corporate Strike Group {fleet_index:02d}"\n',
                f"\t\t\tlocation = {BASE}\n",
            ]
        )
        for definition, hull, version, count, code in SURFACE_COMPOSITION:
            equipment = hull if mtg else LEGACY_EQUIPMENT[definition]
            for _ in range(count):
                serials[code] += 1
                name = f"ARK-{code}-{serials[code]:04d}"
                output.append(
                    ship_line(
                        definition,
                        equipment,
                        name,
                        version if mtg else None,
                        pride=(fleet_index == 1 and code == "CV" and serials[code] == 1),
                    )
                )
        output.extend(["\t\t}\n", "\t}\n"])

    for fleet_index in range(1, 5):
        output.extend(
            [
                "\tfleet = {\n",
                f'\t\tname = "Arasaka Ghost Fleet {fleet_index:02d}"\n',
                f"\t\tnaval_base = {BASE}\n",
                "\t\ttask_force = {\n",
                f'\t\t\tname = "Ghost Submarine Group {fleet_index:02d}"\n',
                f"\t\t\tlocation = {BASE}\n",
            ]
        )
        for _ in range(50):
            serials["SS"] += 1
            output.append(
                ship_line(
                    "submarine",
                    "ship_hull_submarine_4" if mtg else LEGACY_EQUIPMENT["submarine"],
                    f"ARK-SS-{serials['SS']:04d}",
                    "Ghost Class" if mtg else None,
                )
            )
        output.extend(["\t\t}\n", "\t}\n"])

    output.append("}\n")
    return "".join(output)


def main() -> None:
    UNITS.mkdir(parents=True, exist_ok=True)
    (UNITS / "ARK_2069_naval.txt").write_text(generate(mtg=True), encoding="utf-8")
    (UNITS / "ARK_2069_naval_legacy.txt").write_text(
        generate(mtg=False), encoding="utf-8"
    )
    print("Generated MTG and legacy Arasaka OOBs: 400 counters / 2,000-vessel equivalent.")


if __name__ == "__main__":
    main()
