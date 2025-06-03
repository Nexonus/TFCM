from mcresources.resource_manager import ResourceManager
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils
from typing import Sequence, Dict, Union, Optional, Callable, Any
from mcresources.block_context import BlockContext
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_mc = ResourceManager(domain='minecraft', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

