import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    #locations of parking tickets with $1,000 r more total aggregted violation amounts
    totalamount_df = violations_df.pivot_table(index='location', values='amount', aggfunc='sum').sort_values(by='amount', ascending=False)
    totalamount_df['location'] = totalamount_df.index
    totalamount_df.reset_index(drop=True, inplace=True)
    return totalamount_df[totalamount_df['amount'] >= threshold]

def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_map = top_locations(violations_df, threshold)
    location_map = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset=['location'])
    merged_df = pd.merge(top_map, location_map, on='location')
    return merged_df


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000)  -> pd.DataFrame:
    top_locations_df = top_locations(violations_df)
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