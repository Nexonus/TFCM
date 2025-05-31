from mcresources.resource_manager import ResourceManager
import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(ROOT_DIR, 'src/main/resources')

rm = ResourceManager(domain='tfcmineralogy', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_tfc = ResourceManager(domain='tfc', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
rm_forge = ResourceManager(domain='forge', resource_dir=RESOURCES_DIR, indent=2, ensure_ascii=False)
os.makedirs(RESOURCES_DIR, exist_ok=True)

quality_dict = {'poor', 'normal', 'rich'}
meltable_minerals = {'mineral':['smithsonite','galena'],
                     'fluid':['zinc','lead'],
                     'melting_temperature':[420,380],
                     'quality':['poor','normal','rich'],
                     'amount':[15,25,35]}
#result_fluid = ['zinc','lead']
#melting_temperature = [420,380]
recipe = set()
#updated_ingredients = {'ingredient': [*collapse_ingredients], 'result':f'tfc:rock/cobble/{stone}'}

for mineral in meltable_minerals['mineral']:
    for quality in meltable_minerals['quality']:
        mineral_quality = quality+"_"+mineral
        recipe = {'ingredient': mineral_quality, 'result_fluid':f'tfc:metal/{meltable_minerals['fluid']}', 'amount': f'{meltable_minerals["amount"]}','temperature':meltable_minerals['melting_temperature']}
        rm.recipe(f'heating/ore/mineral_quality','tfc:heating',recipe)

rm.flush() # GOT TO FIX THIS CODE
