from database.database import DB
import pandas as pd

def k12_spending_by_zipcode(city: str, state: str) -> pd.DataFrame:
    db = DB()
    df = db.get_k12_spending_data(city, state)
    df = df.rename(columns={'ppcstot': 'total_spending_per_pupil'})
    result_df = df[['zip_code', 'total_spending_per_pupil']]
    return result_df
    
def k12_spending_by_city() -> pd.DataFrame:
    db = DB()
    df = db.get_all_k12_spending_data()
    df = df.rename(columns={'ppcstot': 'total_spending_per_pupil'})
    df = df.astype({'city': str, 'state': str})
    df['location'] = df['city'] + ", " + df['state']
    result_df = df.groupby('location').total_spending_per_pupil.agg('mean').to_frame()\
        .reset_index().rename(columns={"total_spending_per_pupil": "mean_total_spending_per_pupil"})
    return result_df

def college_tuition_by_zipcode(city: str, state: str) -> pd.DataFrame:
    db = DB()
    df = db.get_college_tuition_data(city, state)
    df = df.rename(columns={"costt4_a":"avg_cost_of_attendance"})
    
    result_df = df.groupby('zip_code').avg_cost_of_attendance.agg('mean').to_frame().reset_index()
    return result_df

def college_tuition_by_city() -> pd.DataFrame:
    db = DB()
    df = db.get_all_college_tuition_data()
    df = df.rename(columns={"costt4_a": "avg_cost_of_attendance"})
    
    df = df.astype({'city': str, 'state': str})
    df['location'] = df['city'] + ", " + df['state']
    result_df = df.groupby('location').avg_cost_of_attendance.agg('mean').to_frame().reset_index()
    return result_df

