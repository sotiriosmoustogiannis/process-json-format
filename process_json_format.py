import requests
import pandas as pd
import json 

headers = {
    "Fiware-Service":"alicante"
}

list_green_area_devices = [6003137,6003140,6005386,6007934,6011498,6017429,6018733,6026882,6029315,6043252,6066815,6076287,6077338,6079329,6080043,6089200,6093638,6105526,6112839,6117406,6119860,6119888,6119889,6119989,6119990,6120028,6120069,6120070,6120092,6120493,6122031,6123607,6123928,6127082,6129290,6129318,6129348,6130343,6130619,6130620,6131462,6131516,6131608,6131681,6131711,6131741,6133182,6134058,6135744,6138370,6146235,6146238,6147171,6147185,6149506,6152423,6154750,6154821,6155819,6158296,6158631,6158650,6160999,6166318,6172797,6174142,6226054,6234996,6234998,6235500,6237396,6239342,6241668,6246321,6249830,6252528,6253674,6257473,6258150,6258151,6258844,6261513,6266299,6268230,6291083,6296098,6296282,6296283,6296954,6301600,6302718,6302723,6304860,6307638,6307651,6310968,6315170,6315557,6315747,6315749,6316918,6319155,6321487,6322613,6322732,6323247,6324279,6324546,6326197,6327704,6328280,6331651,6331792,6332631,6332652,6332755,6332902,6332982,6332990,6333363,6334303,6334922]
list_sport_facilities_devices = [6039793,6066013,6066015,6066017,6122462,6138617,6145253,6172534,6226944,6264775,6325199,6327690,6329838,6330672,6331428,6331559]
list_schools_devices = [6146932,6079267,6259674,6062776,6066670,6051908,6110115,6112542,6112543,6078312,6095894,6095117,6095118,6035158,6119151,6110009,6132315,6051079,6106301,6047798,6027532,6028097,6037929,6038740,6039781,6039790,6046403,6050127,6054169,6061913,6065453,6065809,6066661,6067040,6083318,6095967,6095968,6110109,6119419,6124471,6124636,6153577,6171696,6171944,6172870,6260661,6306462,6322730,6329253,6329360,6330883,6331871,6093645,6158464,6123221,6120226,6130563,6133499,6127593,6146237,6119418,6165813,6052536,6253962,6099256,6099257,6144972,6157148,6172600,6325716,6039344,6157669,6254933,6266795,6227847,6083316,6069247,6139960,6027658,6255195,6232155,6332143,6140331,6316821,6066671]
list_other_devices = [6033210,6051559,6060189,6073392,6096695,6123387,6135303,6138585,6138615,6146030,6315677,6003227,6003229,6004154,6005078,6006131,6006183,6006377,6008724,6008732,6023857,6117400,6119241,6146493,6147186,6147255,6171698,6172019,6236224,6252595,6259477,6323978,6330269,6333663,6333886,6333887,6333888,6005124,6173496,6004752,6005048,6005126,6005127,6005128,6005131,6005233,6005234,6005235,6005246,6005403,6006124,6016146,6039963,6040580,6049229,6089153,6145058,6172535,6241154,6246175,6249611,6249613,6254283,6309800,6309806,6311995,6320524,6327901,6336334,6003955,6004153,6006211,6006291,6022859,6038940,6045505,6049228,6060366,6063042,6069257,6073091,6078338,6085166,6113049,6119239,6119727,6120095,6120127,6121589,6121708,6131376,6138470,6142416,6144977,6149505,6154106,6160995,6171694,6171695,6171975,6172587,6173886,6226915,6243163,6250107,6251920,6252527,6263582,6263583,6266797,6293486,6306439,6306497,6307719,6309820,6324643,6325682,6327503,6327504,6327606,6327705,6328004,6328175,6333383,6334113,6033804,6041567,6084396,6084399,6312826]

#Take a list of devices ids
#Fetch the already existed devices (json format) and pass them into a list of jsons
def fetch_list_json (headers,list_devices):

    fetched_list_json = []
    
    for i in range(len(list_devices)):
        entity = 'https://naiades.simavi.ro/context-api/ngsi-ld/v1/entities/urn:ngsi-ld:Device:{}'.format(list_devices[i])
        r = requests.get(entity,headers=headers)
        fetched_list_json.append(r.json())
        
    return fetched_list_json
    
    
    
#Take the fetched list of jsons
#Then create a new format of jsons (like we want)
def process_create_new_jsons(fetched_list_json):
    
    list_new_device_dicts = []

    for j in range(len(fetched_list_json)):
        device_entity = {}
        keys = ["type", "name", "device", "location","date"]
        
        device_entity[keys[0]] = fetched_list_json[j]['description']['value']
        device_entity[keys[1]] = fetched_list_json[j]['name']['value']
        device_entity[keys[2]] = int(fetched_list_json[j]['serialNumber']['value'])
        device_entity[keys[3]] = fetched_list_json[j]['location']['value']['coordinates']
        device_entity[keys[4]] = "2018-12-31T21:00:00.00Z"
        #add a new part of json
        device_entity.update(
            {"short-term": [
            {
                "alert": "",
                "action": ""
            },
            {
                "alert": "",
                "action": ""
            },
            {
                "alert": "",
                "action1": "",
                "action2": "",
                "action3": ""
            }
            ],
            "medium_term": [
            {
                "alert": "",
                "action": ""
            },
            {
                "alert": "",
                "action1": "",
                "action2": "",
                "action3": ""
            }
            ],
            "long_term": [
            {
                "alert": "",
                "action": ""
            },
            {
                "alert": "",
                "action1": "",
                "action2": "",
                "action3": ""
            }
            ],
            "daily _consumption": 0,
            "weekly_consumption": 0,
            "monthly_consumption": 0}
        )
        list_new_device_dicts.append(device_entity)
        
    return list_new_device_dicts
    
    
#Call the fetch_list_json function to get the already existed device jsons
fetched_list_sport_json = fetch_list_json(headers,list_green_area_devices)


#Call the process_create_new_jsons function to create new json formats
list_new_device_dicts = process_create_new_jsons(fetched_list_sport_json)
    
#Get the new dict to convert it to json and save it
new_format_json = json.dumps(list_new_device_dicts, indent = 2) 
with open("new_json.json", "w") as outfile:
    outfile.write(new_format_json)

