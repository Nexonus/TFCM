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
mineral_dict = {'smithsonite'} #Usage vivianite,kaolinite,etc.
stone_dict = {'diorite','gabbro','shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
vein_feature_names = set()
tfcm_veins = set()
tfcm_prospectables = set()
forge_ores = set()
stone_mineral_vein_dict = set() # wip

### MODEL : NO WEIGHTS, SINGULAR MINERAL (HALITE ETC)
"""
for mineral_name in mineral_dict:
    vein_feature_names.add(f'vein/{mineral_name}')
    tfcm_veins.add(f'tfcmineralogy:vein/{mineral_name}')
    forge_ores.add(f'#forge:ores/{mineral_name}')

    rm.placed_feature(f'vein/{mineral_name}', f'tfcmineralogy:vein/{mineral_name}') # This is the vein we're looking for in configured feature
    rm.configured_feature(f'vein/{mineral_name}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.2, 'min_y': -120, 'max_y': 120, 'size': 16,'random_name': f'{mineral_name}',
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
"""
### MODEL : INCLUDING WEIGHTS (POOR, NORMAL, RICH)
mineral_name = 'smithsonite'
qualities = {'poor','normal','rich'}

weight_poor = {55, 30, 20}
weight_normal = {30, 40, 35}
weight_rich = {15, 30, 45}

for q in qualities:
    mineral_quality = q+mineral_name
    vein_feature_names.add(f'vein/{mineral_quality}')
    tfcm_veins.add(f'tfcmineralogy:vein/{mineral_quality}')
    forge_ores.add(f'#forge:ores/{mineral_quality}')
    rm.placed_feature(f'vein/{mineral_quality}', f'tfcmineralogy:vein/{mineral_quality}') # This is the vein we're looking for in configured feature
    rm.configured_feature(f'vein/{mineral_quality}', 'tfc:cluster_vein', {'rarity': 60, 'density': 0.2, 'min_y': -120, 'max_y': 120, 'size': 16,'random_name': f'{mineral_quality}',
'blocks':[  # Comment the ones we don't want to use for the specific generation.
    # Include Weights
    {'replace':['tfc:rock/raw/diorite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/diorite_{mineral_name}'},{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/diorite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/gabbro'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/gabbro_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/shale'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/shale_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/claystone'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/claystone_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/limestone'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/limestone_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/conglomerate'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/conglomerate_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/dolomite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/dolomite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/chert'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/chert_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/chalk'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/chalk_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/rhyolite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/basalt_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/andesite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/andesite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/dacite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/dacite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/quartzite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/quartzite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/slate'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/slate_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/phyllite'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/phyllite_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/schist'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/schist_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/gneiss'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/gneiss_{mineral_name}'}]},
    {'replace':['tfc:rock/raw/marble'],'with':[{'weight':f'{weight_poor}','block':f'tfcmineralogy:ore/marble_{mineral_name}'}]}
]
})
for stone in stone_dict:
    rm_forge.tag(f'{mineral_name}','blocks/ores', f'tfcmineralogy:ore/{stone}_{mineral_name}')
    tfcm_prospectables.add(f'tfcmineralogy:ore/{stone}_{mineral_name}')




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

