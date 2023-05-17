import csv
def shorter(name):
    csv_shorten = []
    with open(name, 'r',encoding="cp949") as f:     
        reader = csv.reader(f)
        i = 0
        for line in reader:
            i += 1
            if i % 35 == 0 or i==1:
                csv_shorten.append(line)
        print(reader.line_num)
    with open(name.split(".")[0]+"_short.csv", 'w', encoding="cp949",newline="") as f:
        writer = csv.writer(f)
        for line in csv_shorten:
            if len(line) == 0:
                continue
            writer.writerow(line)

def colcompress(name, *selectedCol):
    csv_compressed = []
    selectedCol = list(selectedCol)
    with open(name, 'r',encoding="cp949") as f:     
        reader = csv.reader(f)
        i = 0
        for line in reader:
            i += 1
            selected_colData = []
            for i in selectedCol:
                selected_colData.append(line[i])
            csv_compressed.append(selected_colData)
        print(reader.line_num)

    # col0 번호, primary key
    # col1 개방서비스명, 각 파일별로 "휴게음식점", "즉석판매제조가공업", "식품제조가공업"
    # col7 영업상태, 3=폐업, 1=영업중
    # col18 소재지전체주소, 서울특별시 마포구 성산동 253-14 과 같은 형식
    # col25 업태구분, 고속도로 과자점 "커피숍" 푸드트럭 등등...
    # col21 사업장명, 사업장 이름.
    # col5 인허가일자, 해당 허가를 받은 일자, YYYY-MM-DD
    # col11 폐업일자, 폐업을 한 일자, YYYY-MM-DD

    with open(name.split(".")[0]+"_comp.csv", 'w', encoding="cp949",newline="") as f:
        writer = csv.writer(f)
        for line in csv_compressed:
            if len(line) == 0:
                continue
            writer.writerow(line)
def addRow_matchRow(targetCSV, adderCSV, targetmatchRow,addermatchRow, addRow, addingName):
    corrected = []
    with open(targetCSV, encoding="cp949") as t:
        with open(adderCSV, encoding="cp949") as a:
            reader_t = csv.reader(t)
            reader_a = csv.reader(a)
            stt = False
            for line in reader_t:
                if stt == False:
                    corrected.append(line + [addingName])
                    stt = True
                    continue
                for adderRow in reader_a:
                    if line[targetmatchRow][:] == adderRow[addermatchRow][:]:
                        line.append(adderRow[addRow])
                        break
                corrected.append(line)

    with open(targetCSV.split(".")[0]+"_added.csv", 'w', encoding="cp949",newline="") as f:
        writer = csv.writer(f)
        for line in corrected:
            if len(line) == 0:
                continue
            writer.writerow(line)


# shorter("normal_restaurant.csv")

# colcompress("comfort_restaurant_short.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("normal_restaurant_short.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("food_making_short.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("food_temporary_making_short.csv", 0, 1, 7, 18, 21, 25, 5, 11)

# colcompress("comfort_restaurant.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("normal_restaurant.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("food_making.csv", 0, 1, 7, 18, 21, 25, 5, 11)
# colcompress("food_temporary_making.csv", 0, 1, 7, 18, 21, 25, 5, 11)

addRow_matchRow("corrected_jejuRoastery.csv", "comfort_restaurant_comp.csv", 4, 4,6,"휴게음식점인허가일자")