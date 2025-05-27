from mcresources.resource_manager import ResourceManager
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

rm.placed_feature('vein/example_block', 'tfcmineralogy:vein/example_block') # This is the vein we're looking for in configured feature

### CREATE VIVIANITE FEATURE
rm.configured_feature('vein/example_block', 'tfc:cluster_vein', {'rarity': 110, 'density': 0.85, 'min_y': -45, 'max_y': -12, 'size': 8,'random_name': 'example_block',
'blocks':[
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfcmineralogy:example_block'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:example_block'}]}
    #{'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfcmineralogy:ore/vivianite/marble'}]}
]
})
rm.flush()

rm_tfc.tag('veins','worldgen/placed_feature/in_biome','tfcmineralogy:vein/example_block')
rm_tfc.flush()