import os
import shutil
import pandas as pd

# Название полей таблицы с брендами и тп
field_name_advertisers = 'ADVERTISERS LIST'
field_name_brands = 'BRANDS'
field_name_advertisers_sub_brand = 'SUBBRANDS'


def main(path_to_dir, excel_path):
    df = pd.read_excel(excel_path)
    # Создаем папку по результаты
    if not os.path.exists(rf'{os.path.dirname(path_to_dir)}/result'):
        os.makedirs(rf'{os.path.dirname(path_to_dir)}/result')
    # Раскидываем креативы по папкам
    for creative in os.listdir(path_to_dir):
        move = False
        for index, row in df.iterrows():
            advertiser = str(row[field_name_advertisers])
            brands = str(row[field_name_brands]).split(';')
            sub_brands = str(row[field_name_advertisers_sub_brand]).split(';')
            brands += sub_brands
            for brand in brands:
                if (brand.strip().lower() in creative.lower() or
                        brand.strip().lower().replace(' ', '_') in creative.lower()):
                    if advertiser not in os.listdir(rf'{os.path.dirname(path_to_dir)}/result'):
                        os.makedirs(rf'{os.path.dirname(path_to_dir)}/result/{advertiser}')
                    shutil.move(rf"{path_to_dir}/{creative}", fr'{os.path.dirname(path_to_dir)}/result/{advertiser}')
                    move = True
                    break
            if move:
                break
