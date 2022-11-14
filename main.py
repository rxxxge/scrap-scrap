import scrapme

def main():
    url = "https://www.bls.gov/regions/midwest/data/AverageEnergyPrices_SelectedAreas_Table.htm"
    file_count = scrapme.get_data(url)
    for counter in range(file_count + 1):
        print(f"Table {counter}")
        scrapme.download_xlsx(file_path_ids = f"ids_{counter}.txt")
    

if __name__ == "__main__":
    main()