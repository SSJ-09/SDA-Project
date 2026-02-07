import dataLoader  

def main():
    csv_file = "Copy of gdp_with_continent_filled.csv" 
    json_file = "config.json"

    try:
        config = dataLoader.load_config(json_file)
        print(config) 
       
        data = dataLoader.load_gdp_data(csv_file)
        
        print(f"\rows loaded: {len(data)}")
        
        for i in range(3):
            if i < len(data): 
                print(data[i])

    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
    except Exception as e:
        print(f"\unexpected error: {e}")



if __name__ == "__main__":
    main()