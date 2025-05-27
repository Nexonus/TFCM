from mcresources.resource_manager import ResourceManager
import os
import json 

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

### CREATE AN ORE GEN FEATURE
resource_list = {'example_block'} #Usage vivianite,kaolinite,etc. 
vein_feature_names = set()
tfcm_veins = set()
tfcm_prospectables = set()
forge_ores = set()
for mineral_name in resource_list:
    vein_feature_names.add(f'vein/{mineral_name}')
    tfcm_veins.add(f'tfcmineralogy:vein/{mineral_name}')
    tfcm_prospectables.add(f'tfcmineralogy:{mineral_name}')
    forge_ores.add(f'#forge:ores/{mineral_name}')
    
    rm.placed_feature(f'vein/{mineral_name}', f'tfcmineralogy:vein/{mineral_name}') # This is the vein we're looking for in configured feature
    rm.configured_feature(f'vein/{mineral_name}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.2, 'min_y': -120, 'max_y': 120, 'size': 16,'random_name': f'{mineral_name}',
    'blocks':[  # Comment the ones we don't want to use for the generation.
        {'replace':['tfc:rock/raw/diorite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/gabbro'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/shale'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/claystone'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/limestone'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/conglomerate'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/dolomite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/chert'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/chalk'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/basalt'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/andesite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/dacite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/quartzite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/slate'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/phyllite'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/schist'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/gneiss'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]},
        {'replace':['tfc:rock/raw/marble'],'with':[{'block':f'tfcmineralogy:{mineral_name}'}]}
    ]
    })
    rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:{mineral_name}')
    

rm.flush()
rm_forge.flush()

rm_tfc.tag('veins','worldgen/placed_feature/in_biome',*tfcm_veins)
rm_tfc.tag('prospectable','blocks',*tfcm_prospectables)
rm_forge.tag('ores','blocks',*forge_ores)
rm_tfc.flush()
rm_forge.flush()

"""
rm_tfc.tag('veins','worldgen/placed_feature/in_biome',f'tfcmineralogy:vein/{mineral_name}')
rm_tfc.tag('prospectable','blocks',f'tfcmineralogy:{mineral_name}')
rm_forge.tag('ores','blocks',f'#forge:ores/{mineral_name}')
rm_tfc.flush()
rm_forge.flush()
"""


#rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:{mineral_name}')
#rm_forge.tag('ores','blocks',f'#forge:ores/{mineral_name}')
#rm_forge.flush()

