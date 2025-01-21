def transform_data(text_data: str, stt: int):
    data = text_data.split("\n")
    while '·' in data:
        data.remove('·')

    if len(data) < 7:
        return None
    
    extracted_info = data[1:7]

    if 'tỷ' in extracted_info[0]:
        extracted_info[0] = float(extracted_info[0].replace('tỷ', '').replace(',', '.').strip())
    elif 'triệu' in extracted_info[0]:
        extracted_info[0] = float(extracted_info[0].replace('triệu', '').replace(',', '.').strip()) / 1000
    else:
        return None
    
    extracted_info[1] = float(extracted_info[1].replace('m²', '').replace(',', '.').strip())
    extracted_info[2] = float(extracted_info[2].replace('tr/m²', '').replace(',', '.').strip())

    if not extracted_info[3].isdigit() or not extracted_info[4].isdigit():
        return None
    
    if 'Hồ Chí Minh' not in extracted_info[5]:
        return None
    extracted_info[5] = extracted_info[5].replace(', Hồ Chí Minh', '').strip()
    extracted_info.insert(0, 'RS' + '0' * (5 - len(str(stt))) + str(stt))
    return extracted_info