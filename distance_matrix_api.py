import requests
import pandas as pd

df2 = pd.read_csv('distance_matrix_real.csv')
df3 = pd.read_csv('duration_matrix_real.csv')

# from google.colab import drive
# drive.mount('/content/drive')

def get_distance_matrix(api_key, sources, destinations):
    url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"

    querystring = {
        "origins": sources,
        "destinations": destinations
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "trueway-matrix.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    api_key = 'API_KEY'

    df = pd.read_csv('tps.csv')

    # Help (source_destination)
    # V(0:25_0:25)       V(0:25_25:50)        V(0:25_50:75)        V(0:25_75:100)       V(0:25_100:113)
    # V(25:50_0:25)      V(25:50_25:50)       V(25:50_50:75)       V(25:50_75:100)      V(25:50_100:113)
    # V(50:75_0:25)      V(50:75_25:50)       V(50:75_50:75)       V(50:75_75:100)      V(50:75_100:113)
    # V(75:100_0:25)     V(75:100_25:50)      V(75:100_50:75)      V(75:100_75:100)     (75:100_100:113)
    # V(100:114_0:25)    V(100:114_25:50)     V(100:114_50:75)     V(100:114_75:100)    V(100:114_100:113)

    source_coordinates = df[['latitude', 'longitude']].iloc[0:25].values.tolist()
    destination_coordinates = df[['latitude', 'longitude']].iloc[25:50].values.tolist()

    # Format coordinates for the API request
    sources = ';'.join([f'{lat},{lon}' for lat, lon in source_coordinates])
    destinations = ';'.join([f'{lat},{lon}' for lat, lon in destination_coordinates])
    print(sources)
    print(destinations)

    distance_matrix = get_distance_matrix(api_key, sources, destinations)

    print(distance_matrix)

    # Convert the distance matrix into a DataFrame
    df_distance = pd.DataFrame(distance_matrix['distances'])
    df_duration = pd.DataFrame(distance_matrix['durations'])

    # Help (start_col-start_row)
    # (1-0)     (26-0)      (51-0)      (76-0)      (101-0)
    # (1-25)    (26-25)     (51-25)     (76-25)     (101-25)
    # (1-50)    (26-50)     (51-50)     (76-50)     (101-50)
    # (1-75)    (26-75)     (51-75)     (76-75)     (101-75)
    # (1-100)   (26-100)    (51-100)    (76-100)    (101-100)

    start_col = 26
    start_row = 0
    
    # Loop through each row in the distances matrix and write to the DataFrame
    for i in range(len(distance_matrix['distances'])):
        row_index = start_row + i
        for j in range(len(distance_matrix['distances'][i])):
            col_index = start_col + j
            df2.iat[row_index, col_index] = distance_matrix['distances'][i][j]

    # Save the updated DataFrame back to a CSV file
    df2.to_csv('distance_matrix_real.csv', index=False)

    for i in range(len(distance_matrix['durations'])):
        row_index = start_row + i
        for j in range(len(distance_matrix['durations'][i])):
            col_index = start_col + j
            df3.iat[row_index, col_index] = distance_matrix['durations'][i][j]

    # Save the updated DataFrame back to a CSV file
    df3.to_csv('duration_matrix_real.csv', index=False)


