import pandas as pd
import copy
import pickle
import math



def coffeeshop_with_roasting(dfList, location_match="제주특별자치도", only_opened=True):
    # select only "영업상태가 영업 중인 매장"
    if only_opened:
        for i in range(len(dfList)):
            dfList[i] = dfList[i][dfList[i].영업상태구분코드 == 1]
          
    # select only "위치가 location_match 인 매장"
    if location_match != None:
        print("mode location")
        for i in range(len(dfList)):
            dfList[i] = dfList[i][lambda df : df["소재지전체주소"].str[:len(location_match)] == location_match]

    # only select "커피숍" in Cdf 
    business_list = ["커피숍"]#, "까페", "카페", "라이브카페", "키즈카페","기타 휴게음식점"] # <- this will be needed for Ndf. (normal restaurant)
    dfList[0] = dfList[0][lambda df : df["업태구분명"].isin(business_list)]
    
    # find Cdf row in the Fdf, Ftdf, that has same "사업장명".
    # make "사업장명" list
    df = dfList[0]
    Cdf_business = []
    for row in df.iterrows():
        # select "사업장명" data from the row
        business = row[1][4]
        Cdf_business.append(business)
    # find rows in the Fdf, Ftdf, that has same "사업장명" in the Cdf_business
    for i in range(len(dfList)):
        if i == 0:
            continue
        dfList[i] = dfList[i][lambda df : df["사업장명"].isin(Cdf_business)]
    
    fdf_ftdf_concat = pd.concat(dfList[1:3])
    print(fdf_ftdf_concat)
    return fdf_ftdf_concat

def date_to_num(target_date):
    # parse the date and rid only yyyy, mm
    dateList = target_date.split("-")[:3]
    dateList = [int(dateList[0]) - 1900, int(dateList[1])]
    return dateList[0] * 12 + dateList[1]

def num_to_date(target_num):
    reverted_month = target_num % 12
    reverted_year = int((target_num - reverted_month) / 12 + 1900) 

    if reverted_month == 0:
        reverted_month = 12
        reverted_year -= 1

    return str(reverted_year)+'-'+str(reverted_month)+"-01"
    
def coffeeshop_dura_statistic(concated_db, starting_month="1980-01", ending_month="2023-04"):
    """
    # coffeeshop_dura_statistic
    - you first need to run coffeeshop_with_roasting() then get the concated db.
    - then this function will gives you the roastery amout in jeju, month by month.
    - starting month can be specify, and ending month will be 2023-04 by default.
    """

    # bias the x coordinate and ready for indexing
    # note that the whole starting month will be just regarded as opened, 
    # and for opposite, the whole ending month will be regarded as closed.
    datenum_bias = date_to_num(starting_month)
    graph = [[i,0] for i in range(0,date_to_num(ending_month) - date_to_num(starting_month))]
    print(len(graph))
    def dateGrapher(start_date, end_date):
        if type(end_date) != type(" "):
            if math.isnan(end_date):
                end_date = None
        start_num = date_to_num(start_date) - datenum_bias
        if start_num < 0:
            return
        if end_date == None:
            end_date = ending_month
        date_len = date_to_num(end_date) - date_to_num(start_date)
        for i in range(start_num,date_len+start_num):
            graph[i][1] += 1
    
    # make graph
    for row in concated_db.iterrows():
        # select "인허가날짜", "폐업날짜" data from the row
        start_date = row[1][6]
        end_date = row[1][7]
        dateGrapher(start_date, end_date)
    return graph

def find_coffeefinder(dfList):
    for i in range(len(dfList)):
        dfList[i] = dfList[i][dfList[i].사업장명 == "파인더"]
        print(dfList[i])

def find_businessKinds(df):
    businessKinds = []
    for row in df.iterrows():
        # select "사업장명" data from the row
        business = row[1][5]
        # print(business)
        if business in businessKinds:
            pass
        else:
            businessKinds.append(business)
    print(businessKinds)
     

def dfCreate(csv_dir):
        """
        # dfCreate
        - fill df list from selected csv
        args:
            target_csv (str): target csv file. 
        """
        return pd.read_csv(csv_dir, encoding='cp949')
    
# # !!dfCreate section!!

# # Cdf = dfCreate("comfort_restaurant_short_comp.csv")
# # Ftdf = dfCreate("food_temporary_making_short_comp.csv")
# # Fdf = dfCreate("food_making_short_comp.csv")

# Cdf = dfCreate("comfort_restaurant_comp.csv")
# # Ndf = dfCreate("normal_restaurant_comp.csv")
# """
# Ndf col
# ['기타', '한식', '외국음식전문점(인도,태국등)', '일식', '호프/통닭', '뷔페식', '경양식', '김밥(도시락)', '중국식', '분식', '식육(숯불구이)', '탕류(보신용)', '횟집', '라이브카페', '정종/대포집/소주방', '감성주점', '패밀리레스트랑', '냉면집', '출장조리', '통닭(치킨)', '키즈카페', '까페', '복어취급', '패스트푸드', '이동조리', '전통찻집', nan, '일반조리판매', ' 기타 휴게음식점', '커피숍', '193959.150482967', '간이주점', '식품소분업', '제과점영업', '다방', '식품등 수입판매업', '룸살롱']
# """
# Ftdf = dfCreate("food_temporary_making_comp.csv")
# Fdf = dfCreate("food_making_comp.csv")

# dfLists = [Cdf, Fdf, Ftdf]
# # dfLists_normal = [Ndf, Fdf, Ftdf]



       
# jeju = coffeeshop_with_roasting(copy.deepcopy(dfLists), only_opened=False)
# print(jeju[jeju.영업상태구분코드 == 1])

# # jeju = coffeeshop_with_roasting(copy.deepcopy(dfLists),location_match=None, only_opened=False) # korea actually

# jeju.to_csv('jeju_roastery_candidate.csv', index = False, encoding = 'cp949')

jeju = dfCreate('corrected_jejuRoastery.csv')


starting_month="1980-01"
ending_month="2023-04"
jeju_graph = coffeeshop_dura_statistic(jeju, starting_month,ending_month)


#convert the graph obj ([502, 67], [503, 68], [504, 74], ...) to  [YYYY-MM-DD, 68].
jeju_graph_x = []
jeju_graph_y = []
datenum_bias = date_to_num(starting_month)
datenum_len = date_to_num(ending_month) - date_to_num(starting_month)
for i in range(datenum_len):
    if i < 400:
        continue
    current_date = num_to_date(jeju_graph[i][0] + datenum_bias)
    jeju_graph_x.append(current_date)
    jeju_graph_y.append(jeju_graph[i][1])

print(jeju_graph_x)
print(jeju_graph_y)
