"""Generate Biotechnica's 800-vessel-equivalent navy and 10,000-aircraft force."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UNITS = ROOT / "mod" / "history" / "units"
NAVAL_BASE = 1751
AIR_STATES = (8, 39, 72, 139, 148, 172, 698, 788, 848, 975)


def ship(definition: str, equipment: str, name: str, version: str | None) -> str:
    version_text = f' version_name = "{version}"' if version else ""
    return (
        f'\t\t\tship = {{ name = "{name}" definition = {definition} '
        f"start_experience_factor = 0.85 equipment = {{ {equipment} = "
        f"{{ amount = 1 owner = BIO{version_text} }} }} }}\n"
    )


def navy(mtg: bool) -> str:
    classes = {
        "carrier": ("ship_hull_carrier_3", "Helix Class", "carrier_3"),
        "battleship": ("ship_hull_heavy_4", "Genome Class", "battleship_3"),
        "heavy_cruiser": ("ship_hull_cruiser_4", "Chimera Class", "heavy_cruiser_3"),
        "light_cruiser": ("ship_hull_cruiser_4", "Europa Class", "light_cruiser_3"),
        "destroyer": ("ship_hull_light_4", "Vector Class", "destroyer_2"),
        "submarine": ("ship_hull_submarine_4", "Leviathan Class", "submarine_3"),
    }
    serials = {key: 0 for key in classes}
    output = [
        "# AUTO-GENERATED: 160 flotilla counters represent 800 advanced ships.\n",
        "units = {\n",
    ]
    surface = (
        ("carrier", 1),
        ("battleship", 1),
        ("heavy_cruiser", 2),
        ("light_cruiser", 4),
        ("destroyer", 12),
    )
    for index in range(1, 5):
        output.extend(
            [
                "\tfleet = {\n",
                f'\t\tname = "Biotechnica Oceanic Fleet {index:02d}"\n',
                f"\t\tnaval_base = {NAVAL_BASE}\n",
                "\t\ttask_force = {\n",
                f'\t\t\tname = "Bioengineered Strike Group {index:02d}"\n',
                f"\t\t\tlocation = {NAVAL_BASE}\n",
            ]
        )
        for definition, count in surface:
            hull, version, legacy = classes[definition]
            for _ in range(count):
                serials[definition] += 1
                output.append(
                    ship(
                        definition,
                        hull if mtg else legacy,
                        f"BIO-{definition.upper()}-{serials[definition]:04d}",
                        version if mtg else None,
                    )
                )
        output.extend(["\t\t}\n", "\t}\n"])
    for index in range(1, 5):
        output.extend(
            [
                "\tfleet = {\n",
                f'\t\tname = "Biotechnica Deep Ocean Fleet {index:02d}"\n',
                f"\t\tnaval_base = {NAVAL_BASE}\n",
                "\t\ttask_force = {\n",
                f'\t\t\tname = "Leviathan Group {index:02d}"\n',
                f"\t\t\tlocation = {NAVAL_BASE}\n",
            ]
        )
        hull, version, legacy = classes["submarine"]
        for _ in range(20):
            serials["submarine"] += 1
            output.append(
                ship(
                    "submarine",
                    hull if mtg else legacy,
                    f"BIO-SS-{serials['submarine']:04d}",
                    version if mtg else None,
                )
            )
        output.extend(["\t\t}\n", "\t}\n"])
    output.append("}\n")
    return "".join(output)


def air_force(bba: bool) -> str:
    aircraft = (
        ("small_plane_airframe_3", "Genetek Air Superiority", "fighter_equipment_3", 500),
        ("small_plane_cas_airframe_3", "Manticore CAS", "CAS_equipment_3", 250),
        ("medium_plane_airframe_3", "Europa Strategic Tactical", "tac_bomber_equipment_3", 150),
        (
            "small_plane_naval_bomber_airframe_3",
            "Leviathan Naval Bomber",
            "nav_bomber_equipment_3",
            100,
        ),
    )
    output = ["# AUTO-GENERATED: exactly 10,000 advanced Biotechnica aircraft.\n", "air_wings = {\n"]
    for state in AIR_STATES:
        output.append(f"\t{state} = {{\n")
        for bba_type, version, legacy_type, amount in aircraft:
            equipment = bba_type if bba else legacy_type
            version_text = f'\n\t\t\tversion_name = "{version}"' if bba else ""
            output.append(
                f"\t\t{equipment} = {{\n\t\t\towner = BIO\n\t\t\tamount = {amount}"
                f"{version_text}\n\t\t}}\n"
            )
        output.append(f'\t\tname = "Biotechnica Air Command {state}"\n\t}}\n')
    output.append("}\n")
    return "".join(output)


def main() -> None:
    UNITS.mkdir(parents=True, exist_ok=True)
    (UNITS / "BIO_2069_naval.txt").write_text(navy(True), encoding="utf-8")
    (UNITS / "BIO_2069_naval_legacy.txt").write_text(navy(False), encoding="utf-8")
    (UNITS / "BIO_2069_air_bba.txt").write_text(air_force(True), encoding="utf-8")
    (UNITS / "BIO_2069_air_legacy.txt").write_text(air_force(False), encoding="utf-8")
    print("Generated 160 naval counters / 800-vessel equivalent and 10,000 aircraft.")


if __name__ == "__main__":
    main()
