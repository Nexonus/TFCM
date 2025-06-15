from mcresources.resource_manager import ResourceManager
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils, advancements
from mcresources.advancements import AdvancementCategory
from typing import Sequence, Dict, Union, Optional, Callable, Any
from mcresources.block_context import BlockContext
import os

def icon(name: str) -> Json:
    return {'item': name}

def inventory_changed(item: str | Json, name: str = 'item_obtained') -> Json:
    if isinstance(item, str) and name == 'item_obtained':
        name = item.split(':')[1]
    return {name: advancements.inventory_changed(item)}

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
ResourceManager.block_model = _block_model # Modifying the function to apply renderType feature.

def _loot(self, name_parts: ResourceIdentifier, *loot_pools: Json, path: str, loot_type: str) -> ResourceLocation:
        # Original code by AlactrazEscapee
        res = utils.resource_location(self.domain, name_parts)
        self.write(('data', res.domain, 'loot_tables', path, res.path), { # *loot_tables* is plural
            'type': loot_type,
            'pools': [
                utils.loot_pool(pool, path)
                for pool in loot_pools
            ]
        })
        return res
ResourceManager.loot = _loot # Fixing typo

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_mc = ResourceManager(domain='minecraft', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

story = AdvancementCategory(rm, 'story', 'tfc:textures/block/rock/mossy_cobble/schist.png')

# This time trying to make it actually functional :)
metal_tools = {
     'tuyere':{'name':'tuyere', 'units':400},
     'fish_hook':{'name':'fish_hook','units':200},
     'fishing_rod':{'name':'fishing_rod','units':200},
     'pickaxe':{'name':'pickaxe','units':100},
     'pickaxe_head':{'name':'pickaxe_head','units':100},
     'shovel':{'name':'shovel','units':100},
     'shovel_head':{'name':'shovel_head','units':100},
     'axe':{'name':'axe','units':100},
     'axe_head':{'name':'axe_head','units':100},
     'hoe':{'name':'hoe','units':100},
     'hoe_head':{'name':'hoe_head','units':100},
     'chisel':{'name':'chisel','units':100},
     'chisel_head':{'name':'chisel_head','units':100},
     'sword':{'name':'sword','units':200},
     'sword_blade':{'name':'sword_blade','units':200},
     'mace':{'name':'mace','units':200},
     'mace_head':{'name':'mace_head','units':200},
     'saw':{'name':'saw','units':100},
     'saw_blade':{'name':'saw_blade','units':100},
     'javelin':{'name':'javelin','units':100},
     'javelin_head':{'name':'javelin_head','units':100},
     'hammer':{'name':'hammer','units':100},
     'hammer_head':{'name':'hammer_head','units':100},
     'propick':{'name':'propick','units':100},
     'propick_head':{'name':'propick_head','units':100},
     'knife':{'name':'knife','units':100},
     'knife_blade':{'name':'knife_blade','units':100},
     'scythe':{'name':'scythe','units':100},
     'scythe_blade':{'name':'scythe_blade','units':100},
     'shears':{'name':'shears','units':200}
     }
metal_armor = {
     'unfinished_helmet':{'name':'unfinished_helmet','units':400},
     'helmet':{'name':'helmet','units':600},
     'unfinished_chestplate':{'name':'unfinished_chestplate','units':400},
     'chestplate':{'name':'chestplate','units':800},
     'unfinished_greaves':{'name':'unfinished_greaves','units':400},
     'greaves':{'name':'greaves','units':600},
     'unfinished_boots':{'name':'unfinished_boots','units':200},
     'boots':{'name':'boots','units':400}
     }

metal_dict = {
    'lead' :{
        'name': 'lead',
        'tier': 1,
        'melt_temperature' : 330,
        'specific_heat_capacity': 0.00857, # Default: 0.00857 - Cu, 0.02143 - Bi, requires more heat
        'base_heat_capacity': 2.535,
        'forging_temperature': 169,
        'welding_temperature': 215, 
        'parts' : True,
        'utility': False, #Lamps, Trapdoors, Etc
        'tools': False #Pickaxes, Axes, Etc
    },
    'arsenic' :{
        'name': 'arsenic',
        'tier': 1,
        'melt_temperature' : 816,
        'specific_heat_capacity': 0.02857, # Default: 0.00857 - Cu, 0.02143 - Bi, requires more heat
        'base_heat_capacity': 7.358,
        'forging_temperature': 493,
        'welding_temperature': 685, 
        'parts' : True,
        'utility': False, #Lamps, Trapdoors, Etc
        'tools': False #Pickaxes, Axes, Etc
    },
    'arsenical_bronze':{
         'name': 'arsenical_bronze',
         'tier': 2,
         'melt_temperature': 980,
         'specific_heat_capacity': 0.00857,
         'base_heat_capacity': 2.857,
         'forging_temperature': 680,
         'welding_temperature': 896, 
         'parts': True,
         'utility': True,
         'tools': True
    },
    'vanadium':{
         'name': 'vanadium',
         'tier': 4,
         'melt_temperature': 1900,
         'specific_heat_capacity': 0.01257,
         'base_heat_capacity': 4.123,
         'forging_temperature': 1576,
         'welding_temperature': 1785, 
         'parts': True,
         'utility': False,
         'tools': False
    },
    'cobalt':{
         'name': 'cobalt',
         'tier': 4,
         'melt_temperature': 1495,
         'specific_heat_capacity': 0.00925,
         'base_heat_capacity': 2.923,
         'forging_temperature': 983,
         'welding_temperature': 1205, 
         'parts': True,
         'utility': False,
         'tools': False
    }
}
simple_fluid_dict = {
    'ammonized_water':{
        'name': 'ammonized_water'
    }
}
for fluid, properties in simple_fluid_dict.items():
    fluidName = (properties['name'])
    #rm.tag(f'all_fluids',f'blocks',f'tfcmineralogy:fluid/{fluidName}') # I think this isn't necessary
    rm.tag(f'ingredients',f'fluids',f'tfcmineralogy:fluid/{fluidName}')
    rm.tag(f'{fluidName}',f'fluids',f'tfcmineralogy:{fluidName}')
    rm.tag(f'{fluidName}',f'fluids',f'tfcmineralogy:{fluidName}')
    #rm.blockstate(f'tfcmineralogy:cauldron/{fluidName}') # Not sure about this one in the end, shouldn't it be in TFC's domain?
    rm.blockstate(f'tfcmineralogy:fluid/{fluidName}')
    rm.block_model(f'tfcmineralogy:fluid/{fluidName}', {'particle':'minecraft:block/water_stil'}, parent=None)
    rm.custom_item_model(f'tfcmineralogy:bucket/{fluidName}', 'forge:fluid_container', {'parent':'forge:item/bucket', 'fluid':f'tfcmineralogy/{fluidName}'})
    rm_tfc.tag('all_fluids', 'blocks', f'tfcmineralogy:fluid/{fluidName}')
    rm_tfc.tag('ingredients', 'fluids', f'tfcmineralogy:fluid/{fluidName}')

# Metals with no tool usage:
for metal, properties in metal_dict.items():
    metalName = (properties['name'])
    metalUtility = (properties['utility'])
    metalTools = (properties['tools'])
    metalPart = (properties['parts'])
    metalTier = (properties['tier'])
    metalMeltingTemperature = (properties['melt_temperature'])
    metalSpecificHeatCapacity = (properties['specific_heat_capacity'])

    metalBaseHeatCapacity = (properties['base_heat_capacity']) # Base heat for 100 mB of metal
    metalForgingTemperature = (properties['forging_temperature'])
    metalWeldingTemperature = (properties['welding_temperature'])

#-------------------
# Metal Names
    if '_' in metalName:
        splitName = metalName.split('_')
        joinList = list()
        for element in splitName:
            joinList.append(element[0].upper() + element[1:])
        langMetalName = ' '.join(joinList)
    else:
        langMetalName=metal[0].upper()+metal[1:]

    # Add basic Metal Tags - if PART
#---------------------
# Add Molten Fluids here
    rm_tfc.tag('all_fluids', 'blocks', f'tfcmineralogy:metal/{metalName}') # Add to all fluids here
    rm_tfc.tag('molten_metals', 'fluids', f'tfcmineralogy:metal/{metalName}') # Add to the molten_metals
    rm.tag(f'{metalName}',f'fluids',f'tfcmineralogy:metal/{metalName}')
    rm.tag(f'{metalName}',f'fluids',f'tfcmineralogy:metal/flowing_{metalName}')
    rm.blockstate(f'tfcmineralogy:fluid/metal/{metalName}')

# For Special Metals that don't have their parts, tools and utility.
    if not metalPart and not metalTools and not metalUtility and not metalTools:
         rm.data(f'{metalName}',{'tier': metalTier, 'fluid':f'tfcmineralogy:metal/{metalName}','melt_temperature':metalMeltingTemperature,'specific_heat_capacity':metalSpecificHeatCapacity, 
            'ingots':{'tag':f'forge:ingots/{metalName}'}})
         rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/ingot/{metalName}')
         rm_forge.tag(f'{metalName}',f'items/ingots',f'tfcmineralogy:metal/ingot/{metalName}')
         rm_forge.tag(f'ingots',f'items',f'#forge:ingots/{metalName}')
         rm_tfc.tag('pileable_ingots','items',f'#forge:ingots/{metalName}')
         rm.recipe(f'heating/metal/{metalName}_ingot','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/ingot/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
         rm.item_model(f'tfcmineralogy:metal/double_ingot/{metalName}',f'tfcmineralogy:item/metal/double_ingot/{metalName}',parent='item/generated')
         rm.item(f'metal.ingot.{metalName}').with_lang((langMetalName) + ' Ingot')
#---------------------
    if metalPart:
        rm.data(f'{metalName}',{'tier': metalTier, 'fluid':f'tfcmineralogy:metal/{metalName}','melt_temperature':metalMeltingTemperature,'specific_heat_capacity':metalSpecificHeatCapacity, 
            'ingots':{'tag':f'forge:ingots/{metalName}'},
            'double_ingots':{'tag':f'forge:double_ingots/{metalName}'},
            'sheets':{'tag':f'forge:sheets/{metalName}'}},'data', 'tfc/metals/')
        
        rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/ingot/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item',f'items/metal/double_ingot/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item',f'items/metal/sheet/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item',f'items/metal/double_sheet/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/rod/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/block/{metalName}')
        rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/block/{metalName}_slab')
        rm_tfc.tag(f'{metalName}', 'metal_item', f'items/metal/block/{metalName}_stairs')

        rm_forge.tag(f'{metalName}',f'items/double_ingots',f'tfcmineralogy:metal/double_ingot/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/rods',f'tfcmineralogy:metal/rod/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/ingots',f'tfcmineralogy:metal/ingot/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/sheets',f'tfcmineralogy:metal/sheet/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/double_sheets',f'tfcmineralogy:metal/double_sheet/{metalName}')
        rm_forge.tag(f'double_ingots',f'items',f'#forge:double_ingots/{metalName}')
        rm_forge.tag(f'double_sheets',f'items',f'#forge:double_sheets/{metalName}')
        rm_forge.tag(f'ingots',f'items',f'#forge:ingots/{metalName}')
        rm_forge.tag(f'sheets',f'items',f'#forge:sheets/{metalName}')
        #rm.tag(f'all_fluids',f'blocks',f'tfcmineralogy:fluid/metal/{metalName}')
        rm.tag(f'metal_plated_blocks',f'blocks',f'tfcmineralogy:metal/block/{metalName}')
        rm_tfc.tag('pileable_double_ingots','items',f'#forge:double_ingots/{metalName}')
        rm_tfc.tag('pileable_ingots','items',f'#forge:ingots/{metalName}')
        rm_tfc.tag('pileable_sheets','items',f'#forge:sheets/{metalName}')
        
        # Melting Recipes 

        rm.recipe(f'heating/metal/{metalName}_block','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_slab','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}_slab'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':50},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_stairs','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}_stairs'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':75},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_block','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_ingot','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/ingot/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_double_ingot','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/double_ingot/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':200},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_sheet','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/sheet/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':200},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_double_sheet','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/double_sheet/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':400},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_rod','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/rod/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':50},'temperature':(metalMeltingTemperature)})
        # Crafting Recipes

        rm.recipe(f'crafting/metal/block/{metalName}', 'tfc:damage_inputs_shaped_crafting',{'recipe':{'type':'minecraft:crafting_shaped',
             'pattern':[' SH','SWS',' S '], 'key':{'S':{'tag':f'forge:sheets/{metalName}'},'W':{'tag':'minecraft:planks'},
             'H':{'tag':'tfc:hammers'}},'result':{'item':f'tfcmineralogy:metal/block/{metalName}', 'count':8}
             }})
        rm.recipe(f'crafting/metal/block/{metalName}_slab', 'minecraft:crafting_shaped', {'pattern':['XXX'],
            'key':{'X':{'item':f'tfcmineralogy:metal/block/{metalName}'}},'result':{'item':f'tfcmineralogy:metal/block/{metalName}_slab',
            'count':6}})
        rm.recipe(f'crafting/metal/block/{metalName}_stairs', 'minecraft:crafting_shaped', {'pattern':['X  ', 'XX ', 'XXX'],
            'key':{'X':{'item':f'tfcmineralogy:metal/block/{metalName}'}},'result':{'item':f'tfcmineralogy:metal/block/{metalName}_stairs',
            'count':8}})
        
        # Block Heats Recipes:
        rm.data(f'{metalName}_block',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_block_slab',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}_slab'}, 
        'heat_capacity':round(metalBaseHeatCapacity*0.5,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_block_stairs',{'ingredient':{'item':f'tfcmineralogy:metal/block/{metalName}_stairs'}, 
        'heat_capacity':round(metalBaseHeatCapacity*0.75,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')

        # Item Parts Heats Recipes:
        rm.data(f'{metalName}_ingot',{'ingredient':{'tag':f'forge:ingots/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_double_ingot',{'ingredient':{'tag':f'forge:double_ingots/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*2.0,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_rod',{'ingredient':{'tag':f'forge:rods/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*0.5,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_sheet',{'ingredient':{'tag':f'forge:sheets/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*2.0,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_double_sheet',{'ingredient':{'tag':f'forge:double_sheets/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*4.0,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        
        
        #rm.blockstate(f'tfcmineralogy:cauldron/metal/{metalName}') # Shouldn't this be in TFC's Domain?
        rm.blockstate(f'tfcmineralogy:metal/block/{metalName}')
        rm.blockstate(f'tfcmineralogy:metal/block/{metalName}_slab', f'tfcmineralogy:metal/block/{metalName}_slab', 
                      {'type=bottom':{'model': f'tfcmineralogy:block/metal/block/{metalName}_slab'},
                      'type=top':{'model': f'tfcmineralogy:block/metal/block/{metalName}_slab_top'},
                      'type=double':{'model': f'tfcmineralogy:block/metal/block/{metalName}'}})
        rm.blockstate(f'tfcmineralogy:metal/block/{metalName}_stairs', f'tfcmineralogy:metal/block/{metalName}_stairs', 
                        #Stairs bottom - straight OK
                      {'facing=east,half=bottom,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs'},
                       'facing=west,half=bottom,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'y':180, 'uvlock':True},
                       'facing=south,half=bottom,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'y':90, 'uvlock':True},
                       'facing=north,half=bottom,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'y':270, 'uvlock':True},
                        # Stairs bottom - outer right OK
                       'facing=east,half=bottom,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer'},
                       'facing=west,half=bottom,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':180, 'uvlock':True},
                       'facing=south,half=bottom,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':90, 'uvlock':True},
                       'facing=north,half=bottom,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':270, 'uvlock':True},
                        # Stairs bottom - outer left FIXED
                       'facing=east,half=bottom,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':270, 'uvlock':True},
                       'facing=west,half=bottom,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':90, 'uvlock':True},
                       'facing=south,half=bottom,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer'},
                       'facing=north,half=bottom,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'y':180, 'uvlock':True},
                        # Stairs bottom - inner right OK
                       'facing=east,half=bottom,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner'},
                       'facing=west,half=bottom,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':180, 'uvlock':True},
                       'facing=south,half=bottom,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':90, 'uvlock':True},
                       'facing=north,half=bottom,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':270, 'uvlock':True},
                        # Stairs bottom - inner left FIXED
                       'facing=east,half=bottom,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':270, 'uvlock':True},
                       'facing=west,half=bottom,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':90, 'uvlock':True},
                       'facing=south,half=bottom,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner'},
                       'facing=north,half=bottom,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'y':180, 'uvlock':True},
                        # Stairs top - straight FIXED
                       'facing=east,half=top,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'x':180, 'uvlock':True},
                       'facing=west,half=top,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'x':180, 'y':180, 'uvlock':True},
                       'facing=south,half=top,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'x':180, 'y':90, 'uvlock':True},
                       'facing=north,half=top,shape=straight':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs', 'x':180, 'y':270, 'uvlock':True},
                        # Stairs top - outer right FIXED
                       'facing=east,half=top,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':90, 'uvlock':True},
                       'facing=west,half=top,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':270, 'uvlock':True},
                       'facing=south,half=top,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':180, 'uvlock':True},
                       'facing=north,half=top,shape=outer_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'uvlock':True},
                        # Stairs top outer left FIXED
                       'facing=east,half=top,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'uvlock': True},
                       'facing=west,half=top,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':180, 'uvlock':True},
                       'facing=south,half=top,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':90, 'uvlock':True},
                       'facing=north,half=top,shape=outer_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_outer', 'x':180, 'y':270, 'uvlock':True},
                        # Stairs top inner right FIXED
                       'facing=east,half=top,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':90, 'uvlock':True},
                       'facing=west,half=top,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':270, 'uvlock':True},
                       'facing=south,half=top,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':180, 'uvlock':True},
                       'facing=north,half=top,shape=inner_right':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'uvlock':True},

                       'facing=east,half=top,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'uvlock':True},
                       'facing=west,half=top,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':180, 'uvlock':True},
                       'facing=south,half=top,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':90, 'uvlock':True},
                       'facing=north,half=top,shape=inner_left':{'model': f'tfcmineralogy:block/metal/block/{metalName}_stairs_inner', 'x':180, 'y':270, 'uvlock':True},
                      })
        rm.item_model(f'tfcmineralogy:metal/double_ingot/{metalName}',f'tfcmineralogy:item/metal/double_ingot/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/double_sheet/{metalName}',f'tfcmineralogy:item/metal/double_sheet/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/ingot/{metalName}',f'tfcmineralogy:item/metal/ingot/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/rod/{metalName}',f'tfcmineralogy:item/metal/rod/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/sheet/{metalName}',f'tfcmineralogy:item/metal/sheet/{metalName}',parent='item/generated')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}_slab', {'bottom':f'tfcmineralogy:block/metal/block/{metalName}','top':f'tfcmineralogy:block/metal/block/{metalName}','side':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='block/slab')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}_slab_top', {'bottom':f'tfcmineralogy:block/metal/block/{metalName}','top':f'tfcmineralogy:block/metal/block/{metalName}','side':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='block/slab_top')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}_stairs', {'bottom':f'tfcmineralogy:block/metal/block/{metalName}','top':f'tfcmineralogy:block/metal/block/{metalName}','side':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='block/stairs')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}_stairs_inner', {'bottom':f'tfcmineralogy:block/metal/block/{metalName}','top':f'tfcmineralogy:block/metal/block/{metalName}','side':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='block/inner_stairs')
        rm.block_model(f'tfcmineralogy:metal/block/{metalName}_stairs_outer', {'bottom':f'tfcmineralogy:block/metal/block/{metalName}','top':f'tfcmineralogy:block/metal/block/{metalName}','side':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='block/outer_stairs')

        rm.item_model(f'tfcmineralogy:metal/block/{metalName}',parent=f'tfcmineralogy:block/metal/block/{metalName}', no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/block/{metalName}_slab',parent=f'tfcmineralogy:block/metal/block/{metalName}_slab', no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/block/{metalName}_stairs',parent=f'tfcmineralogy:block/metal/block/{metalName}_stairs', no_textures=True)

        rm.block_model(f'tfcmineralogy:fluid/metal/{metalName}', {'particle':'block/lava_still'}, parent=None)
        rm.custom_item_model(f'tfcmineralogy:bucket/metal/{metalName}', 'forge:fluid_container', {'parent':'forge:item/bucket', 'fluid':f'tfcmineralogy/metal/{metalName}'})

        # Lang
        rm.lang(f'metal.tfcmineralogy.{metalName}', (langMetalName))
        rm.lang(f'fluid.tfcmineralogy.metal.{metalName}', (langMetalName))
        rm.lang(f'fluid.tfcm.metal.{metalName}', (langMetalName)) # I think it's this one?
        rm.item(f'metal.ingot.{metalName}').with_lang((langMetalName) + ' Ingot')
        rm.item(f'metal.rod.{metalName}').with_lang((langMetalName) +' Rod')
        rm.item(f'metal.sheet.{metalName}').with_lang((langMetalName) +' Sheet')
        rm.item(f'metal.double_ingot.{metalName}').with_lang((langMetalName) +' Double Ingot')
        rm.item(f'metal.double_sheet.{metalName}').with_lang((langMetalName) +' Double Sheet')
        rm.item(f'bucket.metal.{metalName}').with_lang('Molten ' + (langMetalName) + ' Bucket')

        rm.block(f'metal.block.{metalName}').with_lang((langMetalName) +' Plated Block')
        rm.block(f'metal.block.{metalName}_slab').with_lang((langMetalName) +' Plated Slab')
        rm.block(f'metal.block.{metalName}_stairs').with_lang((langMetalName) +' Plated Stairs')
        rm.block(f'fluid.metal.{metalName}').with_lang('Molten ' + (langMetalName))
        rm.block(f'cauldron.metal.{metalName}').with_lang('Molten ' + (langMetalName) + ' Cauldron')

        # Loot
        rm.block_loot(f'metal/block/{metalName}',{'name': f'tfcmineralogy:metal/block/{metalName}'})
        rm.block_loot(f'metal/block/{metalName}_slab',{'name': f'tfcmineralogy:metal/block/{metalName}_slab'})
        rm.block_loot(f'metal/block/{metalName}_stairs',{'name': f'tfcmineralogy:metal/block/{metalName}_stairs'})

        # Parts Anvil Recipes
        # Rod
        rm.recipe(f'anvil/{metalName}_rod','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/rod/{metalName}', 'count':2},'tier':metalTier,'rules':
        [
             'bend_last','draw_second_last','draw_third_last'
        ]})     
        # Sheet
        rm.recipe(f'anvil/{metalName}_sheet','tfc:anvil',{'input':{'tag':f'forge:double_ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/sheet/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','hit_second_last','hit_third_last'
        ]})
        # Welding Recipes:
        # Double Ingot
        rm.recipe(f'welding/{metalName}_double_ingot','tfc:welding',
        {'first_input':{'tag':f'forge:ingots/{metalName}'},
        'second_input':{'tag':f'forge:ingots/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/double_ingot/{metalName}'}})
        # Double Sheet
        rm.recipe(f'welding/{metalName}_double_sheet','tfc:welding',
        {'first_input':{'tag':f'forge:sheets/{metalName}'},
        'second_input':{'tag':f'forge:sheets/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/double_sheet/{metalName}'}})

        # Casting recipe:
        rm.recipe(f'casting/{metalName}_ingot','tfc:casting',{
            'mold':{'item':'tfc:ceramic/ingot_mold'},
            'fluid':{'ingredient':f'tfcmineralogy:metal/{metalName}','amount':100},
            'result':{'item':f'tfcmineralogy:metal/ingot/{metalName}'},
            'break_chance':0.1
        })
        
#---------------------
    if metalUtility:
        # Add Anvil, Lamp, Trapdoor if UTILITY
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/trapdoor/{metalName}')
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/lamp/{metalName}')
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/anvil/{metalName}')
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/bars/{metalName}')
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/unfinished_lamp/{metalName}')
        rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/chain/{metalName}')

        rm.tag(f'trapdoors',f'items',f'tfcmineralogy:metal/trapdoor/{metalName}')
        rm_tfc.tag(f'lamps',f'blocks',f'tfcmineralogy:metal/lamp/{metalName}')
        rm_tfc.tag(f'lamps',f'items',f'tfcmineralogy:metal/lamp/{metalName}') # Fixing these tags
        rm.tag(f'anvils',f'blocks',f'tfcmineralogy:metal/anvil/{metalName}')
        rm.blockstate(f'tfcmineralogy:metal/anvil/{metalName}', f'tfcmineralogy:block/metal/anvil/{metalName}', 
                      {'facing=north':{'model': f'tfcmineralogy:block/metal/anvil/{metalName}','y':90},
                       'facing=east':{'model': f'tfcmineralogy:block/metal/anvil/{metalName}','y':180}, 
                       'facing=south':{'model': f'tfcmineralogy:block/metal/anvil/{metalName}','y':270}, 
                       'facing=west':{'model': f'tfcmineralogy:block/metal/anvil/{metalName}'}}, False)
        rm.blockstate_multipart(f'tfcmineralogy:metal/bars/{metalName}', {'model':f'tfcmineralogy:block/bars/{metalName}_bars_post_ends'}, 
                ({'north':False, 'south': False, 'east': False, 'west': False}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_post'}),
                ({'north':True, 'south': False, 'east': False, 'west': False}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_cap'}),
                ({'north':False, 'south': False, 'east': True, 'west': False}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_cap', 'y':90}),
                ({'north':False, 'south': True, 'east': False, 'west': False}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_cap_alt'}),
                ({'north':False, 'south': False, 'east': False, 'west': True}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_cap_alt', 'y':90}),
                ({'north':True}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_side'}),
                ({'east':True}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_side', 'y':90}),
                ({'south':True}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_side_alt'}),
                ({'west':True}, {'model':f'tfcmineralogy:block/bars/{metalName}_bars_side_alt', 'y':90}))
        rm.blockstate(f'tfcmineralogy:metal/chain/{metalName}', f'tfcmineralogy:metal/chain/{metalName}', 
                      {'axis=x':{'model': f'tfcmineralogy:block/metal/chain/{metalName}', 'x':90, 'y':90},
                      'axis=y':{'model': f'tfcmineralogy:block/metal/chain/{metalName}'},
                      'axis=z':{'model': f'tfcmineralogy:block/metal/chain/{metalName}', 'x':90}})
        rm.blockstate(f'tfcmineralogy:metal/lamp/{metalName}', f'tfcmineralogy:metal/lamp/{metalName}', 
                      {'hanging=false,lit=false':{'model': f'tfcmineralogy:block/metal/lamp/{metalName}_off'},
                      'hanging=true,lit=false':{'model': f'tfcmineralogy:block/metal/lamp/{metalName}_hanging_off'},
                      'hanging=false,lit=true':{'model': f'tfcmineralogy:block/metal/lamp/{metalName}_on'},
                      'hanging=true,lit=true':{'model': f'tfcmineralogy:block/metal/lamp/{metalName}_hanging_on'}})
        rm.blockstate(f'tfcmineralogy:metal/trapdoor/{metalName}', f'tfcmineralogy:metal/trapdoor/{metalName}', 
                      {'facing=north,half=bottom,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_bottom'},
                       'facing=south,half=bottom,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_bottom', 'y':180},
                       'facing=east,half=bottom,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_bottom', 'y':90},
                       'facing=west,half=bottom,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_bottom', 'y':270},

                       'facing=north,half=top,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_top'},
                       'facing=south,half=top,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_top', 'y':180},
                       'facing=east,half=top,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_top', 'y':90},
                       'facing=west,half=top,open=false':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_top', 'y':270},

                       'facing=north,half=bottom,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open'},
                       'facing=south,half=bottom,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'y':180},
                       'facing=east,half=bottom,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'y':90},
                       'facing=west,half=bottom,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'y':270},

                       'facing=north,half=top,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'x':180, 'y':180},
                       'facing=south,half=top,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'x':180, 'y':0},
                       'facing=east,half=top,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'x':180, 'y':270},
                       'facing=west,half=top,open=true':{'model': f'tfcmineralogy:block/metal/trapdoor/{metalName}_open', 'x':180, 'y':90}})
        rm.item_model(f'tfcmineralogy:metal/anvil/{metalName}',parent=f'tfcmineralogy:block/metal/anvil/{metalName}',no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/bars/{metalName}',f'tfcmineralogy:block/metal/bars/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/chain/{metalName}',f'tfcmineralogy:item/metal/chain/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/lamp/{metalName}',f'tfcmineralogy:item/metal/lamp/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/trapdoor/{metalName}',parent=f'tfcmineralogy:block/metal/trapdoor/{metalName}_bottom', no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/unfinished_lamp/{metalName}',f'tfcmineralogy:item/metal/unfinished_lamp/{metalName}',parent='item/generated')

        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_cap', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_cap',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_cap_alt', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_cap_alt',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_post', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_post',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_post_ends', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_post_ends',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_post', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_post',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_side', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_side',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:bars/{metalName}_bars_side_alt', {'particle':f'tfcmineralogy:block/metal/bars/{metalName}','bars':f'tfcmineralogy:block/metal/bars/{metalName}','edge':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='minecraft:block/iron_bars_side_alt',render='minecraft:cutout')

        rm.block_model(f'tfcmineralogy:metal/anvil/{metalName}', {'top':f'tfcmineralogy:block/metal/anvil/{metalName}_top', 'side':f'tfcmineralogy:block/metal/anvil/{metalName}_side','particle':f'tfcmineralogy:block/metal/smooth/{metalName}'}, parent='tfc:block/anvil')

        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_hanging_off', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}_off'}, parent='minecraft:block/template_hanging_lantern', render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_hanging_on', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}'}, parent='minecraft:block/template_hanging_lantern', render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_off', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}_off'}, parent='minecraft:block/template_lantern',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_on', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}'}, parent='minecraft:block/template_lantern',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_bottom', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_bottom',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_top', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_top',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_open', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_open',render='minecraft:cutout')
        rm.block(f'{metalName}_trapdoor').with_lang((langMetalName) +' Trapdoor')
        rm.block_model(f'tfcmineralogy:metal/chain/{metalName}', {'all':f'tfcmineralogy:block/metal/chain/{metalName}','particle':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='minecraft:block/chain', render='minecraft:cutout')
        
        #Lang
        rm.item(f'metal.unfinished_lamp.{metalName}').with_lang((langMetalName) +' Unfinished Lamp')
        
        rm.block(f'metal.anvil.{metalName}').with_lang((langMetalName) +' Anvil')
        rm.block(f'metal.bars.{metalName}').with_lang((langMetalName) +' Bars')
        rm.block(f'metal.chain.{metalName}').with_lang((langMetalName) +' Chain')
        rm.block(f'metal.bars.{metalName}').with_lang((langMetalName) +' Bars')
        rm.block(f'metal.lamp.{metalName}').with_lang((langMetalName) +' Lamp')
        rm.block(f'metal.lamp.{metalName}.filled').with_lang('Filled '+(langMetalName) +' Lantern')
        rm.block(f'metal.trapdoor.{metalName}').with_lang((langMetalName) +' Trapdoor')

        #Loot
        rm.block_loot(f'metal/anvil/{metalName}',{'name': f'tfcmineralogy:metal/anvil/{metalName}'})
        rm.block_loot(f'metal/bars/{metalName}',{'name': f'tfcmineralogy:metal/bars/{metalName}'})
        rm.block_loot(f'metal/chain/{metalName}',{'name': f'tfcmineralogy:metal/chain/{metalName}'})
        rm.block_loot(f'metal/lamp/{metalName}',{'name': f'tfcmineralogy:metal/lamp/{metalName}'})
        rm.block_loot(f'metal/trapdoor/{metalName}',{'name': f'tfcmineralogy:metal/trapdoor/{metalName}'})

        # Melting Recipes
        rm.recipe(f'heating/metal/{metalName}_anvil','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/anvil/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':1400},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_trapdoor','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/trapdoor/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':200},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_bars','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/bars/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':25},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_lamp','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/lamp/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_unfinished_lamp','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/unfinished_lamp/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':100},'temperature':(metalMeltingTemperature)})
        rm.recipe(f'heating/metal/{metalName}_chain','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/chain/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':6},'temperature':(metalMeltingTemperature)})
        
        # Utility Block Heating Recipes
        rm.data(f'{metalName}_trapdoor',{'ingredient':{'tag':f'tfcmineralogy:metal/trapdoors/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*2.0,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_bars',{'ingredient':{'tag':f'tfcmineralogy:metal/bars/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity*0.25,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_anvil',{'ingredient':{'tag':f'tfcmineralogy:metal/anvils/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity/14.0,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')
        rm.data(f'{metalName}_chain',{'ingredient':{'tag':f'tfcmineralogy:metal/chains/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity/16.7,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')    # Chain is about 16.7 smaller than a full ingot (2.857 / 0.171 for Cu)
        rm.data(f'{metalName}_lamp',{'ingredient':{'tag':f'tfcmineralogy:metal/lamps/{metalName}'}, 
        'heat_capacity':round(metalBaseHeatCapacity,3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
        'data', 'tfc/item_heats/metal/')

        # Utility Anvil Recipes:
        # Bars
        rm.recipe(f'anvil/{metalName}_bars','tfc:anvil',{'input':{'tag':f'forge:sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/bars/{metalName}', 'count':8},'tier':metalTier,'rules':
        [
             'upset_last','punch_second_last','punch_third_last'
        ]})
        # Double Bars
        rm.recipe(f'anvil/{metalName}_double_bars','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/bars/{metalName}', 'count':16},'tier':metalTier,'rules':
        [
             'upset_last','punch_second_last','punch_third_last'
        ]})
        # Chain
        rm.recipe(f'anvil/{metalName}_chain','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/chain/{metalName}', 'count':16},'tier':metalTier,'rules':
        [
             'hit_any','hit_any','draw_last'
        ]})
        # Lamp
        rm.recipe(f'anvil/{metalName}_lamp','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/unfinished_lamp/{metalName}'},'tier':metalTier,'rules':
        [
             'bend_last','bend_second_last','draw_third_last'
        ]})
        # Trapdoor
        rm.recipe(f'anvil/{metalName}_trapdoor','tfc:anvil',{'input':{'tag':f'forge:sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/trapdoor/{metalName}'},'tier':metalTier,'rules':
        [
             'bend_last','draw_second_last','draw_third_last'
        ]})
        # Crafting Recipes:
        rm.recipe(f'crafting/metal/anvil/{metalName}', 'minecraft:crafting_shaped',{
             'pattern':['XXX',' X ','XXX'],'key':{'X':{'tag':f'forge:double_ingots/{metalName}'}},
             'result':{'item':f'tfcmineralogy:metal/anvil/{metalName}'}
        })
        rm.recipe(f'crafting/metal/lamp/{metalName}', 'minecraft:crafting_shapeless',{
            'ingredients':[
                {'item':'tfc:lamp_glass'},
                {'item':f'tfcmineralogy:metal/unfinished_lamp/{metalName}'}
            ],
            'result':{
                'item':f'tfcmineralogy:metal/lamp/{metalName}'
            }
        })

#---------------------
    if metalTools:
        # Add Metal Tools if TOOL
        rm.tag(f'pickaxes',f'items',f'tfcmineralogy:metal/pickaxe/{metalName}')
        rm.tag(f'axes',f'items',f'tfcmineralogy:metal/axe/{metalName}')
        rm.tag(f'shovels',f'items',f'tfcmineralogy:metal/shovel/{metalName}')
        rm.tag(f'swords',f'items',f'tfcmineralogy:metal/sword/{metalName}')
        rm.tag(f'hammers',f'items',f'tfcmineralogy:metal/hammer/{metalName}')
        rm.tag(f'knives',f'items',f'tfcmineralogy:metal/knife/{metalName}')
        rm.tag(f'hoes',f'items',f'tfcmineralogy:metal/hoe/{metalName}')
        rm.tag(f'chisels',f'items',f'tfcmineralogy:metal/chisel/{metalName}')
        rm.tag(f'propicks',f'items',f'tfcmineralogy:metal/propick/{metalName}')
        rm.tag(f'saws',f'items',f'tfcmineralogy:metal/saw/{metalName}')
        rm.tag(f'scythes',f'items',f'tfcmineralogy:metal/scythe/{metalName}')
        rm.tag(f'javelins',f'items',f'tfcmineralogy:metal/javelin/{metalName}')
        rm.tag(f'maces',f'items',f'tfcmineralogy:metal/mace/{metalName}')
        rm.tag(f'tuyeres',f'items',f'tfcmineralogy:metal/tuyere/{metalName}')
        rm.tag(f'shears',f'items',f'tfcmineralogy:metal/shears/{metalName}')
        # Add UsableOnToolRack tag if TOOL
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/axe/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/pickaxe/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/shovel/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/sword/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/hammer/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/knife/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/hoe/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/chisel/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/propick/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/saw/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/scythe/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/javelin/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/mace/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/tuyere/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/shears/{metalName}')
        rm.tag(f'usable_on_tool_rack',f'items',f'tfcmineralogy:metal/fishing_rod/{metalName}')
        # Add to metal Tool tag:
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/axe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/pickaxe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/shovel/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/sword/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/hammer/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/knife/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/hoe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/chisel/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/propick/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/saw/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/scythe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/javelin/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/mace/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/tuyere/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/shears/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal',f'tfcmineralogy:metal/fishing_rod/{metalName}')
        # Deals damage tags for TOOL
        rm.tag(f'deals_slashing_damage',f'items',f'#tfcmineralogy:scythes')
        rm.tag(f'deals_crushing_damage',f'items',f'#tfcmineralogy:hammers')
        rm.tag(f'deals_crushing_damage',f'items',f'#tfcmineralogy:maces')
        rm.tag(f'deals_piercing_damage',f'items',f'#tfcmineralogy:javelins')
        rm.tag(f'deals_piercing_damage',f'items',f'#tfcmineralogy:knives')
        # Add Metal Tools Models
        rm.item_model(f'tfcmineralogy:metal/axe/{metalName}',f'tfcmineralogy:item/metal/axe/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/chisel/{metalName}',f'tfcmineralogy:item/metal/chisel/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/hammer/{metalName}',f'tfcmineralogy:item/metal/hammer/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/hoe/{metalName}',f'tfcmineralogy:item/metal/hoe/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/axe_head/{metalName}',f'tfcmineralogy:item/metal/axe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/chisel_head/{metalName}',f'tfcmineralogy:item/metal/chisel_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/fish_hook/{metalName}',f'tfcmineralogy:item/metal/fish_hook/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/fishing_rod/{metalName}',f'tfcmineralogy:item/metal/fishing_rod/{metalName}',parent='minecraft:item/handheld_rod', overrides=[{'predicate':{'tfc:cast':1},'model':f'tfcmineralogy:item/metal/fishing_rod/{metalName}_cast'}])
        rm.item_model(f'tfcmineralogy:metal/fishing_rod/{metalName}_cast',f'minecraft:item/fishing_rod_cast',parent='item/fishing_rod')

        rm.item_model(f'tfcmineralogy:metal/hammer_head/{metalName}',f'tfcmineralogy:item/metal/hammer_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/hoe_head/{metalName}',f'tfcmineralogy:item/metal/hoe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/horse_armor/{metalName}',f'tfcmineralogy:item/metal/horse_armor/{metalName}',parent='item/generated')

        rm.custom_item_model(f'tfcmineralogy:metal/javelin/{metalName}','forge:separate_transforms',{'textures':{'particle':f'tfcmineralogy:item/metal/javelin/{metalName}'},
        'gui_light':'front','overrides':[{'predicate':{'tfc:throwing':1},'model':f'tfcmineralogy:item/metal/javelin/{metalName}_throwing'}],
        'base':{'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_in_hand'},'perspectives':
        {'none':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'fixed':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'ground':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'gui':
        {
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        }}})
        rm.item_model(f'tfcmineralogy:metal/javelin/{metalName}_gui',f'tfcmineralogy:item/metal/javelin/{metalName}',parent='item/generated')
        rm.data(f'tfcmineralogy:metal/javelin/{metalName}_in_hand',{'parent':'item/trident_in_hand','textures':{'particle':f'tfcmineralogy:item/metal/javelin/{metalName}'}},'assets','models/item/')
        #rm.item_model(f'tfcmineralogy:metal/javelin/{metalName}_in_hand',f'tfcmineralogy:item/metal/javelin/{metalName}',parent='item/trident_in_hand')
        rm.custom_item_model(f'tfcmineralogy:metal/javelin/{metalName}_throwing','forge:separate_transforms',{'gui_light':'front',
        'base':{'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_throwing_base'},'perspectives':
        {'none':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'fixed':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'ground':{
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        },
        'gui':
        {
            'parent':f'tfcmineralogy:item/metal/javelin/{metalName}_gui'
        }}})
        rm.item_model(f'tfcmineralogy:metal/javelin/{metalName}_throwing_base',f'tfcmineralogy:item/metal/javelin/{metalName}',parent='item/trident_throwing')

        #rm.item_model(f'tfcmineralogy:metal/javelin/{metalName}',f'tfcmineralogy:item/metal/javelin/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/javelin_head/{metalName}',f'tfcmineralogy:item/metal/javelin_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/knife/{metalName}',f'tfcmineralogy:item/metal/knife/{metalName}',parent='tfc:item/handheld_flipped')
        
        rm.item_model(f'tfcmineralogy:metal/knife_blade/{metalName}',f'tfcmineralogy:item/metal/knife_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/mace/{metalName}',f'tfcmineralogy:item/metal/mace/{metalName}',parent='item/handheld')

        rm.item_model(f'tfcmineralogy:metal/mace_head/{metalName}',f'tfcmineralogy:item/metal/mace_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/pickaxe/{metalName}',f'tfcmineralogy:item/metal/pickaxe/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/pickaxe_head/{metalName}',f'tfcmineralogy:item/metal/pickaxe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/propick/{metalName}',f'tfcmineralogy:item/metal/propick/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/propick_head/{metalName}',f'tfcmineralogy:item/metal/propick_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/saw/{metalName}',f'tfcmineralogy:item/metal/saw/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/saw_blade/{metalName}',f'tfcmineralogy:item/metal/saw_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/scythe/{metalName}',f'tfcmineralogy:item/metal/scythe/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/scythe_blade/{metalName}',f'tfcmineralogy:item/metal/scythe_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/shears/{metalName}',f'tfcmineralogy:item/metal/shears/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/shovel/{metalName}',f'tfcmineralogy:item/metal/shovel/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/shovel_head/{metalName}',f'tfcmineralogy:item/metal/shovel_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/sword_blade/{metalName}',f'tfcmineralogy:item/metal/sword_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/sword/{metalName}',f'tfcmineralogy:item/metal/sword/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/tuyere/{metalName}',f'tfcmineralogy:item/metal/tuyere/{metalName}',parent='item/generated')

        rm.item_model(f'tfcmineralogy:metal/unfinished_helmet/{metalName}',f'tfcmineralogy:item/metal/unfinished_helmet/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_chestplate/{metalName}',f'tfcmineralogy:item/metal/unfinished_chestplate/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_greaves/{metalName}',f'tfcmineralogy:item/metal/unfinished_greaves/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_boots/{metalName}',f'tfcmineralogy:item/metal/unfinished_boots/{metalName}',parent='item/generated')

        rm.custom_item_model(f'tfcmineralogy:metal/boots/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/boots/{metalName}','trim':'tfc:item/boots_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/chestplate/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/chestplate/{metalName}','trim':'tfc:item/chestplate_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/greaves/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/greaves/{metalName}','trim':'tfc:item/greaves_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/helmet/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/helmet/{metalName}','trim':'tfc:item/helmet_trim'}})
        
        #Lang
        # why did i do this- anyway.
        rm.item(f'metal.tuyere.{metalName}').with_lang((langMetalName) +' Tuyere')
        rm.item(f'metal.fish_hook.{metalName}').with_lang((langMetalName) +' Fish Hook')
        rm.item(f'metal.fishing_rod.{metalName}').with_lang((langMetalName) +' Fishing Rod')
        rm.item(f'metal.pickaxe.{metalName}').with_lang((langMetalName) +' Pickaxe')
        rm.item(f'metal.pickaxe_head.{metalName}').with_lang((langMetalName) +' Pickaxe Head')
        rm.item(f'metal.shovel.{metalName}').with_lang((langMetalName) +' Shovel')
        rm.item(f'metal.shovel_head.{metalName}').with_lang((langMetalName) +' Shovel Head')
        rm.item(f'metal.axe.{metalName}').with_lang((langMetalName) +' Axe')
        rm.item(f'metal.axe_head.{metalName}').with_lang((langMetalName) +' Axe Head')
        rm.item(f'metal.hoe.{metalName}').with_lang((langMetalName) +' Hoe')
        rm.item(f'metal.hoe_head.{metalName}').with_lang((langMetalName) +' Hoe Head')
        rm.item(f'metal.chisel.{metalName}').with_lang((langMetalName) +' Chisel')
        rm.item(f'metal.chisel_head.{metalName}').with_lang((langMetalName) +' Chisel Head')
        rm.item(f'metal.sword.{metalName}').with_lang((langMetalName) +' Sword')
        rm.item(f'metal.sword_blade.{metalName}').with_lang((langMetalName) +' Sword Blade')
        rm.item(f'metal.mace.{metalName}').with_lang((langMetalName) +' Mace')
        rm.item(f'metal.mace_head.{metalName}').with_lang((langMetalName) +' Mace Head')
        rm.item(f'metal.saw.{metalName}').with_lang((langMetalName) +' Saw')
        rm.item(f'metal.saw_blade.{metalName}').with_lang((langMetalName) +' Saw Blade')
        rm.item(f'metal.javelin.{metalName}').with_lang((langMetalName) +' Javelin')
        rm.item(f'metal.javelin_head.{metalName}').with_lang((langMetalName) +' Javelin Head')
        rm.item(f'metal.hammer_head.{metalName}').with_lang((langMetalName) +' Hammer Head')
        rm.item(f'metal.hammer.{metalName}').with_lang((langMetalName) +' Hammer')
        rm.item(f'metal.propick.{metalName}').with_lang((langMetalName) +" Prospector's Pick")
        rm.item(f'metal.propick_head.{metalName}').with_lang((langMetalName) +" Prospector's Pick Head")
        rm.item(f'metal.knife.{metalName}').with_lang((langMetalName) +" Knife")
        rm.item(f'metal.knife_blade.{metalName}').with_lang((langMetalName) +" Knife Blade")
        rm.item(f'metal.scythe.{metalName}').with_lang((langMetalName) +" Scythe")
        rm.item(f'metal.scythe_blade.{metalName}').with_lang((langMetalName) +" Scythe Blade")
        rm.item(f'metal.shears.{metalName}').with_lang((langMetalName) +" Shears")
        rm.item(f'metal.unfinished_helmet.{metalName}').with_lang((langMetalName) +" Unfinished Helmet")
        rm.item(f'metal.helmet.{metalName}').with_lang((langMetalName) +" Helmet")
        rm.item(f'metal.unfinished_chestplate.{metalName}').with_lang((langMetalName) +" Unfinished Chestplate")
        rm.item(f'metal.chestplate.{metalName}').with_lang((langMetalName) +" Chestplate")
        rm.item(f'metal.unfinished_greaves.{metalName}').with_lang((langMetalName) +" Unfinished Greaves")
        rm.item(f'metal.greaves.{metalName}').with_lang((langMetalName) +" Greaves")
        rm.item(f'metal.unfinished_boots.{metalName}').with_lang((langMetalName) +" Unfinished Boots")
        rm.item(f'metal.boots.{metalName}').with_lang((langMetalName) +" Boots")
        rm.item(f'metal.horse_armor.{metalName}').with_lang((langMetalName) +" Horse Armor")
        rm.item(f'metal.shield.{metalName}').with_lang((langMetalName) +" Shield")
        rm.tag('axes_that_log','items',f'#tfcmineralogy:axes')
        rm.tag('sharp_tools','items',f'#tfcmineralogy:knives')
        rm.tag('sharp_tools','items',f'#tfcmineralogy:scythes')

        # Heating Recipes and Tags
        for toolID, recipe_property in metal_tools.items():
            metalUnits = (recipe_property['units'])
            metalPart = (recipe_property['name'])
            
            rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/{metalPart}/{metalName}')
            rm.recipe(f'heating/metal/{metalName}_{metalPart}','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':metalUnits},'temperature':(metalMeltingTemperature)})
            # Heating Recipes:
            rm.data(f'{metalName}_{metalPart}',{'ingredient':{'tag':f'tfcmineralogy:metal/{metalPart}/{metalName}'}, 
            'heat_capacity':round(metalBaseHeatCapacity*(metalUnits/100),3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
            'data', 'tfc/item_heats/metal/')
            # Crafting Recipes for Tools:
            # Crafting Recipes:
            if ('head' in metalPart):
                toolPart = str(metalPart).replace('_head', '')
                rm.recipe(f'crafting/metal/{toolPart}/{metalName}', 'tfc:advanced_shaped_crafting',{
                'pattern':['X', 'Y'],'key':{'X':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'},
                'Y':{'tag':'forge:rods/wooden'}},
                'result':{'stack':{'item':f'tfcmineralogy:metal/{toolPart}/{metalName}'},'modifiers':['tfc:copy_forging_bonus']
                },'input_row':0,'input_column':0})
            # Casting Recipes
                rm.recipe(f'casting/{metalName}_{metalPart}','tfc:casting',{
                'mold':{'item':f'tfc:ceramic/{metalPart}_mold'},
                'fluid':{'ingredient':f'tfcmineralogy:metal/{metalName}','amount':metalUnits},
                'result':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'},
                'break_chance':1
                })
            if ('blade' in metalPart):
                toolPart = str(metalPart).replace('_blade', '')
                rm.recipe(f'crafting/metal/{toolPart}/{metalName}', 'tfc:advanced_shaped_crafting',{
                'pattern':['X', 'Y'],'key':{'X':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'},
                'Y':{'tag':'forge:rods/wooden'}},
                'result':{'stack':{'item':f'tfcmineralogy:metal/{toolPart}/{metalName}'},'modifiers':['tfc:copy_forging_bonus']
                },'input_row':0,'input_column':0})
                # Casting Recipes
                rm.recipe(f'casting/{metalName}_{metalPart}','tfc:casting',{
                'mold':{'item':f'tfc:ceramic/{metalPart}_mold'},
                'fluid':{'ingredient':f'tfcmineralogy:metal/{metalName}','amount':metalUnits},
                'result':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'},
                'break_chance':1
                })
             
        for armorpart, recipe_property in metal_armor.items():
             metalUnits = (recipe_property['units'])
             metalPart = (recipe_property['name'])
             rm_tfc.tag(f'{metalName}','metal_item', f'items/metal/{metalPart}/{metalName}') # The I'm Done Loop
             rm.recipe(f'heating/metal/{metalName}_{metalPart}','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/{metalPart}/{metalName}'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/{metalName}', 'amount':metalUnits},'temperature':(metalMeltingTemperature)})
             # Heating Recipes:
             rm.data(f'{metalName}_{metalPart}',{'ingredient':{'tag':f'tfcmineralogy:metal/{metalPart}/{metalName}'}, 
             'heat_capacity':round(metalBaseHeatCapacity*(metalUnits/100),3), 'forging_temperature':metalForgingTemperature, 'welding_temperature':metalWeldingTemperature},
             'data', 'tfc/item_heats/metal/')
        # Recipe Hell - Anvil Recipes for Tools:
        # Axe Head
        rm.recipe(f'anvil/{metalName}_axe_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/axe_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','hit_second_last','upset_third_last'
        ],'apply_forging_bonus':True})
        # Chisel
        rm.recipe(f'anvil/{metalName}_chisel_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/chisel_head/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','hit_not_last','draw_not_last'
        ],'apply_forging_bonus':True})
        # Fish Hook
        rm.recipe(f'anvil/{metalName}_fish_hook','tfc:anvil',{'input':{'tag':f'forge:sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/fish_hook/{metalName}'},'tier':metalTier,'rules':
        [
             'draw_not_last','bend_any','hit_any'
        ],'apply_forging_bonus':True})
        # Hammer
        rm.recipe(f'anvil/{metalName}_hammer_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/hammer_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','shrink_not_last'
        ],'apply_forging_bonus':True})
        # Hoe
        rm.recipe(f'anvil/{metalName}_hoe_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/hoe_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','hit_not_last','bend_not_last'
        ],'apply_forging_bonus':True})
        # Javelin
        rm.recipe(f'anvil/{metalName}_javelin_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/javelin_head/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','hit_second_last','draw_third_last'
        ],'apply_forging_bonus':True})
        # Knife
        rm.recipe(f'anvil/{metalName}_knife_blade','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/knife_blade/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','draw_second_last','draw_third_last'
        ],'apply_forging_bonus':True})
        # Mace
        rm.recipe(f'anvil/{metalName}_mace_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/mace_head/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','shrink_not_last','bend_not_last'
        ],'apply_forging_bonus':True})
        # Pickaxe
        rm.recipe(f'anvil/{metalName}_pickaxe_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/pickaxe_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','bend_not_last','draw_not_last'
        ],'apply_forging_bonus':True})
        # Propick 
        rm.recipe(f'anvil/{metalName}_propick_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/propick_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','draw_not_last','bend_not_last'
        ],'apply_forging_bonus':True})
        # Propick 
        rm.recipe(f'anvil/{metalName}_propick_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/propick_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','draw_not_last','bend_not_last'
        ],'apply_forging_bonus':True})
        # Saw
        rm.recipe(f'anvil/{metalName}_saw_blade','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/saw_blade/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','hit_second_last'
        ],'apply_forging_bonus':True})
        # Scythe
        rm.recipe(f'anvil/{metalName}_scythe_blade','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/scythe_blade/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','draw_second_last','bend_third_last'
        ],'apply_forging_bonus':True})
        # Shield
        rm.recipe(f'anvil/{metalName}_shield','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/shield/{metalName}'},'tier':metalTier,'rules':
        [
             'upset_last','bend_second_last','bend_third_last'
        ],'apply_forging_bonus':True})
        # Shovel
        rm.recipe(f'anvil/{metalName}_shovel_head','tfc:anvil',{'input':{'tag':f'forge:ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/shovel_head/{metalName}'},'tier':metalTier,'rules':
        [
             'punch_last','hit_not_last'
        ],'apply_forging_bonus':True})
        # Sword
        rm.recipe(f'anvil/{metalName}_sword_blade','tfc:anvil',{'input':{'tag':f'forge:double_ingots/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/sword_blade/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','bend_second_last','bend_third_last'
        ],'apply_forging_bonus':True})
        # Tuyere
        rm.recipe(f'anvil/{metalName}_tuyere','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/tuyere/{metalName}'},'tier':metalTier,'rules':
        [
             'bend_last','bend_second_last'
        ]})
        # Unfinished Boots
        rm.recipe(f'anvil/{metalName}_unfinished_boots','tfc:anvil',{'input':{'tag':f'forge:sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/unfinished_boots/{metalName}'},'tier':metalTier,'rules':
        [
             'bend_last','bend_second_last','shrink_third_last'
        ]})
        # Unfinished Chestplate
        rm.recipe(f'anvil/{metalName}_unfinished_chestplate','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/unfinished_chestplate/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','hit_second_last','upset_third_last'
        ]})
        # Unfinished Greaves
        rm.recipe(f'anvil/{metalName}_unfinished_greaves','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/unfinished_greaves/{metalName}'},'tier':metalTier,'rules':
        [
             'bend_any','draw_any','hit_any'
        ]})
        # Unfinished Helmet
        rm.recipe(f'anvil/{metalName}_unfinished_helmet','tfc:anvil',{'input':{'tag':f'forge:double_sheets/{metalName}'},
        'result':{'item':f'tfcmineralogy:metal/unfinished_helmet/{metalName}'},'tier':metalTier,'rules':
        [
             'hit_last','bend_second_last','bend_third_last'
        ]})
    # Welding recipes:
    # Boots
        rm.recipe(f'welding/{metalName}_boots','tfc:welding',
        {'first_input':{'item':f'tfcmineralogy:metal/unfinished_boots/{metalName}'},
        'second_input':{'item':f'tfcmineralogy:metal/sheet/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/boots/{metalName}'}})
    # Chestplate
        rm.recipe(f'welding/{metalName}_chestplate','tfc:welding',
        {'first_input':{'item':f'tfcmineralogy:metal/unfinished_chestplate/{metalName}'},
        'second_input':{'item':f'tfcmineralogy:metal/double_sheet/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/chestplate/{metalName}'}})
    # Greaves
        rm.recipe(f'welding/{metalName}_greaves','tfc:welding',
        {'first_input':{'item':f'tfcmineralogy:metal/unfinished_greaves/{metalName}'},
        'second_input':{'item':f'tfcmineralogy:metal/sheet/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/greaves/{metalName}'}})
    # Helmet
        rm.recipe(f'welding/{metalName}_helmet','tfc:welding',
        {'first_input':{'item':f'tfcmineralogy:metal/unfinished_helmet/{metalName}'},
        'second_input':{'item':f'tfcmineralogy:metal/sheet/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/helmet/{metalName}'}})
    # Shears
        rm.recipe(f'welding/{metalName}_shears','tfc:welding',
        {'first_input':{'item':f'tfcmineralogy:metal/knife_blade/{metalName}'},
        'second_input':{'item':f'tfcmineralogy:metal/knife_blade/{metalName}'},
        'tier':metalTier-1,
        'result':{'item':f'tfcmineralogy:metal/shears/{metalName}'},
        'combine_forging_bonus': True})
    # Crafting Recipes Special:
    rm.recipe(f'crafting/{metalName}_horse_armor', 'minecraft:crafting_shaped',{
             'pattern':['YXY','ZZZ'],'key':{'Z':{'tag':f'forge:double_sheets/{metalName}'},
             'Y':{'item':f'tfc:jute_fiber'},
             'X':{'item':f'minecraft:leather_horse_armor'}},
             'result':{'item':f'tfcmineralogy:metal/horse_armor/{metalName}'}
        })

rm.lang('tfcm.creative_tab.tfcm_metals', 'TFCM Metals')
rm.lang('tfcm.creative_tab.tfcm_ores', 'TFCM Ores')
rm.lang('tfcm.creative_tab.tfcm_misc', 'TFCM Miscellaneous')
rm.lang('tfcm.advancements.story.heavy_lead_block.title', 'Mostly Metal')
rm.lang('tfcm.advancements.story.heavy_lead_block.description', 'Make a Heavy Lead Block')

# Special stuff - Singular recipes, tags, etc:
rm.recipe(f'crafting/metal/heavy_lead_block', 'tfc:damage_inputs_shaped_crafting',{'recipe':{'type':'minecraft:crafting_shaped','pattern':[' SH','SBS',' S '], 'key':{
             'S':{'tag':f'forge:sheets/lead'},'B':{'item':'tfcmineralogy:metal/block/lead'},'H':{'tag':'tfc:hammers'}},
             'result':{'item':f'tfcmineralogy:metal/heavy_lead_block', 'count':1}
             }})
rm.block(f'metal.heavy_lead_block').with_lang('Heavy Lead Plated Block')
rm.recipe(f'heating/metal/heavy_lead_block','tfc:heating',{'ingredient':{'item':f'tfcmineralogy:metal/heavy_lead_block'}, 
                'result_fluid':{'fluid':f'tfcmineralogy:metal/lead', 'amount':900},'temperature':380})    

story.advancement('heavy_lead_block', icon('tfcmineralogy:metal/heavy_lead_block'), 'Mostly Metal', 'Make a Heavy Lead Block', 'tfc:story/plated_block', inventory_changed('tfcmineralogy:metal/heavy_lead_block'))    

# Alloying Recipes:
rm.recipe(f'alloy/arsenical_bronze', 'tfc:alloy', {'result':'tfcmineralogy:arsenical_bronze',
'contents':[
    {
        'metal':'tfc:copper',
        'min':0.78,
        'max':0.9
    },
    {
        'metal':'tfc:tin',
        'min':0.06,
        'max':0.16
    },
    {
        'metal':'tfcmineralogy:arsenic',
        'min':0.04,
        'max':0.06
    }
]})

rm_forge.flush()
rm_tfc.flush()
rm.flush()
