import pandas as pd

def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df['Login Time'] = pd.to_datetime(df['Login Time'])
    df['Logout Time'] = pd.to_datetime(df['Logout Time'])
    
    samples = []
    for _, row in df.iterrows():
        npi = row['NPI']
        specialty = row['Speciality']
        region = row['Region']
        usage_time = row['Usage Time (mins)']
        attempts = row['Count of Survey Attempts']
        login = row['Login Time']
        logout = row['Logout Time']
        
        active_hours = set()
        current = login
        while current <= logout:
            active_hours.add(current.hour)
            current += pd.Timedelta(hours=1)
        
        for hour in range(24):
            target = 1 if hour in active_hours else 0
            samples.append({
                'NPI': npi,
                'Speciality': specialty,
                'Region': region,
                'Usage Time (mins)': usage_time,
                'Count of Survey Attempts': attempts,
                'Hour': hour,
                'Target': target
            })
    
    samples_df = pd.DataFrame(samples)
    samples_df.to_csv(output_path, index=False)
    return samples_df

if __name__ == "__main__":
<<<<<<< HEAD
    preprocess_data('data/doctors.csv','data/processed.csv')
=======
    preprocess_data('data/doctors.csv','data/processed.csv')
>>>>>>> e377d25 (fin.)
