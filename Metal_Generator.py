from mcresources.resource_manager import ResourceManager
from mcresources.type_definitions import Json, JsonObject, ResourceLocation, ResourceIdentifier, TypeWithOptionalConfig
from mcresources import utils
from typing import Sequence, Dict, Union, Optional, Callable, Any
from mcresources.block_context import BlockContext
import os

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

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_mc = ResourceManager(domain='minecraft', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)
# This time trying to make it actually functional :)
metal_dict = {
    'lead' :{
        'name': 'lead',
        'tier': 1,
        'melt_temperature' : 380,
        'specific_heat_capacity': 0.01029,
        'parts' : True,
        'utility': True, #Lamps, Trapdoors, Etc
        'tools': False #Pickaxes, Axes, Etc
    }
}
simple_fluid_dict = {
    'ammonized_water':{
        'name': 'ammonized_water'
    }
}
for fluid, properties in simple_fluid_dict.items():
    fluidName = (properties['name'])
    rm.tag(f'all_fluids',f'blocks',f'tfcmineralogy:fluid/{fluidName}') # For now just this
    rm.tag(f'ingredients',f'fluids',f'tfcmineralogy:fluid/{fluidName}')
    rm.tag(f'{fluidName}',f'fluids',f'tfcmineralogy:{fluidName}')
    rm.tag(f'{fluidName}',f'fluids',f'tfcmineralogy:{fluidName}')
    #rm.blockstate(f'tfcmineralogy:cauldron/{fluidName}') # Not sure about this one in the end, shouldn't it be in TFC's domain?
    rm.blockstate(f'tfcmineralogy:fluid/{fluidName}')
    rm.block_model(f'tfcmineralogy:fluid/{fluidName}', {'particle':'minecraft:block/water_stil'}, parent=None)
    rm.custom_item_model(f'tfcmineralogy:bucket/{fluidName}', 'forge:fluid_container', {'parent':'forge:item/bucket', 'fluid':f'tfcmineralogy/{fluidName}'})

# Metals with no tool usage:
for metal, properties in metal_dict.items():
    metalName = (properties['name'])
    metalUtility = (properties['utility'])
    metalTools = (properties['tools'])
    metalPart = (properties['parts'])
    # Add basic Metal Tags - if PART
    if metalPart:
        rm_forge.tag(f'{metalName}',f'items/double_ingots',f'tfcmineralogy:metal/double_ingot/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/rods',f'tfcmineralogy:metal/rod/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/ingots',f'tfcmineralogy:metal/ingot/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/sheets',f'tfcmineralogy:metal/sheet/{metalName}')
        rm_forge.tag(f'{metalName}',f'items/double_sheets',f'tfcmineralogy:metal/double_sheet/{metalName}')
        rm_forge.tag(f'double_ingots',f'items',f'#forge:double_ingots/{metalName}')
        rm_forge.tag(f'double_sheets',f'items',f'#forge:double_sheets/{metalName}')
        rm_forge.tag(f'ingots',f'items',f'#forge:ingots/{metalName}')
        rm_forge.tag(f'sheets',f'items',f'#forge:sheets/{metalName}')
        rm.tag(f'all_fluids',f'blocks',f'tfcmineralogy:fluid/metal/{metalName}')
        rm.tag(f'metal_plated_blocks',f'blocks',f'tfcmineralogy:metal/block/{metalName}')
        rm.tag(f'{metalName}',f'fluids',f'tfcmineralogy:metal/{metalName}')
        rm.tag(f'{metalName}',f'fluids',f'tfcmineralogy:metal/flowing_{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/ingot/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/double_ingot/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/sheet/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/double_sheet/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/rod/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/block/{metalName}')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/block/{metalName}_slab')
        rm.tag(f'{metalName}',f'items/metal_item',f'tfcmineralogy:metal/block/{metalName}_stairs')

        #rm.lang(f'metal.tfcmineralogy.{metalName}')

        #rm.blockstate(f'tfcmineralogy:cauldron/metal/{metalName}') # Shouldn't this be in TFC's Domain?
        rm.blockstate(f'tfcmineralogy:fluid/metal/{metalName}')
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
        
        rm.block_model(f'tfcmineralogy:metal/chain/{metalName}', {'all':f'tfcmineralogy:block/metal/chain/{metalName}','particle':f'tfcmineralogy:block/metal/block/{metalName}'}, parent='minecraft:block/chain', render='minecraft:cutout')

        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_hanging_off', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}_off'}, parent='minecraft:block/template_hanging_lantern', render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_hanging_on', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}'}, parent='minecraft:block/template_hanging_lantern', render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_off', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}_off'}, parent='minecraft:block/template_lantern',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/lamp/{metalName}_on', {'lantern': f'tfcmineralogy:block/metal/lamp/{metalName}'}, parent='minecraft:block/template_lantern',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_bottom', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_bottom',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_top', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_top',render='minecraft:cutout')
        rm.block_model(f'tfcmineralogy:metal/trapdoor/{metalName}_open', {'texture':f'tfcmineralogy:block/metal/trapdoor/{metalName}'}, parent='block/template_orientable_trapdoor_open',render='minecraft:cutout')

        rm.block_model(f'tfcmineralogy:fluid/metal/{metalName}', {'particle':'block/lava_still'}, parent=None)
        rm.custom_item_model(f'tfcmineralogy:bucket/metal/{metalName}', 'forge:fluid_container', {'parent':'forge:item/bucket', 'fluid':f'tfcmineralogy/metal/{metalName}'})

    if metalUtility:
        # Add Anvil, Lamp, Trapdoor if UTILITY
        rm.tag(f'trapdoors',f'items',f'tfcmineralogy:metal/trapdoor/{metalName}')
        rm.tag(f'lamps',f'blocks',f'tfcmineralogy:metal/lamp/{metalName}')
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
        rm.item_model(f'tfcmineralogy:metal/block/{metalName}',parent=f'tfcmineralogy:block/metal/block/{metalName}', no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/block/{metalName}_slab',parent=f'tfcmineralogy:block/metal/block/{metalName}_slab', no_textures=True)
        rm.item_model(f'tfcmineralogy:metal/block/{metalName}_stairs',parent=f'tfcmineralogy:block/metal/block/{metalName}_stairs', no_textures=True)
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
        # Add to Metal_Item Tool tag:
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/axe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/pickaxe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/shovel/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/sword/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/hammer/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/knife/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/hoe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/chisel/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/propick/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/saw/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/scythe/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/javelin/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/mace/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/tuyere/{metalName}')
        rm.tag(f'{metalName}_tools',f'items/metal_item',f'tfcmineralogy:metal/shears/{metalName}')
        # Deals damage tags for TOOL
        rm.tag(f'deals_slashing_damage',f'items',f'#tfcmineralogy:scythes')
        rm.tag(f'deals_crushing_damage',f'items',f'#tfcmineralogy:hammers')
        rm.tag(f'deals_crushing_damage',f'items',f'#tfcmineralogy:maces')
        rm.tag(f'deals_piercing_damage',f'items',f'#tfcmineralogy:javelins')
        rm.tag(f'deals_piercing_damage',f'items',f'#tfcmineralogy:knives')
        # Add Metal Tools Models
        rm.item_model(f'tfcmineralogy:metal/axe/{metalName}',f'tfcmineralogy:item/metal/axe/{metalName}',parent='item/handheld')
        rm.item_model(f'tfcmineralogy:metal/chisel/{metalName}',f'tfcmineralogy:item/metal/chisel/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/hammer/{metalName}',f'tfcmineralogy:item/metal/hammer/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/hoe/{metalName}',f'tfcmineralogy:item/metal/hoe/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/axe_head/{metalName}',f'tfcmineralogy:item/metal/axe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/chisel_head/{metalName}',f'tfcmineralogy:item/metal/chisel_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/fish_hook/{metalName}',f'tfcmineralogy:item/metal/fish_hook/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/hammer_head/{metalName}',f'tfcmineralogy:item/metal/hammer_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/hoe_head/{metalName}',f'tfcmineralogy:item/metal/hoe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/horse_armor/{metalName}',f'tfcmineralogy:item/metal/horse_armor/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/javelin/{metalName}',f'tfcmineralogy:item/metal/javelin/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/javelin_head/{metalName}',f'tfcmineralogy:item/metal/javelin_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/knife/{metalName}',f'tfcmineralogy:item/metal/knife/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/knife_blade/{metalName}',f'tfcmineralogy:item/metal/knife_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/mace/{metalName}',f'tfcmineralogy:item/metal/mace/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/mace_head/{metalName}',f'tfcmineralogy:item/metal/mace_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/pickaxe/{metalName}',f'tfcmineralogy:item/metal/pickaxe/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/pickaxe_head/{metalName}',f'tfcmineralogy:item/metal/pickaxe_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/propick/{metalName}',f'tfcmineralogy:item/metal/propick/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/propick_head/{metalName}',f'tfcmineralogy:item/metal/propick_head/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/saw/{metalName}',f'tfcmineralogy:item/metal/saw/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/saw_blade/{metalName}',f'tfcmineralogy:item/metal/saw_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/scythe/{metalName}',f'tfcmineralogy:item/metal/scythe/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/scythe_blade/{metalName}',f'tfcmineralogy:item/metal/scythe_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/shears/{metalName}',f'tfcmineralogy:item/metal/shears/{metalName}',parent='tfc:item/handheld')
        rm.item_model(f'tfcmineralogy:metal/shovel/{metalName}',f'tfcmineralogy:item/metal/shovel/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/shovel_head/{metalName}',f'tfcmineralogy:item/metal/shovel_head/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/sword_blade/{metalName}',f'tfcmineralogy:item/metal/sword_blade/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/sword/{metalName}',f'tfcmineralogy:item/metal/sword/{metalName}',parent='tfc:item/handheld_flipped')
        rm.item_model(f'tfcmineralogy:metal/tuyere/{metalName}',f'tfcmineralogy:item/metal/tuyere/{metalName}',parent='item/generated')

        rm.item_model(f'tfcmineralogy:metal/unfinished_helmet/{metalName}',f'tfcmineralogy:item/metal/unfinished_helmet/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_chestplate/{metalName}',f'tfcmineralogy:item/metal/unfinished_chestplate/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_greaves/{metalName}',f'tfcmineralogy:item/metal/unfinished_greaves/{metalName}',parent='item/generated')
        rm.item_model(f'tfcmineralogy:metal/unfinished_boots/{metalName}',f'tfcmineralogy:item/metal/unfinished_boots/{metalName}',parent='item/generated')

        rm.custom_item_model(f'tfcmineralogy:metal/boots/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/boots/{metalName}','trim':'tfc:item/boots_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/chestplate/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/chestplate/{metalName}','trim':'tfc:item/chestplate_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/greaves/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/greaves/{metalName}','trim':'tfc:item/greaves_trim'}})
        rm.custom_item_model(f'tfcmineralogy:metal/helmet/{metalName}', 'tfc:trim', {'parent':'forge:item/default', 'textures':{'armor':f'tfcmineralogy:item/metal/helmet/{metalName}','trim':'tfc:item/helmet_trim'}})

rm_forge.flush()
rm.flush()
