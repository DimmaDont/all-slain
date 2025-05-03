## Installing

### Pip
```bash
pip install "allslain @ git+https://github.com/DimmaDont/all-slain"
```

### pyproject.toml
```
[project]
dependencies = [
    "allslain @ git+https://github.com/DimmaDont/all-slain",

    # or with commit hash
    "allslain @ git+https://github.com/DimmaDont/all-slain@COMMIT_HASH_HERE",
]
```


## Usage Examples

### Getting Actor Names
```python
from allslain.data.actors import ACTORS

actor_name: str | None = ACTORS.get("PU_Human_Enemy_GroundCombat_NPC_Ninetails_juggernaut")
```

### Getting Location Names
```python
from allslain.data.locations import LOCATIONS

location: str | tuple[str, str] | None = LOCATIONS.get("pyro6")
if isinstance(location, tuple):
    location_preposition, location_name = location
else:
    location_name: str | None = location
```

### Getting FPS Weapon Names
```python
from allslain.data.weapons_fps import WEAPONS_FPS

fps_weapon_name: str = WEAPONS_FPS.get("behr_rifle_ballistic_01")
```

### Getting Ship Weapon Names
```python
from allslain.data.weapons_ship import WEAPONS_SHIP

ship_weapon_name: str = WEAPONS_SHIP.get("KLWE_LaserRepeater_S2")
```

### Getting Latest Game Log File
Install `allslain[launcher_store]`, e.g. `pip install "allslain[launcher_store] @ git+https://github.com/DimmaDont/all-slain"`

```python
from allslain.launcher_store import get_log

log_path = get_log()
if log_path is None:
    ...
with open(log_path) as f:
    ...
```

## Other Usable Bits of Code
See `allslain.functions`.


## Attribution
**all-slain** is released under the [MIT License](LICENSE).

While not required, we greatly appreciate attribution for this work.

If this project is used in your work, please cite this project as:
```
all-slain: A Star Citizen Game Log Reader (https://github.com/DimmaDont/all-slain)
```
or something otherwise similar. Even just a link would be great.


## Contribution
If you improve or extend this work, we encourage you to share your enhancements.

See [CONTRIBUTING.md](CONTRIBUTING.md).

Your contributions help make all-slain even better for the Star Citizen community!
