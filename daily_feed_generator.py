
import pandas as pd
import json
import os
import random

STATE_FILE = 'feed_state.json'
OUTPUT_FILE = 'news.json'
EXCEL_FILE = 'dataset.xlsx'

# Starting indices as requested
# Note: Excel is 1-indexed for rows, but pandas is 0-indexed.
# If user says 1-401, in pandas it's row 0 to 400.
# User Logic:
# 1-401 ai -> 0 index start
# 402-718 gaming -> 401 index start
# 719-1114 mobile -> 718 index start
# 1115-1472 space -> 1114 index start
# 1473-1772 Gear -> 1472 index start

INITIAL_STATE = {
    'ai': 0,
    'gaming': 401,
    'mobile': 718,
    'space': 1114,
    'gear': 1472
}

STYLES = {
    'ai': {'colorClass': 'text-blue-400 border-blue-400/30', 'type': 'ai'},
    'gaming': {'colorClass': 'text-purple-400 border-purple-400/30', 'type': 'gaming'},
    'mobile': {'colorClass': 'text-green-400 border-green-400/30', 'type': 'mobile'},
    'space': {'colorClass': 'text-yellow-400 border-yellow-400/30', 'type': 'space'},
    'gear': {'colorClass': 'text-red-400 border-red-400/30', 'type': 'gear'}
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return INITIAL_STATE.copy()

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def get_category_style(category_name):
    cat_lower = str(category_name).lower().strip()
    return STYLES.get(cat_lower, {'colorClass': 'text-gray-400 border-gray-400/30', 'type': 'general'})

def generate_daily_feed():
    try:
        # Load Data
        df = pd.read_excel(EXCEL_FILE)
        # Ensure column names are stripped of whitespace and lowercased for consistent access
        df.columns = df.columns.str.strip().str.lower()
        
        state = load_state()
        daily_items = []
        
        categories_map = {
            'ai': 'AI',
            'gaming': 'Gaming',
            'mobile': 'Mobile',
            'space': 'Space',
            'gear': 'Gear'
        }
        
        # Process each category
        for cat_key, cat_display in categories_map.items():
            start_idx = state[cat_key]
            
            # Select 4 items
            # We assume the excel is sorted or we just grab by row index directly from the big dataframe
            # But the user gave ranges which implies the data is likely grouped or we should just trust the indices.
            # Let's slice the dataframe based on the index.
            
            # Check bounds
            if start_idx + 4 > len(df):
                print(f"Warning: End of list reached for {cat_key}, resetting to initial.")
                start_idx = INITIAL_STATE[cat_key]
            
            # Get 4 rows
            # We are assuming the dataset is just one big list and we pick rows by index.
            # However, the user gave specific ranges for categories: 1-401 for AI.
            # If we just pick row 401, is it guaranteed to be Gaming?
            # User's prompt implies the dataset is structured this way. 
            # So we will just use iloc.
            
            subset = df.iloc[start_idx : start_idx + 4]
            
            for _, row in subset.iterrows():
                # Force category style based on the section we are pulling from, to be safe
                # Or rely on the 'category' column in Excel. 
                # Let's rely on our hardcoded style for this key since the ranges are fixed categories.
                style = STYLES[cat_key]
                
                item = {
                    "id": f"news-{cat_key}-{start_idx}", # Unique ID
                    "time": "Today", # Fix for undefined time
                    "tags": [
                        {
                            "text": cat_display,
                            "colorClass": style['colorClass'],
                            "type": style['type']
                        }
                    ],
                    "content": {
                        "en": {
                            "title": str(row.get('title', 'No Title')),
                            "description": str(row.get('content', 'No Content')),
                            "hashtags": ["#news", f"#{cat_key}"]
                        },
                        "tr": { # Simple fallback for TR
                            "title": str(row.get('title', 'Başlık Yok')),
                            "description": str(row.get('content', 'İçerik Yok')),
                            "hashtags": ["#haber", f"#{cat_key}"]
                        }
                    },
                    "url": str(row.get('url', '#'))
                }
                daily_items.append(item)
                
            # Update state
            state[cat_key] = start_idx + 4
            
        # Shuffle result
        random.shuffle(daily_items)
        
        # Save JSON
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(daily_items, f, ensure_ascii=False, indent=4)
            
        # Save State
        save_state(state)
        
        print(f"Generated {len(daily_items)} items for the daily feed.")
        print("Updated indices:", state)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_daily_feed()
