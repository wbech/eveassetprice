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
			typeids[typeid]= int(quantity)
		else:
			typeids[typeid] += int(quantity)
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
	return avg

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
	iteminfo= {}
	for item in typeids.keys():
		try:
			item_name= get_item_name(get_quicklook(item,usesystem))
			avg= get_avg(get_itemxml(item,usesystem))	
			iteminfo[item_name]=[avg,item]
		except:
			print "Error for item:",item
			continue
	return iteminfo
	
#prints each iteminfo key and value on separate line
def print_separate(iteminfo):
	for key, value in iteminfo.iteritems():
			print key, value	

print_separate(all_assets(keyID,vCode,charID,usesystem))




