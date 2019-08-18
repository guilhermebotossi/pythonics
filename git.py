import requests
import json
import base64
import re
from datetime import datetime
import time

username = 'guilhermebotossi@gmail.com'
token = 'd2bdcf02c03ac7137a07b17f7814378398cd4ebf'
config_key_regex_pattern = "\@Config\.Key\(\"(.*)\"\)\s+\@DefaultValue\(\"(.*)\"\)|\@DefaultValue\(\"(.*)\"\)\s+\@Config\.Key\(\"(.*)\"\)|\@Config\.Key\(\"(.*)\"\)"
config_key_regex = re.compile(config_key_regex_pattern)
key_regex_pattern = "\@Key\(\"(.*)\"\)\s+\@DefaultValue\(\"(.*)\"\)|\@DefaultValue\(\"(.*)\"\)\s+\@Key\(\"(.*)\"\)|\@Key\(\"(.*)\"\)"
key_regex = re.compile(key_regex_pattern)
url = "https://api.github.com/search/code?q=%22import%20org.aeonbits.owner.Config%22+in:file+language:Java+org:ContaAzul&per_page=100"

gh_session = requests.Session()
gh_session.auth = (username, token)

properties = {}
page = 1
while True:
    full_url = url + "&page=" + str(page)
    print(full_url)
    response = json.loads(gh_session.get(full_url).text)

    print("Quantidade de Itens no Response : " + str(len(response["items"])))
    for item in response["items"]:
        file = json.loads(gh_session.get(item["url"]).text)
        content = base64.b64decode(file["content"]).decode('UTF-8')  
        if "import org.aeonbits.owner.Config;" in content :
            matches = config_key_regex.findall(content)
            if not matches :
                matches = key_regex.findall(content)
            
            for match in matches:
                prop = {}   
                ## nome index 0,3,4
                name = match[0] if match[0] else match[3] if match[3] else match[4]
                prop["name"] = name
                prop["project_location"] = item["repository"]["full_name"]
                prop["filename"] = item["name"]
                ## defaultvalue 1, 2
                prop["defaultValue"] = match[1] if match[1] else match[2]
                ## nome index 0,3
                prop["hasDefaultValue"] = True if match[0] or match[3] else False
                prop["description"] = "" 
                properties[name] = prop

    if len(response["items"]) < 100 :
        break
    page+=1
    print("Aguardando 60 segundos para nova busca")
    time.sleep(60)

output_file = "config_" + str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')) + ".properties"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(properties, f, ensure_ascii=False, indent=4)
