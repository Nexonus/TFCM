from mcresources.resource_manager import ResourceManager
import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

### CREATE AN ORE GEN FEATURE, NO TIERS
vein_feature_names = set()
tfcm_veins = set()
tfcm_prospectables = set()
tfcm_can_start_collapse = set()
tfcm_can_collapse = set()
tfcm_can_trigger_collapse = set()
forge_ores = set()
collapse_ingredients = set()
ingredient_minerals = set()


### MODEL : NO WEIGHTS, SINGULAR MINERAL (HALITE ETC)
mineral_name = 'vivianite'
vein_feature_names.add(f'vein/{mineral_name}')
tfcm_veins.add(f'tfcmineralogy:vein/{mineral_name}')
forge_ores.add(f'#forge:ores/{mineral_name}')
resource_generation = [] # Try to generate ore replacements here (for the json) to avoid spaghetti notation

# Configure which stones should the feature generate in here
#stone_generation_dict = {'quartzite','slate','phyllite','schist','gneiss','marble','granite','diorite','gabbro'} # Realgar
stone_generation_dict = {'chalk','limestone','dolomite','shale','claystone'} # Vivianite
stone_dict_full = {'diorite','gabbro', 'granite', 'shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 

#stone_dict = {'diorite','gabbro', 'granite', 'shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
for stone in stone_generation_dict:
    entry = ({
    'replace': [f'tfc:rock/raw/{stone}'],
    'with': [
        {'block': f'tfcmineralogy:ore/{mineral_name}/{stone}'}
    ]
    })
    resource_generation.append(entry)

rm.placed_feature(f'vein/{mineral_name}', f'tfcmineralogy:vein/{mineral_name}') # This is the vein we're looking for in configured feature
# Configured Feature: Cluster Vein, uncomment to use:
rm.configured_feature(f'vein/{mineral_name}', 'tfc:cluster_vein', {'rarity': 25, 'density': 0.15, 'min_y': 45, 'max_y': 80, 'biomes':'#tfc:is_river', 'size': 20,'random_name': f'{mineral_name}', # Vivianite
# Configured Feature: Disc Vein, uncomment to use:
#rm.configured_feature(f'vein/{mineral_name}', 'tfc:disc_vein', {'rarity': 4, 'density': 0.25, 'min_y': -64, 'max_y': -45, 'near_lava':True, 'size': 20, 'height':5, 'random_name': f'{mineral_name}', # Realgar-Orpiment
'blocks':resource_generation})

for stone in stone_dict_full:
    tfcm_prospectables.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    tfcm_can_collapse.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    tfcm_can_trigger_collapse.add(f'tfcmineralogy:ore/{mineral_name}/{stone}')
    rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:ore/{mineral_name}/{stone}')

    ingredient_minerals.add(mineral_name)


### MODEL : INCLUDING WEIGHTS (POOR, NORMAL, RICH)
mineral_name = 'galena'
qualities = ['poor','normal','rich']
weight = [15, 30, 55]
resource_list = list()
resource_generation = [] # Try to generate ore replacements here (for the json) to avoid spaghetti notation

downgraded_quality = ''
for q in qualities:
    mineral_quality = q+'_'+mineral_name
    resource_list.append(mineral_quality)   # Populate list here

# Configure which stones should the feature generate in here
stone_generation_dict = {'rhyolite','basalt','andesite','dacite','granite','diorite','gabbro'} 
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
    rm.configured_feature(f'vein/{mineral_quality}', 'tfc:cluster_vein', {'rarity': 28, 'density': 0.35, 'min_y': 40, 'max_y': 130, 'size': 20,'random_name': f'{mineral_quality}',
    'blocks':resource_generation})

    for stone in stone_dict_full:
        match(q):
            case 'rich':
                current_quality='rich'
                downgraded_quality='normal' # Format downgradedquality_stone_mineral
                collapse_input = {'ingredient': [f'tfcmineralogy:ore/{current_quality}_{mineral_name}/{stone}'], 'result':f'tfcmineralogy:ore/{downgraded_quality}_{mineral_name}/{stone}'}
                rm.recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}','tfc:collapse',collapse_input)
            case 'normal':
                current_quality='normal'
                downgraded_quality='poor'
                collapse_input = {'ingredient': [f'tfcmineralogy:ore/{current_quality}_{mineral_name}/{stone}'], 'result':f'tfcmineralogy:ore/{downgraded_quality}_{mineral_name}/{stone}'}
                rm.recipe(f'collapse/ore/{downgraded_quality}_{stone}_{mineral_name}','tfc:collapse',collapse_input)
            case 'poor':
                current_quality = 'poor'+'_'+mineral_name
                ingredient_minerals.add(current_quality)

    # Just make sure ALL the blocks are prospectable
    for stone in stone_dict_full:
        rm_forge.tag(f'{mineral_quality}','blocks/ores', f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_prospectables.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_can_collapse.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
        tfcm_can_trigger_collapse.add(f'tfcmineralogy:ore/{mineral_quality}/{stone}')

### MODEL : HYBRID, MULTI-ORE
mineral_list = ['realgar','orpiment']
weight = [35, 55]
resource_list = list()
resource_generation = [] # Try to generate ore replacements here (for the json) to avoid spaghetti notation

# Configure which stones should the feature generate in here
stone_generation_dict = {'quartzite','slate','phyllite','schist','gneiss','marble','granite','diorite','gabbro'} # Realgar-Orpiment
for stone in stone_generation_dict:
    entry = ({
    'replace': [f'tfc:rock/raw/{stone}'],
    'with': [
        {'weight': f'{weight[0]}', 'block': f'tfcmineralogy:ore/{mineral_list[0]}/{stone}'},
        {'weight': f'{weight[1]}', 'block': f'tfcmineralogy:ore/{mineral_list[1]}/{stone}'},
    ]
    })
    resource_generation.append(entry)

merged_vein_name = mineral_list[0]+"_"+mineral_list[1]
vein_feature_names.add(f'vein/{merged_vein_name}')
tfcm_veins.add(f'tfcmineralogy:vein/{merged_vein_name}')
rm.placed_feature(f'vein/{merged_vein_name}', f'tfcmineralogy:vein/{merged_vein_name}') # This is the vein we're looking for in configured feature
rm.configured_feature(f'vein/{merged_vein_name}', 'tfc:disc_vein', {'rarity': 7, 'density': 0.45, 'min_y': -64, 'max_y': -55, 'near_lava':True, 'size': 15, 'height':5, 'random_name': f'{merged_vein_name}', # Realgar-Orpiment
'blocks':resource_generation})

for mineral in mineral_list:
    forge_ores.add(f'#forge:ores/{mineral}')

    for stone in stone_dict_full:
        tfcm_prospectables.add(f'tfcmineralogy:ore/{mineral}/{stone}')
        tfcm_can_collapse.add(f'tfcmineralogy:ore/{mineral}/{stone}')
        tfcm_can_start_collapse.add(f'tfcmineralogy:ore/{mineral}/{stone}')
        tfcm_can_trigger_collapse.add(f'tfcmineralogy:ore/{mineral}/{stone}')
        rm_forge.tag(f'{mineral}','blocks/ores', f'tfcmineralogy:ore/{mineral}/{stone}')
        
        ingredient_minerals.add(mineral)

# Done, add the collapses and finish:

for stone in stone_dict_full:
    path = f'.\\src\\main\\resources\\data\\tfcmineralogy\\recipes\\collapse\\{stone}_cobble.json'
    if os.path.exists(path):
        file = open(path)
        fileData = json.load(file)
        for i in fileData['ingredient']:
            collapse_ingredients.add(i) # Load existing entries
        for min in ingredient_minerals:
            entry = f'tfcmineralogy:ore/{min}/{stone}'
            collapse_ingredients.add(entry)
    updated_ingredients = {'ingredient': [*collapse_ingredients], 'result':f'tfc:rock/cobble/{stone}'}
    rm.recipe(f'collapse/{stone}_cobble','tfc:collapse',updated_ingredients)
    collapse_ingredients = set()    # Currently requires to be run twice to generate the collapses, will fix later

rm_tfc.tag('veins','worldgen/placed_feature/in_biome',*tfcm_veins)
rm_tfc.tag('prospectable','blocks',*tfcm_prospectables)
rm_tfc.tag('can_start_collapse','blocks',*tfcm_can_start_collapse)
rm_tfc.tag('can_collapse','blocks',*tfcm_can_collapse)
rm_tfc.tag('can_trigger_collapse','blocks',*tfcm_can_trigger_collapse)
rm_forge.tag('ores','blocks',*forge_ores)
rm_tfc.flush()
rm_forge.flush()
rm.flush()

