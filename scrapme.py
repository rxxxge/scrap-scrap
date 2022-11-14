from libs import *

headers = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

def get_data(url):
    cur_date = datetime.now().strftime("%m_%d_%Y")
    response = requests.get(url = url, headers = headers)

    with open("index.html", "w") as file:
        file.write(response.text)

    with open("index.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    tables = soup.find_all("table")

    file_counter = 0
    for index, table in enumerate(tables):
        data_th = table.find("thead").find_all("tr")[-1].find_all("th")

        table_headers = ["Area"]
        for dth in data_th:
            dth = dth.text.strip()
            table_headers.append(dth)

        workbook = xlsxwriter.Workbook(f"data_{cur_date}_({index}).xlsx")
        worksheet = workbook.add_worksheet(table.find("span", class_ = "tableTitle").text)

        row = 0
        col = 0

        for i, header in enumerate(table_headers):
            worksheet.write(row, col + i, header)
        row += 1

        tbody_trs = table.find("tbody").find_all("tr")

        data = []
        ids = []
        for tr in tbody_trs:
            t_data = []
            area = tr.find("th").text.strip()

            data_by_month = tr.find_all("td")
            t_data.append(area)
            for dbm in data_by_month:
                if dbm.find("a"):
                    area_data = dbm.find("a").get("href")
                    id = area_data.split("/")[4].split("?")[0]
                    ids.append(id)
                    
                elif dbm.find("span"):
                    area_data = dbm.find("span").text.strip()
                else:
                    area_data = "None"

                t_data.append(area_data)
            data.append(t_data)

        for i, area in enumerate(data):
            for j, element in enumerate(area):
                worksheet.write(row, col + j, element)
            row += 1

        workbook.close()


        with open(f"ids_{index}.txt", "w") as file:
            for id in ids:
                file.write(f'{id}\n')

        file_counter = index

        

    print("Tables Done")
    return file_counter


def download_xlsx(file_path_ids, xlsx_path = "xlsx"):
    with open(file = file_path_ids) as file:
        ids = [line.strip() for line in file.readlines()]


    for i, id in enumerate(ids):
        cookies = {
            '_ga': 'GA1.3.781093904.1668348574',
            '_gid': 'GA1.3.2006440337.1668348574',
            'nmstat': '701ffe8a-8bd0-16d8-3a47-e02feb6bab92',
            '_ga': 'GA1.2.173814881.1668348577',
            '_gid': 'GA1.2.301342010.1668348577',
        }

        headers = {
            'Host': 'data.bls.gov',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://data.bls.gov',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7',
            'Connection': 'close',
            # Requests sorts cookies= alphabetically
            # 'Cookie': '_ga=GA1.3.781093904.1668348574; _gid=GA1.3.2006440337.1668348574; nmstat=701ffe8a-8bd0-16d8-3a47-e02feb6bab92; _ga=GA1.2.173814881.1668348577; _gid=GA1.2.301342010.1668348577',
        }

        data = {
            'request_action': 'get_data',
            'reformat': 'true',
            'from_results_page': 'true',
            'years_option': 'specific_years',
            'delimiter': 'comma',
            'output_type': 'multi',
            'periods_option': 'all_periods',
            'output_view': 'data',
            'output_format': 'excelTable',
            'original_output_type': 'default',
            'annualAveragesRequested': 'false',
            'series_id': f'{id}',
        }

        response = requests.post('https://data.bls.gov/pdq/SurveyOutputServlet', cookies=cookies, headers=headers, data=data, verify=False)

        with open(file = f'{xlsx_path}/{id}.xlsx', mode = 'wb') as file:
            file.write(response.content)

        print(f'{i+ 1}/{len(ids)}')