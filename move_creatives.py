import os
import shutil
import pandas as pd
from transliterate import translit

# Название полей таблицы с брендами и тп
field_name_advertisers = 'Advertisers list'
field_name_brands = 'Brands list'
field_name_advertisers_sub_brand = 'Subbrands list'

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
                # Переменная brand с замененными пробелами на подчеркивание
                alt_brand = brand.strip().lower().replace(' ', '_').replace("'", '')
                # Без замены пробелов
                brand = brand.strip().lower().replace("'", '')
                # Перевод транслитом
                translit_creative = translit(creative.lower(), language_code='ru', reversed=True)
                if brand in creative.lower() or alt_brand in creative.lower() or brand in translit_creative or alt_brand in translit_creative:
                    if advertiser not in os.listdir(rf'{os.path.dirname(path_to_dir)}/result'):
                        os.makedirs(rf'{os.path.dirname(path_to_dir)}/result/{advertiser}')
                    shutil.move(rf"{path_to_dir}/{creative}", fr'{os.path.dirname(path_to_dir)}/result/{advertiser}')
                    move = True
                    break
            if move:
                break
