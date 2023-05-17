import urllib.request
import csv
import json

client_id = "8CG2J7yPuOxb4x2_E9Sy"
client_secret = "mecMAx7RJa"

url = "https://openapi.naver.com/v1/search/local.json"
url_web = "https://openapi.naver.com/v1/search/webkr.json"
option = "&display=5&sort=count"
option_web = "&display=5&sort=count"
corrected_csv = []
with open("jeju_roastery_candidate.csv", "r",encoding="cp949") as f:
    jeju_csv = csv.reader(f)
    for line in jeju_csv:
        if line[4] == "사업장명":
            corrected_csv.append(line)
            continue
        print(line[4])


        # request localsearch
        query = "?query="+urllib.parse.quote(line[4][:])
        url_query = url + query + option

        request = urllib.request.Request(url_query)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)

        response = urllib.request.urlopen(request)
        rescode = response.getcode()


        #request websearch
        query = "?query="+urllib.parse.quote(line[4][:]+" 제주")
        url_query = url_web + query + option_web

        request = urllib.request.Request(url_query)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)

        response_web = urllib.request.urlopen(request)
        rescode_web = response_web.getcode()

        if(rescode == 200 and rescode_web == 200):
            response_body = response.read().decode('utf-8')
            response_body_web = response_web.read().decode('utf-8')
            JSON_obj = json.loads(response_body)
            JSON_obj_web = json.loads(response_body_web)
            for item in JSON_obj["items"]:
                if "제주특별자치도" in item["address"][:7]:
                    print(item)
            i = 0
            for item in JSON_obj_web["items"]:
                if i >= 2:
                    break
                print(item)
                i += 1
            ask = input("해당 매장을 로스터리로 분류합니까? (Y/n)  : ")
            if ask == "n":
                continue
            else:
                corrected_csv.append(line)
        else:
            print("Error code:"+rescode)

with open('corrected_jejuRoastery.csv', 'w', newline='', encoding='cp949') as f:
    jeju_csv = csv.writer(f)
    for line in corrected_csv:
        jeju_csv.writerow(line)