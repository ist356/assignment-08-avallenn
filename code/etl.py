import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    #locations of parking tickets with $1,000 r more total aggregted violation amounts
    totalamount_df = violations_df.pivot_table(index='location', values='amount', aggfunc='sum').sort_values(by='amount', ascending=False)
    top_df = totalamount_df[totalamount_df['amount'] >= threshold]
    top_df = top_df.sort_values(by='amount', ascending=False)
    top_df['location'] = top_df.index
    top_df = top_df.reset_index(drop=True)
    return top_df

def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_df = top_locations(violations_df, threshold)
    combined = pd.merge(top_df, violations_df, left_on='location', 
                        right_on='location')
    top_loc_df = combined[['location', 'amount_x', 'lat', 'lon']]
    top_loc_dedupe_df = top_loc_df.drop_duplicates(subset='location')
    top_loc_dedupe_df = top_loc_dedupe_df.rename(columns={'amount_x': 'amount'})
    return top_loc_dedupe_df


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000)  -> pd.DataFrame:
    top_locations_df = top_locations(violations_df, threshold)
    del top_locations_df['amount']
    merged_df = pd.merge(top_locations_df[['location']], violations_df, on='location')
    return merged_df

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    
    top_locations_df = top_locations(violations_df)
    top_locations_df.to_csv('./cache/top_locations.csv', index=False)

    top_map = top_locations_mappable(violations_df)
    top_map.to_csv('./cache/top_locations_mappable.csv', index=False)

    top_tickets = tickets_in_top_locations(violations_df, top_locations_df)
    top_tickets.to_csv('./cache/tickets_in_top_locations.csv', index=False)