import requests
import pandas as pd

# Load store_list.xlsx into a DataFrame
store_list_df = pd.read_excel('store_list.xlsx')

# Create an empty list to store the section IDs
section_ids = []

# Iterate through rows in store_list DataFrame to get section IDs
for index, row in store_list_df.iterrows():
    store_id = row['store_id']
    branch_id = row['branch_id']

    # Define the URL to get section IDs
    sections_url = f"https://api.express24.uz/client/v4/store/{store_id}/menu?branchId={branch_id}"

    # Send a GET request to the URL
    sections_response = requests.get(sections_url)

    # Check if the request was successful (status code 200)
    if sections_response.status_code == 200:
        # Parse the JSON data to get section IDs
        sections_data = sections_response.json()
        sections = sections_data.get('sections', [])
        section_ids += [section['id'] for section in sections]

# Create an empty list to store the full data
data_list = []

# Iterate through rows in store_list DataFrame and section IDs
for index, row in store_list_df.iterrows():
    store_id = row['store_id']
    branch_id = row['branch_id']

    for parent_id in section_ids:
        # Define the URL with the current branch, store, and parent IDs
        url = f"https://api.express24.uz/client/v4/store/{store_id}/menu?branchId={branch_id}&parentId={parent_id}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()

            # Access the data you need
            isNested = data['isNested']
            sections = data['sections']

            # Iterate through sections and products
            for section in sections:
                section_id = section['id']
                section_name = section['name']
                products = section['products']
                for product in products:
                    product_id = product['id']
                    product_name = product['name']
                    product_price = product['price']['current']

                    # Append the data to the list
                    data_list.append({
                        'store_id': store_id,
                        'branch_id': branch_id,
                        'parent_id': parent_id,
                        'section_id': section_id,
                        'section_name': section_name,
                        'product_id': product_id,
                        'product_name': product_name,
                        'price': product_price
                    })

# Create a DataFrame from the data
df = pd.DataFrame(data_list)

# Export the DataFrame to an Excel file with the same name as JSON file
excel_file_name = 'menu_data_sub_menu.xlsx'
df.to_excel(excel_file_name, index=False)

print(f"Excel file '{excel_file_name}' has been saved.")
