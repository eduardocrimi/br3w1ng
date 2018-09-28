import glob, os
import xml.etree.ElementTree as ET
import csv

path = 'beerxmls'
os.chdir(path)
files = []
fermentables = []

shoppingList = {}
for file in glob.glob("*.xml"):
    files.append(file)
for f in files:
    root = ET.parse(os.path.join(os.path.dirname(f), f)).getroot()
    fermentables = root.iter('FERMENTABLE')
    for malt in fermentables:
        name = malt.findall('NAME')
        kg = malt.findall('AMOUNT')
        if name[0].text not in shoppingList:
            shoppingList[name[0].text] = {'kg':0,'qty':0, 'type': 'A'}
        shoppingList[name[0].text]['kg']= float(kg[0].text) + shoppingList[name[0].text]['kg']
    hops = root.iter('HOP')
    for hop in hops:
        name = hop.findall('NAME')
        kg = hop.findall('AMOUNT')
        if name[0].text not in shoppingList:
            shoppingList[name[0].text] = {'kg':0,'qty':0, 'type': 'B'}
        shoppingList[name[0].text]['kg'] = float(kg[0].text) + shoppingList[name[0].text]['kg']
    yeasts = root.iter('YEAST')
    for yeast in yeasts:
        name = yeast.findall('NAME')
        if name[0].text not in shoppingList:
            shoppingList[name[0].text] = {'kg':0,'qty':0, 'type': 'C'}
        shoppingList[name[0].text]['qty'] = 1 + shoppingList[name[0].text]['qty']

with open('pedido.csv','w') as csvfile:
    fieldnames = ['item', 'kg', 'cantidad']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for key, value in shoppingList.items():
        if(value['type']=='A'):
            writer.writerow({'item': key, 'kg': value['kg'], 'cantidad': value['qty']})
    for key, value in shoppingList.items():
        if(value['type']=='B'):
            writer.writerow({'item': key, 'kg': value['kg'], 'cantidad': value['qty']})
    for key, value in shoppingList.items():
        if(value['type']=='C'):
            writer.writerow({'item': key, 'kg': value['kg'], 'cantidad': value['qty']})


print(shoppingList)