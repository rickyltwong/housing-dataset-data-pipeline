import pandas as pd
import psycopg2

'''
The script extract all attributes from the flat file and insert them into attribute tables.
'''

# create attribute tables
try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=housing user=postgres password=postgres")
    cur = conn.cursor()

    df = pd.read_csv('../data/melb_data.csv')
    # CouncilArea table
    subset_councilarea_tbl = ['CouncilArea']
    distinct_df_councilarea = df[subset_councilarea_tbl].drop_duplicates()
    distinct_councilarea_list = [tuple(x) for x in distinct_df_councilarea.to_records(index=False)]

    for councilarea, in distinct_councilarea_list:
        cur.execute("INSERT INTO councilarea (name) VALUES (%s) ON CONFLICT DO NOTHING;", (councilarea,))

    # Method table
    method_tuples = [
        ("S", "property sold"),
        ("SP", "property sold prior"),
        ("PI", "property passed in"),
        ("PN", "sold prior not disclosed"),
        ("SN", "sold not disclosed"),
        ("NB", "no bid"),
        ("VB", "vendor bid"),
        ("W", "withdrawn prior to auction"),
        ("SA", "sold after auction"),
        ("SS", "sold after auction price not disclosed"),
        ("N/A", "price or highest bid not available")
    ]

    for method_code, description in method_tuples:
        cur.execute("INSERT INTO method (method_code, description) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (method_code, description))

    # Region table
    subset_region_tbl = ['Regionname']
    distinct_df_region = df[subset_region_tbl].drop_duplicates()
    distinct_region_list = [tuple(x) for x in distinct_df_region.to_records(index=False)]

    for region_name, in distinct_region_list:
        cur.execute("INSERT INTO region (name) VALUES (%s) ON CONFLICT DO NOTHING;", (region_name,))

    # Seller table
    subset_seller_tbl = ['SellerG']
    distinct_df_seller = df[subset_seller_tbl].drop_duplicates()
    distinct_seller_list = [tuple(x) for x in distinct_df_seller.to_records(index=False)]

    for seller, in distinct_seller_list:
        cur.execute("INSERT INTO seller (name) VALUES (%s) ON CONFLICT DO NOTHING;", (seller,))

    # Type table
    property_type_tuples = [
        ("br", "bedroom(s)"),
        ("h", "house, cottage, villa, semi, terrace"),
        ("u", "unit, duplex"),
        ("t", "townhouse"),
        ("dev site", "development site"),
        ("o res", "other residential")
    ]

    for type_code, description in property_type_tuples:
        cur.execute("INSERT INTO type (type_code, description) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (type_code, description))

    # Suburb table
    subset_suburb_tbl = ['Suburb', 'Postcode', 'Propertycount']
    distinct_df_suburb = df[subset_suburb_tbl].drop_duplicates()
    distinct_suburb_list = [tuple(x) for x in distinct_df_suburb.to_records(index=False)]

    for suburb, postcode, propertycount in distinct_suburb_list:
        cur.execute("INSERT INTO suburb (name, postcode, property_count) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", (suburb, postcode, propertycount))

    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()