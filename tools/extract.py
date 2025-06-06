import json
from typing import Any


def is_flight_ready(item: dict[str, str]) -> bool:
    return "flightReady" in item["tags"].split()


def get_item_name(labels: dict[str, str], item_name_ref: str):
    name = labels.get(item_name_ref) or labels.get("item_Name" + item_name_ref)
    if name:
        if "PLACEHOLDER" in name:
            raise KeyError()
        return name.replace("\xa0", " ").strip()
    raise KeyError()


def get_item_name_ship_weapon(labels: dict[str, str], item_name_ref: str):
    if item_name_ref.startswith("@"):
        item_name_ref = item_name_ref[1:]
    name = labels.get(item_name_ref) or labels.get("item_Name" + item_name_ref)
    if name:
        if "PLACEHOLDER" in name:
            raise KeyError()
        return (
            name.strip()
            .replace("\xa0", " ")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2019", "'")
        )
    raise KeyError()


def get_ships(data: dict) -> dict:
    ships = {}
    for ship in data:
        ship_class_name = ship["ClassName"]
        ship_name = ship["Name"].strip()
        if ship_class_name.endswith("_Temp"):
            continue
        if ship_class_name.endswith("_Indestructible"):
            continue
        if ship_class_name.endswith("_NineTails"):
            ships[ship_class_name] = ship_name + " (NineTails)"
        elif ship_class_name.endswith("_Unmanned_Salvage"):
            ships[ship_class_name] = ship_name + " (Salvage)"
        elif "BIS" in ship_class_name:
            ships[ship_class_name] = ship_name + " (BIS)"
        elif ship_class_name.endswith("_Tutorial"):
            # Tutorial C8
            ships[ship_class_name] = ship_name + " (Tutorial)"
        else:
            ships[ship_class_name] = ship_name
    return ships


def get_locations(labels: dict[str, str]) -> dict:
    locations = {}
    for k, v in labels.items():
        if not (
            k.startswith("Stanton")
            or k.startswith("Pyro")
            or k.startswith("RR_")
            or (k.startswith("ui_pregame_port_") and k.endswith("_name"))
        ):
            continue
        k_lower = k.lower()
        if any(
            [
                k_lower.endswith("_desc"),
                k_lower.endswith("_desc,p"),
                k_lower.endswith("_desc_shared"),
                k_lower.endswith("_desc_shared"),
                k_lower.endswith("_add"),
                k_lower.endswith("_entrance"),
            ]
        ):
            continue
        locations[k.rstrip(",P")] = v.replace("\xa0", "").strip()
    return locations


def dump_to_file(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(
            "X = "
            + json.dumps(
                dict(sorted(data.items(), key=lambda x: x[0].lower())), indent=4
            )
        )


def main(directory: str):
    with open(directory + "v2/ships.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        ships = get_ships(data)

    with open(directory + "labels.json", "r", encoding="utf-8") as f:
        labels: dict[str, str] = json.loads(f.read())
        locations = get_locations(labels)

    weapons_fps = {}
    weapons_ship = {}
    with open(directory + "items.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        for item in data:
            # Non-ship ships
            if item["type"] == "AIModule":
                if any(
                    [
                        item["className"].startswith("test_"),
                        item["className"].startswith("SimpleOpenableObject_"),
                    ]
                ):
                    continue
                ships[item["className"]] = item["name"]

            # FPS Weapons
            elif item["type"] == "WeaponPersonal":
                # if item["className"] != item["itemName"]:
                #     print(item["className"], item["itemName"])
                if any(
                    [
                        item["className"].startswith("Carryable_"),
                        item["className"].startswith("grin_multitool_"),
                        item["className"].startswith("sasu_pistol_toy_"),
                        "_test_" in item["className"],
                    ]
                ):
                    continue
                try:
                    weapons_fps[item["className"]] = get_item_name(
                        labels,
                        (
                            item["name"][1:]
                            if item["name"].startswith("@")
                            else item["name"]
                        ),
                    )
                except KeyError:
                    print(f'Could not find item with name "{item["name"]}"')

            # Ship weapons
            elif item["type"] == "WeaponGun":
                # if item["className"] != item["itemName"]:
                #     print(f"{item["className"]}, {item["itemName"]}")
                if any(
                    [
                        item["className"].endswith("_LowPoly"),
                        item["className"].endswith("_Turret"),
                        "Tractor" in item["className"],
                        item["className"].endswith("_reference"),
                    ]
                ):
                    continue
                try:
                    weapons_ship[item["className"]] = get_item_name_ship_weapon(
                        labels, item["name"]
                    )
                except KeyError:
                    print(f'Could not find item with name "{item["name"]}"')
            elif item["type"] == "Bomb":
                try:
                    weapons_ship[item["className"]] = get_item_name_ship_weapon(
                        labels, item["name"]
                    )
                except KeyError:
                    print(f'Could not find item with name "{item["name"]}"')
            elif item["type"] == "BombLauncher":
                if "_TEMP_" in item["className"]:
                    continue
                try:
                    weapons_ship[item["className"]] = get_item_name_ship_weapon(
                        labels, item["name"]
                    )
                except KeyError:
                    print(f'Could not find item with name "{item["name"]}"')

    missileracks_ship = {}
    with open(directory + "ship-items.json", "r", encoding="utf-8") as f:
        items: dict[str, Any] = json.loads(f.read())
        for item in items:
            if item["classification"] != "Ship.MissileLauncher.MissileRack":
                continue
            if "_cap" in item["className"].lower():
                continue
            missileracks_ship[item["className"]] = labels.get(
                item["name"][1:],
                (
                    str(item["stdItem"].get("MissileRack", {}).get("Size", "?"))
                    + "x"
                    + str(item["stdItem"].get("MissileRack", {}).get("Count", "?"))
                ),
            )

    dump_to_file(ships, "src/data/ships.py")
    dump_to_file(weapons_fps, "src/data/weapons_fps.py")
    dump_to_file(weapons_ship, "src/data/weapons_ship.py")
    dump_to_file(locations, "src/data/locations_respawn.py")
    dump_to_file(missileracks_ship, "src/data/missileracks_ship.py")


if __name__ == "__main__":
    main("../LIVE_EXTRACT2/")
