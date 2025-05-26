from mcresources.resource_manager import ResourceManager
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')
#ASSETS_DIR = os.path.join(RESOURCES_DIR, 'assets')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)
#os.makedirs(ASSETS_DIR, exist_ok=True)

rm.placed_feature('vein/vivianite', 'tfc_mineralogy:vein/vivianite')
#rm.configured_feature('vivianite')

### CREATE VIVIANITE FEATURE
rm.configured_feature('vein/vivianite', 'tfc:disc_vein', {'rarity': 110, 'density': 0.85, 'min_y': -45, 'max_y': -12, 'size': 8,'random_name': 'vivianite',
'blocks':[
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfc_mineralogy:ore/vivianite/rhyolite'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfc_mineralogy:ore/vivianite/basalt'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfc_mineralogy:ore/vivianite/andesite'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfc_mineralogy:ore/vivianite/dacite'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfc_mineralogy:ore/vivianite/quartzite'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfc_mineralogy:ore/vivianite/slate'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfc_mineralogy:ore/vivianite/phyllite'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfc_mineralogy:ore/vivianite/schist'}]},
    {'replace':['tfc:rock/raw/rhyolite'],'with':[{'block':'tfc_mineralogy:ore/vivianite/gneiss'}]},
    {'replace':['tfc:rock/raw/basalt'],'with':[{'block':'tfc_mineralogy:ore/vivianite/marble'}]}
]
})
rm.tag('vivianite','blocks/ores',
    'tfc_mineralogy:ore/vivianite/granite',
    'tfc_mineralogy:ore/vivianite/diorite',
    'tfc_mineralogy:ore/vivianite/gabbro',
    'tfc_mineralogy:ore/vivianite/shale',
    'tfc_mineralogy:ore/vivianite/claystone',
    'tfc_mineralogy:ore/vivianite/limestone',
    'tfc_mineralogy:ore/vivianite/conglomerate',
    'tfc_mineralogy:ore/vivianite/dolomite',
    'tfc_mineralogy:ore/vivianite/chert',
    'tfc_mineralogy:ore/vivianite/chalk',
    'tfc_mineralogy:ore/vivianite/rhyolite',
    'tfc_mineralogy:ore/vivianite/basalt',
    'tfc_mineralogy:ore/vivianite/andesite',
    'tfc_mineralogy:ore/vivianite/dacite',
    'tfc_mineralogy:ore/vivianite/quartzite',
    'tfc_mineralogy:ore/vivianite/slate',
    'tfc_mineralogy:ore/vivianite/phyllite',
    'tfc_mineralogy:ore/vivianite/schist',
    'tfc_mineralogy:ore/vivianite/gneiss',
    'tfc_mineralogy:ore/vivianite/marble')

rm.flush()
### Add Veins here to the worldgen tags as a value
rm_tfc.tag('veins','worldgen\placed_feature\in_biome','tfc_mineralogy:vein/vivianite')
### Add prospectables to the list
rm_tfc.tag('prospectable','blocks','tfc_mineralogy:ore/vivianite/granite',
    'tfc_mineralogy:ore/vivianite/diorite',
    'tfc_mineralogy:ore/vivianite/gabbro',
    'tfc_mineralogy:ore/vivianite/shale',
    'tfc_mineralogy:ore/vivianite/claystone',
    'tfc_mineralogy:ore/vivianite/limestone',
    'tfc_mineralogy:ore/vivianite/conglomerate',
    'tfc_mineralogy:ore/vivianite/dolomite',
    'tfc_mineralogy:ore/vivianite/chert',
    'tfc_mineralogy:ore/vivianite/chalk',
    'tfc_mineralogy:ore/vivianite/rhyolite',
    'tfc_mineralogy:ore/vivianite/basalt',
    'tfc_mineralogy:ore/vivianite/andesite',
    'tfc_mineralogy:ore/vivianite/dacite',
    'tfc_mineralogy:ore/vivianite/quartzite',
    'tfc_mineralogy:ore/vivianite/slate',
    'tfc_mineralogy:ore/vivianite/phyllite',
    'tfc_mineralogy:ore/vivianite/schist',
    'tfc_mineralogy:ore/vivianite/gneiss',
    'tfc_mineralogy:ore/vivianite/marble')

rm_tfc.tag('can_start_collapse','blocks','tfc_mineralogy:ore/vivianite/granite',
    'tfc_mineralogy:ore/vivianite/diorite',
    'tfc_mineralogy:ore/vivianite/gabbro',
    'tfc_mineralogy:ore/vivianite/shale',
    'tfc_mineralogy:ore/vivianite/claystone',
    'tfc_mineralogy:ore/vivianite/limestone',
    'tfc_mineralogy:ore/vivianite/conglomerate',
    'tfc_mineralogy:ore/vivianite/dolomite',
    'tfc_mineralogy:ore/vivianite/chert',
    'tfc_mineralogy:ore/vivianite/chalk',
    'tfc_mineralogy:ore/vivianite/rhyolite',
    'tfc_mineralogy:ore/vivianite/basalt',
    'tfc_mineralogy:ore/vivianite/andesite',
    'tfc_mineralogy:ore/vivianite/dacite',
    'tfc_mineralogy:ore/vivianite/quartzite',
    'tfc_mineralogy:ore/vivianite/slate',
    'tfc_mineralogy:ore/vivianite/phyllite',
    'tfc_mineralogy:ore/vivianite/schist',
    'tfc_mineralogy:ore/vivianite/gneiss',
    'tfc_mineralogy:ore/vivianite/marble')

rm_tfc.tag('can_collapse','blocks','tfc_mineralogy:ore/vivianite/granite',
    'tfc_mineralogy:ore/vivianite/diorite',
    'tfc_mineralogy:ore/vivianite/gabbro',
    'tfc_mineralogy:ore/vivianite/shale',
    'tfc_mineralogy:ore/vivianite/claystone',
    'tfc_mineralogy:ore/vivianite/limestone',
    'tfc_mineralogy:ore/vivianite/conglomerate',
    'tfc_mineralogy:ore/vivianite/dolomite',
    'tfc_mineralogy:ore/vivianite/chert',
    'tfc_mineralogy:ore/vivianite/chalk',
    'tfc_mineralogy:ore/vivianite/rhyolite',
    'tfc_mineralogy:ore/vivianite/basalt',
    'tfc_mineralogy:ore/vivianite/andesite',
    'tfc_mineralogy:ore/vivianite/dacite',
    'tfc_mineralogy:ore/vivianite/quartzite',
    'tfc_mineralogy:ore/vivianite/slate',
    'tfc_mineralogy:ore/vivianite/phyllite',
    'tfc_mineralogy:ore/vivianite/schist',
    'tfc_mineralogy:ore/vivianite/gneiss',
    'tfc_mineralogy:ore/vivianite/marble')
rm_tfc.flush()

rm_forge.tag('ores','blocks','#forge:ores/vivianite')
rm_forge.tag('vivianite','blocks/ores','#tfc_mineralogy:ores/vivianite')
rm_forge.flush()

### Add Loot Tables for ores
rm.block_loot('slate','tfc_mineralogy:vivianite')
rm.block_loot('shale','tfc_mineralogy:vivianite')
rm.block_loot('schist','tfc_mineralogy:vivianite')
rm.block_loot('rhyolite','tfc_mineralogy:vivianite')
rm.block_loot('quartzite','tfc_mineralogy:vivianite')
rm.block_loot('phyllite','tfc_mineralogy:vivianite')
rm.block_loot('marble','tfc_mineralogy:vivianite')
rm.block_loot('limestone','tfc_mineralogy:vivianite')
rm.block_loot('granite','tfc_mineralogy:vivianite')
rm.block_loot('gneiss','tfc_mineralogy:vivianite')
rm.block_loot('gabbro','tfc_mineralogy:vivianite')
rm.block_loot('dolomite','tfc_mineralogy:vivianite')
rm.block_loot('diorite','tfc_mineralogy:vivianite')
rm.block_loot('dacite','tfc_mineralogy:vivianite')
rm.block_loot('conglomerate','tfc_mineralogy:vivianite')
rm.block_loot('claystone','tfc_mineralogy:vivianite')
rm.block_loot('chert','tfc_mineralogy:vivianite')
rm.block_loot('chalk','tfc_mineralogy:vivianite')
rm.block_loot('basalt','tfc_mineralogy:vivianite')
rm.block_loot('andesite','tfc_mineralogy:vivianite')
rm.flush()

#rm_assets = ResourceManager(domain='tfc_mineralogy', resource_dir=ASSETS_DIR, indent=2, ensure_ascii=False)
#rm_assets.blockstate()
rm.blockstate('ore/vivianite/slate','tfc_mineralogy:block/ore/vivianite/slate')
rm.blockstate('ore/vivianite/shale','tfc_mineralogy:block/ore/vivianite/shale')
rm.blockstate('ore/vivianite/schist','tfc_mineralogy:block/ore/vivianite/schist')
rm.blockstate('ore/vivianite/rhyolite','tfc_mineralogy:block/ore/vivianite/rhyolite')
rm.blockstate('ore/vivianite/quartzite','tfc_mineralogy:block/ore/vivianite/quartzite')
rm.blockstate('ore/vivianite/phyllite','tfc_mineralogy:block/ore/vivianite/phyllite')
rm.blockstate('ore/vivianite/marble','tfc_mineralogy:block/ore/vivianite/marble')
rm.blockstate('ore/vivianite/limestone','tfc_mineralogy:block/ore/vivianite/limestone')
rm.blockstate('ore/vivianite/granite','tfc_mineralogy:block/ore/vivianite/granite')
rm.blockstate('ore/vivianite/gneiss','tfc_mineralogy:block/ore/vivianite/gneiss')
rm.blockstate('ore/vivianite/gabbro','tfc_mineralogy:block/ore/vivianite/gabbro')
rm.blockstate('ore/vivianite/dolomite','tfc_mineralogy:block/ore/vivianite/dolomite')
rm.blockstate('ore/vivianite/diorite','tfc_mineralogy:block/ore/vivianite/diorite')
rm.blockstate('ore/vivianite/dacite','tfc_mineralogy:block/ore/vivianite/dacite')
rm.blockstate('ore/vivianite/conglomerate','tfc_mineralogy:block/ore/vivianite/conglomerate')
rm.blockstate('ore/vivianite/claystone','tfc_mineralogy:block/ore/vivianite/claystone')
rm.blockstate('ore/vivianite/chert','tfc_mineralogy:block/ore/vivianite/chert')
rm.blockstate('ore/vivianite/chalk','tfc_mineralogy:block/ore/vivianite/chalk')
rm.blockstate('ore/vivianite/basalt','tfc_mineralogy:block/ore/vivianite/basalt')
rm.blockstate('ore/vivianite/andesite','tfc_mineralogy:block/ore/vivianite/andesite')
rm.flush()

### Add Lang
rm.lang('item.tfc_mineralogy.ore.vivianite', 'Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.slate', 'Slate Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.shale', 'Shale Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.schist', 'Schist Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.rhyolite', 'Rhyolite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.quartzite', 'Quartzite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.phyllite', 'Phyllite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.marble', 'Marble Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.limestone', 'Limestone Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.granite', 'Granite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.gneiss', 'Gneiss Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.gabbro', 'Gabbro Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.dolomite', 'Dolomite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.diorite', 'Diorite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.dacite', 'Dacite Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.conglomerate', 'Conglomerate Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.claystone', 'Claystone Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.chert', 'Chert Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.chalk', 'Chalk Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.basalt', 'Basalt Vivianite')
rm.lang('block.tfc_mineralogy.ore.vivianite.andesite', 'Andesite Vivianite')
rm.flush()

rm.block_model('ore/vivianite/slate', {'all':'tfc:block/rock/raw/slate','particle':'tfc:block/rock/raw/slate','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/shale', {'all':'tfc:block/rock/raw/shale','particle':'tfc:block/rock/raw/shale','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/schist', {'all':'tfc:block/rock/raw/schist','particle':'tfc:block/rock/raw/schist','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/rhyolite', {'all':'tfc:block/rock/raw/rhyolite','particle':'tfc:block/rock/raw/rhyolite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/quartzite', {'all':'tfc:block/rock/raw/quartzite','particle':'tfc:block/rock/raw/quartzite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/phyllite', {'all':'tfc:block/rock/raw/phyllite','particle':'tfc:block/rock/raw/phyllite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/marble', {'all':'tfc:block/rock/raw/marble','particle':'tfc:block/rock/raw/marble','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/limestone', {'all':'tfc:block/rock/raw/limestone','particle':'tfc:block/rock/raw/limestone','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/granite', {'all':'tfc:block/rock/raw/granite','particle':'tfc:block/rock/raw/granite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/gneiss', {'all':'tfc:block/rock/raw/gneiss','particle':'tfc:block/rock/raw/gneiss','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/gabbro', {'all':'tfc:block/rock/raw/gabbro','particle':'tfc:block/rock/raw/gabbro','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/dolomite', {'all':'tfc:block/rock/raw/dolomite','particle':'tfc:block/rock/raw/dolomite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/diorite', {'all':'tfc:block/rock/raw/diorite','particle':'tfc:block/rock/raw/diorite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/dacite', {'all':'tfc:block/rock/raw/dacite','particle':'tfc:block/rock/raw/dacite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/conglomerate', {'all':'tfc:block/rock/raw/conglomerate','particle':'tfc:block/rock/raw/conglomerate','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/claystone', {'all':'tfc:block/rock/raw/claystone','particle':'tfc:block/rock/raw/claystone','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/chert', {'all':'tfc:block/rock/raw/chert','particle':'tfc:block/rock/raw/chert','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/chalk', {'all':'tfc:block/rock/raw/chalk','particle':'tfc:block/rock/raw/chalk','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/basalt', {'all':'tfc:block/rock/raw/basalt','particle':'tfc:block/rock/raw/basalt','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.block_model('ore/vivianite/andesite', {'all':'tfc:block/rock/raw/andesite','particle':'tfc:block/rock/raw/andesite','overlay':'tfc_mineralogy:block/ore/vivianite'})
rm.flush()

### Add item models
rm.item_model('ore/vivianite','tfc_mineralogy:item/ore/vivianite')
rm.item_model('ore/vivianite/slate', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/slate')
rm.item_model('ore/vivianite/shale', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/shale')
rm.item_model('ore/vivianite/schist', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/schist')
rm.item_model('ore/vivianite/rhyolite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/rhyolite')
rm.item_model('ore/vivianite/quartzite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/quartzite')
rm.item_model('ore/vivianite/phyllite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/phyllite')
rm.item_model('ore/vivianite/marble', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/marble')
rm.item_model('ore/vivianite/limestone', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/limestone')
rm.item_model('ore/vivianite/granite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/granite')
rm.item_model('ore/vivianite/gneiss', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/gneiss')
rm.item_model('ore/vivianite/gabbro', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/gabbro')
rm.item_model('ore/vivianite/dolomite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/dolomite')
rm.item_model('ore/vivianite/diorite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/diorite')
rm.item_model('ore/vivianite/dacite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/dacite')
rm.item_model('ore/vivianite/conglomerate', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/conglomerate')
rm.item_model('ore/vivianite/claystone', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/claystone')
rm.item_model('ore/vivianite/chert', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/chert')
rm.item_model('ore/vivianite/chalk', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/chalk')
rm.item_model('ore/vivianite/basalt', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/basalt')
rm.item_model('ore/vivianite/andesite', no_textures=True, parent='tfc_mineralogy:block/ore/vivianite/andesite')
