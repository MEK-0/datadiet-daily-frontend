
import pandas as pd
import json

def get_category_style(category):
    category = str(category).lower().strip()
    styles = {
        'ai': {'colorClass': 'text-blue-400 border-blue-400/30', 'type': 'ai'},
        'gaming': {'colorClass': 'text-purple-400 border-purple-400/30', 'type': 'gaming'},
        'mobile': {'colorClass': 'text-green-400 border-green-400/30', 'type': 'mobile'},
        'space': {'colorClass': 'text-yellow-400 border-yellow-400/30', 'type': 'space'},
        'gear': {'colorClass': 'text-red-400 border-red-400/30', 'type': 'gear'}
    }
    return styles.get(category, {'colorClass': 'text-gray-400 border-gray-400/30', 'type': 'general'})

def excel_to_json():
    try:
        # Read Excel file
        df = pd.read_excel('dataset.xlsx')
        
        # Take first 5 rows
        df = df.head(5)
        
        news_list = []
        
        for index, row in df.iterrows():
            # Use lowercase keys as found in the Excel file
            category = row.get('category', 'General')
            style = get_category_style(category)
            
            news_item = {
                "id": f"news-excel-{index + 1}",
                "tags": [
                    {
                        "text": str(category).upper(),
                        "colorClass": style['colorClass'],
                        "type": style['type']
                    }
                ],
                "content": {
                    "en": {
                        "title": str(row.get('title', '')),
                        "description": str(row.get('content', '')),
                        "hashtags": ["#news"]
                    },
                    "tr": {
                        "title": str(row.get('title', '')),
                        "description": str(row.get('content', '')),
                        "hashtags": ["#haber"]
                    }
                },
                "url": str(row.get('url', '#'))
            }
            news_list.append(news_item)
            
        # Write to JSON file
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
            
        print("Successfully converted dataset.xlsx to news.json")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    excel_to_json()
