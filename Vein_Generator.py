from mcresources.resource_manager import ResourceManager
import os
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils
from mcresources.recipe_context import RecipeContext
from typing import Sequence, Dict, Union, Optional, Callable, Any
import json


# Modifying crafting_shapeless code by AlcatrazEscapee to match the collapse recipe
def collapse_recipe(self, name_parts: ResourceIdentifier, ingredients: Json, result: Json, group: str = None, conditions: Optional[Json] = None) -> RecipeContext:
        res = utils.resource_location(self.domain, name_parts)
        self.write(('data', res.domain, 'recipes', res.path), {
            'type': 'tfc:collapse',
            'group': group,
            'ingredient': ingredients,
            'result': result,
            'conditions': utils.recipe_condition(conditions)
        })
        return RecipeContext(self, res)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

ResourceManager.collapse_recipe = collapse_recipe # Add the modified method

### CREATE AN ORE GEN FEATURE, NO TIERS
vein_feature_names = set()
tfcm_veins = set()
tfcm_prospectables = set()
tfcm_can_start_collapse = set()
tfcm_can_collapse = set()
forge_ores = set()

### MODEL : NO WEIGHTS, SINGULAR MINERAL (HALITE ETC)
mineral_name = 'vivianite'
vein_feature_names.add(f'vein/{mineral_name}')
tfcm_veins.add(f'tfcmineralogy:vein/{mineral_name}')
forge_ores.add(f'#forge:ores/{mineral_name}')
resource_generation = [] # Try to generate ore replacements here (for the json) to avoid spaghetti notation

# Configure which stones should the feature generate in here
stone_generation_dict = {'chalk','limestone','dolomite','shale','claystone'} 
stone_dict_full = {'diorite','gabbro','shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 

#stone_dict = {'diorite','gabbro','shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
for stone in stone_generation_dict:
    entry = ({
    'replace': [f'tfc:rock/raw/{stone}'],
    'with': [
        {'block': f'tfcmineralogy:ore/{mineral_name}/{stone}'}
    ]
    })
    resource_generation.append(entry)

rm.placed_feature(f'vein/{mineral_name}', f'tfcmineralogy:vein/{mineral_name}') # This is the vein we're looking for in configured feature
rm.configured_feature(f'vein/{mineral_name}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.65, 'min_y': 50, 'max_y': 90, 'size': 16,'random_name': f'{mineral_name}',
'blocks':resource_generation})

for stone in stone_generation_dict:
    rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:ore/{mineral_name}/{stone}')
for stone in stone_dict_full:
    tfcm_prospectables.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    tfcm_can_collapse.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')

### MODEL : INCLUDING WEIGHTS (POOR, NORMAL, RICH)
mineral_name = 'smithsonite'
qualities = ['poor','normal','rich']
weight = [50, 35, 15]
resource_list = list()
resource_generation = [] # Try to generate ore replacements here (for the json) to avoid spaghetti notation

downgraded_quality = ''
for q in qualities:
    mineral_quality = q+'_'+mineral_name
    resource_list.append(mineral_quality)   # Populate list here

# Configure which stones should the feature generate in here
stone_generation_dict = {'limestone','marble','dolomite','chalk'} 
for stone in stone_generation_dict:
    entry = ({
    'replace': [f'tfc:rock/raw/{stone}'],
    'with': [
        {'weight': f'{weight[0]}', 'block': f'tfcmineralogy:ore/{resource_list[0]}/{stone}'},
        {'weight': f'{weight[1]}', 'block': f'tfcmineralogy:ore/{resource_list[1]}/{stone}'},
        {'weight': f'{weight[2]}', 'block': f'tfcmineralogy:ore/{resource_list[2]}/{stone}'}
    ]
    })
    resource_generation.append(entry)

for q in qualities:
    mineral_quality = q+'_'+mineral_name
    vein_feature_names.add(f'vein/{mineral_quality}')
    tfcm_veins.add(f'tfcmineralogy:vein/{mineral_quality}')
    forge_ores.add(f'#forge:ores/{mineral_quality}')
    rm.placed_feature(f'vein/{mineral_quality}', f'tfcmineralogy:vein/{mineral_quality}') # This is the vein we're looking for in configured feature
    rm.configured_feature(f'vein/{mineral_quality}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.3, 'min_y': 30, 'max_y': 120, 'size': 22,'random_name': f'{mineral_quality}',
    'blocks':resource_generation})

    for stone in stone_generation_dict:
        rm_forge.tag(f'{mineral_quality}','blocks/ores', f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        match(q):
            case 'rich':
                current_quality='rich'
                downgraded_quality='normal' # Format downgradedquality_stone_mineral
                rm.collapse_recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}',f'tfcmineralogy:ore/{current_quality}_{mineral_name}/{stone}',f'tfcmineralogy:ore/{downgraded_quality}_{mineral_name}/{stone}')
            case 'normal':
                current_quality='normal'
                downgraded_quality='poor'
                rm.collapse_recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}',f'tfcmineralogy:ore/{current_quality}_{mineral_name}/{stone}',f'tfcmineralogy:ore/{downgraded_quality}_{mineral_name}/{stone}')
            case 'poor':
                current_quality='poor'
                downgraded_quality='cobble'
                rm.collapse_recipe(f'collapse/{stone}_cobble',f'tfcmineralogy:ore/{current_quality}_{mineral_name}/{stone}',f'tfc:rock/cobble/{stone}')

    # Just make sure ALL the blocks are prospectable
    for stone in stone_dict_full:
        tfcm_prospectables.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_can_collapse.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')

rm_tfc.tag('veins','worldgen/placed_feature/in_biome',*tfcm_veins)
rm_tfc.tag('prospectable','blocks',*tfcm_prospectables)
rm_tfc.tag('can_start_collapse','blocks',*tfcm_can_start_collapse)
rm_tfc.tag('can_collapse','blocks',*tfcm_can_collapse)
rm_forge.tag('ores','blocks',*forge_ores)
rm_tfc.flush()
rm_forge.flush()
rm.flush()

