import pandas as pd
import numpy as np
import json

# ==========================================
# 1. SETUP DUMMY DATA (Simulating the CSV)
# ==========================================
# In a real scenario, you would use: df = pd.read_csv('market_data.csv')
data = {
    'Crop': ['Onion', 'Onion', 'Onion', 'Onion', 'Onion', 'Tomato'],
    'Source': ['Gov_Mandi', 'Trader_A', 'Farmer_Report', 'Random_User', 'Gov_Database', 'Gov_Mandi'],
    'Price': [1450, 1420, 1400, 3500, 1440, 800],  # Note the '3500' outlier
    'Trust_Score': [1.0, 0.8, 0.5, 0.1, 1.0, 1.0]   # Gov sources have high trust, random users low
}

df = pd.DataFrame(data)
def get_trusted_price(crop_name):
    # Filter data for the specific crop
    crop_df = df[df['Crop'] == crop_name].copy()
    
    if crop_df.empty:
        return json.dumps({"error": "Crop not found"})

#     # ==========================================
#     # 2. MUTATION A: Z-SCORE OUTLIER DETECTION
#     # ==========================================
    # Calculate Mean and Standard Deviation
    mean_price = crop_df['Price'].mean()
    std_dev = crop_df['Price'].std()

#     # If we have enough data points, apply Z-Score filter
    if std_dev > 0 and len(crop_df) > 1:
        # Calculate Z-Score: (Price - Mean) / StdDev
        crop_df['z_score'] = (crop_df['Price'] - mean_price) / std_dev
        
        # Filter: Keep only prices within 2 Standard Deviations (-2 < Z < 2)
        # This removes the "3500" outlier
        clean_df = crop_df[np.abs(crop_df['z_score']) < 2]
    else:
        clean_df = crop_df

#     # ==========================================
#     # 3. CALCULATE WEIGHTED AVERAGE
#     # ==========================================
#     # Formula: Sum(Price * Trust) / Sum(Trust)
    weighted_sum = (clean_df['Price'] * clean_df['Trust_Score']).sum()
    total_trust = clean_df['Trust_Score'].sum()

    if total_trust == 0:
        trusted_avg = clean_df['Price'].mean()
    else:
        trusted_avg = weighted_sum / total_trust

    # Define the "Trusted Range" based on the CLEAN data
    # (e.g., slightly below and above the weighted average, or the min/max of clean data)
    low_bound = int(clean_df['Price'].min())
    high_bound = int(clean_df['Price'].max())

#     # ==========================================
#     # 4. JSON OUTPUT
#     # ==========================================
    result ={

        "crop": crop_name,
        "trusted_price_avg": int(trusted_avg),
        "trusted_range": f"{low_bound}-{high_bound}",
        "data_points_used": len(clean_df),
        "outliers_removed": len(crop_df) - len(clean_df)
    }
 

    return json.dumps(result, indent=4)

# # ==========================================
# # EXECUTION
# # ==========================================
if __name__ == "__main__":
    # Test with 'Onion' to see outlier removal in action
    # x=str(input("enter crop name"))
    print(get_trusted_price("onion"))