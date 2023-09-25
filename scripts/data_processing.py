import pandas as pd
import numpy as np
import psycopg2

'''
The script demonstrates data cleaning and processing on the flat file and data insertion.
It is for reference only, in this project data insertion is done using NiFi.
'''


# create central table
try:
    df = pd.read_csv('../data/melb_data.csv')

    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=housing user=postgres password=postgres")
    cur = conn.cursor()

    print(df.isnull().sum())

    # mapping

    # councilarea
    cur.execute('SELECT council_area_id, name FROM councilarea;')
    councilarea_to_id = {name: council_area_id for council_area_id, name in cur.fetchall()}

    # region
    cur.execute('SELECT region_id, name FROM region;')
    region_to_id = {name: region_id for region_id, name in cur.fetchall()}

    # seller
    cur.execute('SELECT seller_id, name FROM seller;')
    seller_to_id = {name: seller_id for seller_id, name in cur.fetchall()}

    # suburb
    cur.execute('SELECT suburb_id, name FROM suburb;')
    suburb_to_id = {name: suburb_id for suburb_id, name in cur.fetchall()}

    df['suburb_id'] = df['Suburb'].map(suburb_to_id)
    df['council_area_id'] = df['CouncilArea'].map(councilarea_to_id)
    df['region_id'] = df['Regionname'].map(region_to_id)
    df['seller_id'] = df['SellerG'].map(seller_to_id)

    df.rename(columns={
        'Method': 'method_code',
        'Type': 'type_code',
    }, inplace=True)

    # drop columns
    df.drop(columns=['Suburb', 'CouncilArea', 'Regionname', 'SellerG', 'Postcode', 'Propertycount'], inplace=True)

    print(df.isnull().sum())
    df.fillna(value=np.nan, inplace=True)

    df = df[[
        'Address', 'Rooms', 'Bedroom2', 'Bathroom', 'Car',
        'Landsize', 'BuildingArea', 'YearBuilt', 'Distance', 'Price',
        'Lattitude', 'Longtitude', 'suburb_id', 'type_code', 'seller_id',
        'method_code', 'region_id', 'council_area_id', 'Date']]

    print(df.dtypes)
    print(df.head())
    print(df.isnull().sum())

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

    # Explicitly convert to Python's native int
    int_cols = ['Rooms', 'Bedroom2', 'Bathroom', 'suburb_id', 'region_id', 'seller_id', 'Car']
    for col in int_cols:
        df[col] = df[col].apply(lambda x: int(x) if pd.notna(x) else None)

    # Explicitly convert to Python's native float
    float_cols = ['Price', 'Distance', 'Landsize', 'BuildingArea', 'YearBuilt', 'Lattitude', 'Longtitude', 'council_area_id']
    for col in float_cols:
        df[col] = df[col].apply(lambda x: float(x) if pd.notna(x) else None)

    # Convert object to native Python str
    str_cols = ['Address', 'type_code', 'method_code', 'Date']
    for col in str_cols:
        df[col] = df[col].astype(str)

    print(df.dtypes)

    for record in df.to_records(index=False):
        try:
            record = tuple(x.item() if hasattr(x, 'item') else x for x in record)

            print(type(x) for x in record)

            cur.execute("""
                    INSERT INTO property (
                        address, rooms, bedroom_2, bathroom, car,
                        land_size, building_area, year_built, distance, price,
                        latitude, longitude, suburb_id, type_code, seller_id,
                        method_code, region_id, council_area_id, post_date
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                ) ON CONFLICT DO NOTHING;
            """, record)

            conn.commit()
        except Exception as e:
            print(f"An error occurred for record {record}: {e}")
            print(f"PostgreSQL error: {e.pgerror}")
            break

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()

#%%
