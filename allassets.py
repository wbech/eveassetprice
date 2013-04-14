import urllib
import xml.etree.ElementTree as ET
import StringIO

#api used to obtain assetxml for character
def get_assets(keyID,vCode,charID):
	url="https://api.eveonline.com/char/AssetList.xml.aspx?"\
		"keyID={}&vCode={}&characterID={}".format(keyID,vCode,charID)
	assetxml= StringIO.StringIO(urllib.urlopen(url).read())
	return assetxml

#returns all typeids and the quantity of item
def all_typeids(assetxml):	
	tree= ET.parse(assetxml)
	root= tree.getroot()
	typeids= {}
	for row in root.iter('row'):
		typeid= row.get('typeID')
		quantity= row.get('quantity')
		if typeid not in typeids:
			typeids[typeid]= [int(quantity)]
		else:
			typeids[typeid][0] += int(quantity)
	return typeids
	
#api used to obtain marketstat xml for item
def get_itemxml(typeid,usesystem):
	url= "http://api.eve-central.com/api/"\
	"marketstat?typeid={}&usesystem={}".format(typeid,usesystem)
	marketstatxml= StringIO.StringIO(urllib.urlopen(url).read())
	return marketstatxml
	
#returns average sell price for item	
def get_avg(marketstatxml):
	tree= ET.parse(marketstatxml)
	root= tree.getroot()
	for sell in root.iter('sell'):
		avg= sell.find('avg').text
	return float(avg)

#api used to obtain quicklook xml for item
def get_quicklook(typeid,usesystem): 
	url= "http://api.eve-central.com/api/"\
	"quicklook?typeid={}&usesystem={}".format(typeid,usesystem)
	quicklookxml= StringIO.StringIO(urllib.urlopen(url).read())
	return quicklookxml

#returns item name for typeid
def get_item_name(quicklookxml):
	tree= ET.parse(quicklookxml)
	root= tree.getroot()
	for item in root.iter('quicklook'):
		item_name= item.find('itemname').text
	return item_name
	
#puts average sell price for each item in assets into the dictionary iteminfo
def all_assets(keyID,vCode,charID,usesystem):
	typeids= all_typeids(get_assets(keyID,vCode,charID))
	for item in typeids.keys():
		try:
			item_name= get_item_name(get_quicklook(item,usesystem))
			avg= get_avg(get_itemxml(item,usesystem))	
			typeids[item].append(avg)
			typeids[item].append(item_name)
		except:
			print "Error for item:", item
			del typeids[item]
			continue
	return typeids
	
#adds avg*quantity for each item
#prints sum of all items
def total_item_val(typeids):
	sum = 0
	for item in typeids.keys():
		total_val= typeids[item][0]*typeids[item][1]
		typeids[item].append(total_val)
		sum += typeids[item][3]
	print "Total worth of all items", "{:,}".format(sum)
	return typeids
	
#prints each iteminfo key and value on separate line
def print_separate(iteminfo):
	for key, value in iteminfo.iteritems():
			print key, value	

print_separate(total_item_val(all_assets(keyID,vCode,charID,usesystem)))




