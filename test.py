"""
metalName = "arsenical_bronze_hello"
if '_' in metalName:
	splitName = metalName.split("_")
for element in splitName:
	print(element)
    element = element[0].upper() + element[1:]
    langMetalName = " ".join(splitName)	
else:
	langMetalName = metalName[0].upper()+metalName[1:]

print(langMetalName)
"""
metalDict = {"arsenical_bronze",'lead'}
for metal in metalDict:
    if '_' in metal:
        splitName = metal.split('_')
        joinList = list()
        for element in splitName:
            joinList.append(element[0].upper() + element[1:])
        langMetalName = ' '.join(joinList)
    else:
        langMetalName=metal[0].upper()+metal[1:]
    print(langMetalName+';')
