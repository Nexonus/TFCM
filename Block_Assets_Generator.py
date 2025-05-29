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

rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_mc = ResourceManager(domain='minecraft', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

### ORES WITH NO TIERS
mineral_dict = {'vivianite', 'realgar','orpiment'} 
stone_dict = {'diorite','gabbro', 'granite', 'shale','claystone','limestone','conglomerate','dolomite','chert','chalk','rhyolite','basalt','andesite','dacite','quartzite','slate','phyllite','schist','gneiss','marble'} 
ore_quality = {'poor','normal','rich'}
lang_dict = set()
prospect_lang_dict = set()
item_lang_dict = set()
# For ores with no Qualities

tool_tier = 'copper'

for mineral in mineral_dict:
    for stone in stone_dict:
        rm.block_loot(f'ore/{mineral}/{stone}',{'name': f'tfcmineralogy:ore/{mineral}'})
        rm_tfc.tag(f'needs_{tool_tier}_tool','blocks',f'tfcmineralogy:ore/{mineral}/{stone}')
        rm_mc.tag('pickaxe','blocks/mineable',f'tfcmineralogy:ore/{mineral}/{stone}')
        rm.blockstate(f'tfcmineralogy:ore/{mineral}/{stone}')
        rm.block_model(f'tfcmineralogy:ore/{mineral}/{stone}',{'all':f'tfc:block/rock/raw/{stone}','particle':f'tfc:block/rock/raw/{stone}','overlay':f'tfcmineralogy:block/ore/{mineral}'}, parent='tfc:block/ore', render='minecraft:cutout')
        rm.item_model(f'tfcmineralogy:ore/{mineral}/{stone}', no_textures=True, parent=f'tfcmineralogy:block/ore/{mineral}/{stone}')
        # Add item for loot here:
        rm.item_model(f'tfcmineralogy:ore/{mineral}',no_textures=False,parent=f'minecraft:item/generated')
        rm.item_model(f'tfcmineralogy:powder/{mineral}',no_textures=False,parent=f'minecraft:item/generated')

        stone_capital = stone[0].upper() + stone[1:]
        mineral_capital = mineral[0].upper() + mineral[1:]
        lang_capital = stone_capital + " " + mineral_capital

        lang_entry = (f'block.tfcmineralogy.ore.{mineral}.{stone}', lang_capital)
        lang_dict.add(lang_entry)

        prospect_lang_entry = (f'block.tfcmineralogy.ore.{mineral}.{stone}.prospected', mineral_capital)
        prospect_lang_dict.add(prospect_lang_entry)
        lang_entry = (f'item.tfcmineralogy.ore.{mineral}', mineral_capital)
        item_lang_dict.add(lang_entry)
        lang_capital = mineral_capital + " Powder"
        lang_entry = (f'item.tfcmineralogy.powder.{mineral}', lang_capital)
        item_lang_dict.add(lang_entry)

rm.lang('itemGroup.tfcmineralogy_tab', 'TFC Mineralogy')
rm.lang(*lang_dict)
rm.lang(*prospect_lang_dict)
rm.lang(*item_lang_dict)

### ORE WITH PREDEFINED TIERS - POOR, NORMAL, RICH
mineral_dict = {'smithsonite'} 
tool_tier = 'copper' #valid: stone, copper, bronze, wrought_iron, black_steel, coloured_steel

for quality in ore_quality:
    for mineral in mineral_dict:
        for stone in stone_dict:
            mineral_quality = quality+'_'+mineral
            rm.block_loot(f'ore/{mineral_quality}/{stone}',{'name': f'tfcmineralogy:ore/{mineral_quality}'})

            rm_tfc.tag(f'needs_{tool_tier}_tool','blocks',f'tfcmineralogy:ore/{mineral_quality}/{stone}')
            rm_mc.tag('pickaxe','blocks/mineable',f'tfcmineralogy:ore/{mineral_quality}/{stone}')

            rm.blockstate(f'tfcmineralogy:ore/{mineral_quality}/{stone}')
            rm.block_model(f'tfcmineralogy:ore/{mineral_quality}/{stone}',{'all':f'tfc:block/rock/raw/{stone}','particle':f'tfc:block/rock/raw/{stone}','overlay':f'tfcmineralogy:block/ore/{mineral_quality}'}, parent='tfc:block/ore', render='minecraft:cutout')
            rm.item_model(f'tfcmineralogy:ore/{mineral_quality}/{stone}', no_textures=True, parent=f'tfcmineralogy:block/ore/{mineral_quality}/{stone}')
            # Add item for loot here:
            rm.item_model(f'tfcmineralogy:ore/{mineral_quality}',no_textures=False,parent=f'minecraft:item/generated')
            rm.item_model(f'tfcmineralogy:powder/{mineral}',no_textures=False,parent=f'minecraft:item/generated')
            
            stone_capital = stone[0].upper() + stone[1:]
            mineral_capital = mineral[0].upper() + mineral[1:]
            quality_capital = quality[0].upper() + quality[1:]
            lang_capital = quality_capital + " " + stone_capital + " " + mineral_capital

            lang_entry = (f'block.tfcmineralogy.ore.{mineral_quality}.{stone}', lang_capital)
            lang_dict.add(lang_entry)

            prospect_lang_entry = (f'block.tfcmineralogy.ore.{mineral_quality}.{stone}.prospected', mineral_capital)
            prospect_lang_dict.add(prospect_lang_entry)
            lang_capital = quality_capital + " " + mineral_capital
            lang_entry = (f'item.tfcmineralogy.ore.{mineral_quality}', lang_capital)
            item_lang_dict.add(lang_entry)
            lang_capital = mineral_capital + " Powder"
            lang_entry = (f'item.tfcmineralogy.powder.{mineral}', lang_capital)
            item_lang_dict.add(lang_entry)

rm.lang('itemGroup.tfcmineralogy_tab', 'TFC Mineralogy')
rm.lang(*lang_dict)
rm.lang(*prospect_lang_dict)
rm.lang(*item_lang_dict)
rm.flush()
rm_mc.flush()
rm_tfc.flush()
