import json


class ReadJson:
    def get_user_property_details(self):
        try:
            user_detail = {}
            with open(r'F:\LeanIX_Assessment\Assessment\assessment.json', 'r') as f:
                playlist = json.load(f)

            for i in range(len(playlist["content"])):
                if "AmazonIamUser" in playlist["content"][i]['type']:
                    access_key_age = playlist["content"][i]["data"]["Properties"]["AccessKeyAge"]
                    adk_name = playlist["content"][i]["data"]["Properties"]["ADK_Name"]
                    user_detail[adk_name] = access_key_age.split(" ")[0]
                    # age_lst.append(access_key_age.split(" ")[0])  ## Space split and index 1
            return user_detail
        except Exception as Error:
            return Error


if __name__ == '__main__':
    readjson_obj = ReadJson()
    print(readjson_obj.get_user_property_details())
