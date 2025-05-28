from mcresources.resource_manager import ResourceManager
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils
from typing import Sequence, Dict, Union, Optional, Callable, Any
from mcresources.block_context import BlockContext
import os

def _loot(self, name_parts: ResourceIdentifier, *loot_pools: Json, path: str, loot_type: str) -> ResourceLocation:
        # Fixing a typo in the loot table generation, original code by AlactrazEscapee
        res = utils.resource_location(self.domain, name_parts)
        self.write(('data', res.domain, 'loot_tables', path, res.path), { # *loot_tables* plural
            'type': loot_type,
            'pools': [
                utils.loot_pool(pool, path)
                for pool in loot_pools
            ]
        })
        return res
# Adding RenderType to fix transparency problems with minecraft:cutout rendering
def _block_model(self, name_parts: ResourceIdentifier, textures: Union[Dict[str, str], Sequence[str]] = None, parent: Union[str, None] = 'block/cube_all', render: Union[str, None] = 'minecraft:solid', elements: Json = None, no_textures: bool = False) -> BlockContext:
        res = utils.resource_location(self.domain, name_parts)
        if textures is None:
            if not no_textures:
                textures = {'all': res.join('block/')}
        elif isinstance(textures, str):
            textures = {'all': textures}
        elif isinstance(textures, Sequence):
            textures = dict((k, res.join('block')) for k in textures)
        if isinstance(elements, Dict):
            elements = [elements]
        self.write(('assets', res.domain, 'models', 'block', res.path), {
            'parent': parent,
            'render_type': render,
            'textures': textures,
            'elements': elements
        })
        return BlockContext(self, res)
ResourceManager.block_model = _block_model
ResourceManager.loot = _loot

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_mc = ResourceManager(domain='minecraft', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

mineral_dict = {'smithsonite'} 
stone_dict = {'diorite','gabbro','shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
ore_quality = {'poor','normal','rich'}
lang_dict = set()
prospect_lang_dict = set()
# For ores with no Qualities
"""
for mineral in mineral_dict:
    for stone in stone_dict:
        rm.block_loot(f'ore/{mineral}/{stone}',{'name': f'tfcmineralogy:ore/{stone}_{mineral}'})
        rm.flush()

        rm_mc.tag('needs_iron_tool','blocks',f'tfcmineralogy:ore/{stone}_{mineral}')
        rm_mc.tag('pickaxe','blocks/mineable',f'tfcmineralogy:ore/{stone}_{mineral}')
        rm_mc.flush()

        rm.blockstate(f'tfcmineralogy:ore/{stone}_{mineral}')
        rm.block_model(f'tfcmineralogy:ore/{stone}_{mineral}',{'all':f'tfc:block/rock/raw/{stone}','particle':f'tfc:block/rock/raw/{stone}','overlay':f'tfcmineralogy:block/ore/{mineral}'}, parent='tfc:block/ore', render='minecraft:cutout')
        rm.item_model(f'tfcmineralogy:ore/{stone}_{mineral}', no_textures=True, parent=f'tfcmineralogy:block/ore/{stone}_{mineral}')
        rm.flush()
        
        stone_capital = stone[0].upper() + stone[1:]
        mineral_capital = mineral[0].upper() + mineral[1:]
        lang_capital = stone_capital + " " + mineral_capital

        lang_entry = (f'block.tfcmineralogy.ore.{stone}_{mineral}', lang_capital)
        lang_dict.add(lang_entry)

        prospect_lang_entry = (f'block.tfcmineralogy.ore.{stone}_{mineral}.prospected', mineral_capital)
        prospect_lang_dict.add(prospect_lang_entry)
        #rm.lang(f'tfcmineralogy:ore/{stone}_{mineral}', lang_entry)
        #lang[0] = f'tfcmineralogy:ore/{stone}_{mineral}'
        #lang[1] = stone[0].upper + stone[1:] + " " + mineral[0].upper + mineral[1:] 
        
        #lang_names.add(lang)
rm.lang('itemGroup.tfcmineralogy_tab', 'TFC Mineralogy')
rm.lang(*lang_dict)
rm.lang(*prospect_lang_dict)
rm.flush()

#rm.block(f'tfcmineralogy:ore/{stone}_{mineral}').with_lang(f'{stone_first_letter}', 'en_us')
#rm.flush()
"""
### With Ore Quality

for quality in ore_quality:
    for mineral in mineral_dict:
        for stone in stone_dict:
            mineral_quality = quality+'_'+mineral
            rm.block_loot(f'ore/{mineral_quality}/{stone}',{'name': f'tfcmineralogy:ore/{stone}_{mineral_quality}'})
            rm.flush()

            rm_mc.tag('needs_iron_tool','blocks',f'tfcmineralogy:ore/{stone}_{mineral_quality}')
            rm_mc.tag('pickaxe','blocks/mineable',f'tfcmineralogy:ore/{stone}_{mineral_quality}')
            rm_mc.flush()

            rm.blockstate(f'tfcmineralogy:ore/{stone}_{mineral_quality}')
            rm.block_model(f'tfcmineralogy:ore/{stone}_{mineral_quality}',{'all':f'tfc:block/rock/raw/{stone}','particle':f'tfc:block/rock/raw/{stone}','overlay':f'tfcmineralogy:block/ore/{mineral_quality}'}, parent='tfc:block/ore', render='minecraft:cutout')
            rm.item_model(f'tfcmineralogy:ore/{stone}_{mineral_quality}', no_textures=True, parent=f'tfcmineralogy:block/ore/{stone}_{mineral_quality}')
            rm.flush()
            
            stone_capital = stone[0].upper() + stone[1:]
            mineral_capital = mineral[0].upper() + mineral[1:]
            quality_capital = quality[0].upper() + quality[1:]
            lang_capital = stone_capital + " " + quality_capital + " " + mineral_capital

            lang_entry = (f'block.tfcmineralogy.ore.{stone}_{mineral_quality}', lang_capital)
            lang_dict.add(lang_entry)

            prospect_lang_entry = (f'block.tfcmineralogy.ore.{stone}_{mineral_quality}.prospected', mineral_capital)
            prospect_lang_dict.add(prospect_lang_entry)

rm.lang('itemGroup.tfcmineralogy_tab', 'TFC Mineralogy')
rm.lang(*lang_dict)
rm.lang(*prospect_lang_dict)
rm.flush()
