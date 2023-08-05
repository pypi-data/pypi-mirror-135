import pathlib
from pathlib import Path
from typing import Dict, Tuple

from gdsfactory.component import Component
from gdsfactory.config import CONFIG
from gdsfactory.name import dict2name, get_name_short
from gdsfactory.tech import LAYER
from gdsfactory.types import SimulationSuffix


def get_sparameters_path(
    component: Component,
    layer_to_material: Dict[Tuple[int, int], str],
    layer_to_thickness: Dict[Tuple[int, int], int],
    dirpath: Path = CONFIG["sparameters"],
    suffix: SimulationSuffix = ".dat",
    **kwargs,
) -> Path:
    """Returns Sparameters filepath.

    it only includes the layers that are present in the component

    Args:
        component:
        layer_to_material: GDSlayer tuple to material alias
        layer_to_thickness: GDSlayer tuple to thickness (nm)
        dirpath:
        suffix: .dat for interconnect
        kwargs: simulation settings
    """
    dirpath = pathlib.Path(dirpath)
    dirpath = (
        dirpath / component.function_name
        if hasattr(component, "function_name")
        else dirpath
    )
    dirpath.mkdir(exist_ok=True, parents=True)
    material_to_thickness = {
        layer_to_material[layer]: layer_to_thickness[layer]
        for layer in layer_to_thickness.keys()
        if tuple(layer) in component.get_layers()
    }
    material_to_thickness.update(**kwargs)
    name_suffix = get_name_short(dict2name(**material_to_thickness))
    return dirpath / f"{component.name}_{name_suffix}{suffix}"


def test_get_sparameters_path() -> None:
    import gdsfactory as gf

    layer_to_thickness_sample = {
        LAYER.WG: 220e-3,
        LAYER.SLAB90: 90e-3,
    }
    layer_to_material_sample = {
        LAYER.WG: "si",
        LAYER.SLAB90: "si",
    }

    c = gf.components.straight()
    p = get_sparameters_path(
        component=c,
        layer_to_thickness=layer_to_thickness_sample,
        layer_to_material=layer_to_material_sample,
    )
    assert p.stem == f"{c.name}_si220n", p.stem

    c = gf.components.straight(layer=LAYER.SLAB90)
    p = get_sparameters_path(
        c,
        layer_to_thickness=layer_to_thickness_sample,
        layer_to_material=layer_to_material_sample,
    )
    cell_name = f"{c.name}_si90n"
    assert p.stem == cell_name, p.stem


if __name__ == "__main__":
    # import gdsfactory as gf
    # c = gf.components.straight()
    # p = get_sparameters_path(c)
    # print(p)

    test_get_sparameters_path()
