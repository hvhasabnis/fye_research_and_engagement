"""
Google Drive File IDs
These are NOT sensitive - just pointers to files
"""

# Main folder ID (for access testing)
MAIN_FOLDER_ID = '1RQq8CeIV1GQEnp2SUzbDTjWA9XGAuiv1'  # Your THM_Survey_Data folder
RAW_FOLDER_ID    = '1Cykif6XmVtx96FCvKmnjBsjXOsA-xNVB'     # ← where your CSVs live
OUTPUT_FOLDER_ID = '1BidjiWkUOWtZBfq-3z1b9IzLpWmYvrG8'    # ← where results get saved
PREPROCESSED_DATA_FOLDER_ID = '1Ux3EyqnDRLDJPGOFEqnBi8ivW220Ye_w'   # ← where preprocessed data will be saved

# File IDs
GDRIVE_FILES = {
    # Cleaned data
    'text_prepared': '1OYdTNbBJNsD0_fHLyQ6sHMaFDICXvOPLdwyVYpCnOfE',
    'quant_prepared': '1WZh3Ohyy9TdS0vrGKOJQWk5RqzsQwbMIEeJwGQso8Vk',
    
    # Raw data
    'fall_2022': '1V7fwK2W1Dt1XcF0KyWqvSmlMad_pEmugBIr8Da8pln4',
    'spring_2023': '19lw4hp-0O9T1RQMygosnCHKgA8fFWusmWI8yODEWzOE',
    'fall_2023': '1ynkiX_rpCWkdl2nZv7YCgy5yQ-hkUncUvbfvPct_GRE',
    'spring_2024': '1JXy8AAkF6b8Zx8Gv2DHkbdpF7AC2QOljacHjMR6WkvY',
    'fall_2024': '1CHHuKJMnFOD4kn8Nh8HpqJr5CQ1mqzsL1TUzT5ypPjM',
    'spring_2025': '1rFBcv5nsiCup431EoWJ8H7Wp1ffgt-jOcxmr7_zniYo',
    'fall_2025': '1j_bmky3RUF2J9nkHnjaOkW8_IDYp6HLSCBZIfDFfvD4'
}

def validate_config():
    issues = []
    all_ids = {
        'MAIN_FOLDER_ID':   MAIN_FOLDER_ID,
        'RAW_FOLDER_ID':    RAW_FOLDER_ID,
        'OUTPUT_FOLDER_ID': OUTPUT_FOLDER_ID,
        **{f'GDRIVE_FILES[{k}]': v for k, v in GDRIVE_FILES.items()}
    }
    for name, val in all_ids.items():
        if val.startswith('REPLACE_WITH'):
            issues.append(f'  ⚠️  {name} is still a placeholder')

    if issues:
        print("CONFIG WARNINGS — Update config.py with real Drive IDs:")
        for i in issues:
            print(i)
        return False

    print("✅ All IDs in config.py are set.")
    return True