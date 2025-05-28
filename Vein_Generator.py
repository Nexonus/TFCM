from mcresources.resource_manager import ResourceManager
import os
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils
from mcresources.recipe_context import RecipeContext
from typing import Sequence, Dict, Union, Optional, Callable, Any


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
stone_dict = {'diorite','gabbro','shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
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

rm.placed_feature(f'vein/{mineral_name}', f'tfcmineralogy:vein/{mineral_name}') # This is the vein we're looking for in configured feature
rm.configured_feature(f'vein/{mineral_name}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.65, 'min_y': 50, 'max_y': 90, 'size': 16,'random_name': f'{mineral_name}',
'blocks':[  # Comment the ones we don't want to use for the specific generation.
    # No Weights
    {'replace':['tfc:rock/raw/diorite'],'with':[{'block':f'tfcmineralogy:ore/diorite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/gabbro'],'with':[{'block':f'tfcmineralogy:ore/gabbro_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/shale'],'with':[{'block':f'tfcmineralogy:ore/shale_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/claystone'],'with':[{'block':f'tfcmineralogy:ore/claystone_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/limestone'],'with':[{'block':f'tfcmineralogy:ore/limestone_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/conglomerate'],'with':[{'block':f'tfcmineralogy:ore/conglomerate_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/dolomite'],'with':[{'block':f'tfcmineralogy:ore/dolomite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/chert'],'with':[{'block':f'tfcmineralogy:ore/chert_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/chalk'],'with':[{'block':f'tfcmineralogy:ore/chalk_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':f'tfcmineralogy:ore/rhyolite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':f'tfcmineralogy:ore/basalt_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/andesite'],'with':[{'block':f'tfcmineralogy:ore/andesite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/dacite'],'with':[{'block':f'tfcmineralogy:ore/dacite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/quartzite'],'with':[{'block':f'tfcmineralogy:ore/quartzite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/slate'],'with':[{'block':f'tfcmineralogy:ore/slate_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/phyllite'],'with':[{'block':f'tfcmineralogy:ore/phyllite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/schist'],'with':[{'block':f'tfcmineralogy:ore/schist_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/gneiss'],'with':[{'block':f'tfcmineralogy:ore/gneiss_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/marble'],'with':[{'block':f'tfcmineralogy:ore/marble_{mineral_name}'}]}
]
})
for stone in stone_dict:
    rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:ore/{stone}_{mineral_name}')
    tfcm_prospectables.add(f'tfcmineralogy:ore/{stone}_{mineral_name}')
    tfcm_can_collapse.add(f'tfcmineralogy:ore/{stone}_{mineral_name}')
    tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{stone}_{mineral_name}')

### MODEL : INCLUDING WEIGHTS (POOR, NORMAL, RICH)
mineral_name = 'smithsonite'
qualities = ['poor','normal','rich']
weight = [50, 35, 15]
resource_list = list()
downgraded_quality = ''
for q in qualities:
    mineral_quality = q+'_'+mineral_name
    resource_list.append(mineral_quality)   # Populate list here
for q in qualities:
    mineral_quality = q+'_'+mineral_name
    vein_feature_names.add(f'vein/{mineral_quality}')
    tfcm_veins.add(f'tfcmineralogy:vein/{mineral_quality}')
    forge_ores.add(f'#forge:ores/{mineral_quality}')
    rm.placed_feature(f'vein/{mineral_quality}', f'tfcmineralogy:vein/{mineral_quality}') # This is the vein we're looking for in configured feature
    rm.configured_feature(f'vein/{mineral_quality}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.3, 'min_y': 30, 'max_y': 120, 'size': 22,'random_name': f'{mineral_quality}',
    'blocks':
    [   # With Weights Applied
    {'replace':['tfc:rock/raw/diorite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/diorite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/diorite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/diorite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/gabbro'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/gabbro_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/gabbro_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/gabbro_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/shale'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/shale_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/shale_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/shale_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/claystone'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/claystone_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/claystone_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/claystone_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/limestone'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/limestone_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/limestone_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/limestone_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/conglomerate'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/conglomerate_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/conglomerate_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/conglomerate_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/dolomite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/dolomite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/dolomite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/dolomite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/chert'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/chert_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/chert_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/chert_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/chalk'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/chalk_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/chalk_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/chalk_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/rhyolite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/rhyolite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/rhyolite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/basalt_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/basalt_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/basalt_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/andesite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/andesite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/andesite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/andesite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/dacite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/dacite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/dacite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/dacite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/quartzite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/quartzite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/quartzite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/quartzite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/slate'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/slate_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/slate_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/slate_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/phyllite'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/phyllite_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/phyllite_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/phyllite_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/schist'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/schist_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/schist_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/schist_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/gneiss'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/gneiss_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/gneiss_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/gneiss_{resource_list[2]}'}]},
    {'replace':['tfc:rock/raw/marble'],'with':[{'weight':f'{weight[0]}','block':f'tfcmineralogy:ore/marble_{resource_list[0]}'},{'weight':f'{weight[1]}','block':f'tfcmineralogy:ore/marble_{resource_list[1]}'},{'weight':f'{weight[2]}','block':f'tfcmineralogy:ore/marble_{resource_list[2]}'}]}
    ]})
    for stone in stone_dict:
        rm_forge.tag(f'{mineral_quality}','blocks/ores', f'tfcmineralogy:ore/{stone}_{mineral_quality}')
        tfcm_prospectables.add(f'tfcmineralogy:ore/{stone}_{mineral_quality}')
        tfcm_can_collapse.add(f'tfcmineralogy:ore/{stone}_{mineral_quality}')
        tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{stone}_{mineral_quality}')
        match(q):
            case 'rich':
                current_quality='rich'
                downgraded_quality='normal'
                rm.collapse_recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}',f'tfcmineralogy:ore/{stone}_{current_quality}_{mineral_name}',f'tfcmineralogy:ore/{stone}_{downgraded_quality}_{mineral_name}')
            case 'normal':
                current_quality='normal'
                downgraded_quality='poor'
                rm.collapse_recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}',f'tfcmineralogy:ore/{stone}_{current_quality}_{mineral_name}',f'tfcmineralogy:ore/{stone}_{downgraded_quality}_{mineral_name}')
            case 'poor':
                current_quality='poor'
                downgraded_quality='cobble'
                rm.collapse_recipe(f'collapse/{stone}_cobble',f'tfcmineralogy:ore/{stone}_{current_quality}_{mineral_name}',f'tfc:rock/cobble/{stone}')

rm_tfc.tag('veins','worldgen/placed_feature/in_biome',*tfcm_veins)
rm_tfc.tag('prospectable','blocks',*tfcm_prospectables)
rm_tfc.tag('can_start_collapse','blocks',*tfcm_can_start_collapse)
rm_tfc.tag('can_collapse','blocks',*tfcm_can_collapse)
rm_forge.tag('ores','blocks',*forge_ores)
rm_tfc.flush()
rm_forge.flush()
rm.flush()

