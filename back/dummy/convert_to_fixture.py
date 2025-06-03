import json

# 파일명과 모델명을 매핑
input_files = [
    ('books_final_utf8bom.json', 'books.book'),
    ('customcategory_final_utf8bom.json', 'books.customcategory'),
]

for file_name, model_name in input_files:
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        original_data = json.load(f)

    fixture_data = []
    for obj in original_data:
        fixture_data.append({
            "model": model_name,
            "pk": obj.pop("id"),
            "fields": obj
        })

    output_name = file_name.replace('.json', '_fixture.json')
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, ensure_ascii=False, indent=2)

    print(f"{output_name} 생성 완료")
