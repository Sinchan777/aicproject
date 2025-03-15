import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

st.markdown("""
<style>
    :root {
        --primary: #2E86AB;
        --background: #0F0F0F;
        --surface: #1A1A1A;
        --text: #FFFFFF;
        --border: #2E86AB55;
    }

    .main {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stTimeInput div[data-baseweb="input"] {
        background-color: var(--surface) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
    }
    
    .stTimeInput input {
        color: var(--text) !important;
    }
    
    .stButton>button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 8px;
        padding: 12px 28px;
        transition: transform 0.2s ease;
        border: none;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
    }
    
    .dataframe {
        background-color: var(--surface) !important;
        color: var(--text) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
    }
    
    .metric-box {
        background: var(--surface);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border);
    }
    
    .metric-box h2 {
        color: var(--primary) !important;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def load_model(model_path):
    return joblib.load(model_path)

def predict_proba(model, doctors_df, input_hour):
    features_df = doctors_df.copy()
    features_df['Hour'] = input_hour
    X = features_df[['Speciality', 'Region', 'Usage Time (mins)', 
                   'Count of Survey Attempts', 'Hour']]
    proba = model.predict_proba(X)[:, 1]
    features_df['Probability'] = proba
    return features_df[['NPI', 'Probability', 'Speciality', 'Region']]\
           .sort_values('Probability', ascending=False)

def main():
    if 'selected_time' not in st.session_state:
        st.session_state.selected_time = datetime.now().time()
    
    st.markdown('<div style="font-size:2.5rem; font-weight:600; color: var(--primary); margin-bottom:30px;">Doctor Connect</div>', 
               unsafe_allow_html=True)
   
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            new_time = st.time_input(
                'Select Target Time', 
                value=st.session_state.selected_time,
                key='time_input'
            )
            st.session_state.selected_time = new_time
            
        with col2:
            st.markdown("<div style='height: 28px'></div>", 
                      unsafe_allow_html=True)
            analyze_btn = st.button("Get recommendations")
        
        if analyze_btn:
            doctors_df = pd.read_csv('data/doctors.csv')
            model = load_model('models/model.pkl')
            input_hour = st.session_state.selected_time.hour
            
            with st.spinner('Analyzing engagement patterns...'):
                result_df = predict_proba(model, doctors_df, input_hour)
                result_df['Probability'] = result_df['Probability'].round(3)
                
                st.markdown("---")
                cols = st.columns(3)
                with cols[0]:
                    st.markdown("""
                    <div class="metric-box">
                        Total Physicians<br>
                        <h2>{}</h2>
                    </div>
                    """.format(len(doctors_df)), unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown("""
                    <div class="metric-box">
                        Recommended<br>
                        <h2>{}</h2>
                    </div>
                    """.format(len(result_df[result_df['Probability'] > 0.5])), 
                    unsafe_allow_html=True)
                
                with cols[2]:
                    st.markdown("""
                    <div class="metric-box">
                        Top Probability<br>
                        <h2>{:.1%}</h2>
                    </div>
                    """.format(result_df['Probability'].max()), 
                    unsafe_allow_html=True)
                
                st.dataframe(
                    result_df.style.format({'Probability': '{:.1%}'}),
                    height=600,
                    use_container_width=True
                )
                
                # Download Section
                st.markdown("---")
                csv = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Report",
                    data=csv,
                    file_name=f'availability_{st.session_state.selected_time.strftime("%H%M")}.csv',
                    mime='text/csv',
                )

if __name__ == '__main__':
    main()