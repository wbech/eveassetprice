import urllib

#api used to obtain xml of assets for a character
def get_assets(keyID,vCode,charID):
	url="https://api.eveonline.com/char/AssetList.xml.aspx?"\
		"keyID={}&vCode={}&characterID={}".format(keyID,vCode,charID)
	assetxml= urllib.urlopen(url).read()
	return assetxml

#returns one typeid from xml        
def get_next_typeid(assetxml):
    start= assetxml.find('typeID="')
    if start == -1:
    	return None,0
    start_id= assetxml.find('"',start)
    end_id= assetxml.find('"', start_id + 1)
    id= assetxml[start_id+1:end_id]
    return id, end_id
 
#creates list of all typeids    
def all_typeids(assetxml):
	typeids= []
	while True:
		id, endpos= get_next_typeid(assetxml)
		if id:
			if id not in typeids:
				typeids.append(id)
				assetxml= assetxml[endpos:]
			else:
				assetxml= assetxml[endpos:]
		else:
			break
	return typeids
	
#api used to obtain marketstat xml for item
def get_itemxml(typeid,usesystem):
	url= "http://api.eve-central.com/api/marketstat?typeid="+str(typeid)+"&usesystem="+str(usesystem)
	marketstatxml= urllib.urlopen(url).read()
	return marketstatxml
	
#returns average sell price for item	
def get_avg(marketstatxml):
	start= marketstatxml.find("<sell>")
	start_avg= marketstatxml.find("<avg>",start)
	end_avg= marketstatxml.find("</avg>",start_avg)
	avg= marketstatxml[start_avg+5:end_avg]
	if avg == None:
		return 0
	else:
		return avg

#api used to obtain quicklook xml for item
def get_quicklook(typeid,usesystem): 
	url= "http://api.eve-central.com/api/quicklook?typeid="+str(typeid)+"&usesystem="+str(usesystem)
	quicklookxml= urllib.urlopen(url).read()
	return quicklookxml

#returns item name for typeid
def get_item_name(quicklookxml):
	start= quicklookxml.find("<itemname>")
	start_name= quicklookxml.find(">",start)
	end_name= quicklookxml.find("</itemname>",start_name)
	item_name= quicklookxml[start_name+1:end_name]
	return item_name
	
#puts average sell price for each item in assets into the dictionary iteminfo
def all_assets(keyID,vCode,charID,usesystem):
	typeids= all_typeids(get_assets(keyID,vCode,charID))
	iteminfo= {}
	for item in typeids:
		item_name= get_item_name(get_quicklook(item,usesystem))
		avg= get_avg(get_itemxml(item,usesystem))	
		iteminfo[item_name]=[avg,item]
	return iteminfo

#prints each iteminfo key and value on separate line
def print_separate(iteminfo):
	for key, value in iteminfo.iteritems():
			print key, value	

#print_separate(all_assets(keyID,vCode,charID,usesystem))




