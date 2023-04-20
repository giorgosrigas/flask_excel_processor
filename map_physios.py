import pandas as pd

class change_excel:   
    def __init__(self, excel_file):
        df1 = pd.read_excel(excel_file, sheet_name='IASurveys')
        self.df1_copy = df1.copy()
        self.df1 = self.df1_copy[[ 'Information_Received','Assessment_provided','Advice_provided', 'Service_provided_by_Ascenti', 'Virtual_appt_satisfaction', 'IA F2F']]

        df2 = pd.read_excel(excel_file, sheet_name='DCSurveys')
        self.df2_copy = df2.copy()
        self.df2 = df2[['Effectiveness_Treatment', 'Satisfaction_professional','Effort_of_understanding', 'Effort_of_listening', 'Effort_of_choosing', 'RecommendClinicFriendsFamily', 'Overall_Satisfaction','F2F lookup 2']]
        
    def map_values(self,df):
        # Replace satisfaction categories with simplified labels
        df.replace({'1 - Very satisfied': 'S',
                '2 - Satisfied': 'S',
                '1 - Every effort was made ':'S',
                '2 - A lot of effort was made':'S',
                '1 - Extremely likely':'S',
                '2 - Likely':'S',
                '3 - Neither satisfied nor dissatisfied': 'N',
                '3 - Some effort was made': 'N',
                '3 - Neither likely or unlikely':'N',
                '6 - Don’t know':'N',     
                '4 - Dissatisfied': 'D',
                '5 - Very dissatisfied': 'D',
                '4 - A little effort was made':'D',
                '5 - No effort was made':'D',
                '4 - Unlikely': 'D',
                '5 - Extremely unlikely':'D'
               }, inplace=True)
        return df
        

   
    def concat_comments(self):
    #helper function for concatenating feedback with file code
        def concatenate_feedback(file_code, feedback):
            return f'{file_code} - {feedback}' if isinstance(feedback, str) else ''

        feedback_1 = self.df1_copy[['File code', 'GeneralFeedback','IA F2F']]
        feedback_2 = self.df2_copy[['File code', 'GeneralFeedback','F2F lookup 2']]
        feedback_2 = feedback_2.rename(columns = {'F2F lookup 2':'IA F2F'})
        feedback_2
        all_comments = pd.concat([feedback_1,feedback_2], axis = 0)
         #apply function on the  relevant columns
        all_comments['feedback_and_file_code'] = all_comments.apply(lambda row: concatenate_feedback(row['File code'], row['GeneralFeedback']), axis=1)
        #include all comments separated by commas  grouped by physio name
        feedback_data = all_comments.groupby('IA F2F')['feedback_and_file_code'].apply(lambda x: ', '.join(filter(None, x)))
        # reindex dataframe 
        feedback_data = feedback_data.to_frame().reset_index()
        feedback_data.columns = ['Physio', 'feedback (file code)'] 
        return feedback_data 
    
    def change_physio_otputs(self):
        #Create a function to count the occurrences of S, N, and D in a list.
        
        df1 = self.map_values(self.df1)
        df2 = self.map_values(self.df2)
        
        def count_s_n_d(lst):
            s_count = lst.count('S')
            n_count = lst.count('N')
            d_count = lst.count('D')
            return f'{s_count}/{n_count}/{d_count}'

        # Group by the last column (name column)
        grouped_data1 = df1.groupby(df1.columns[-1])
        grouped_data2 = df2.groupby(df2.columns[-1])


        # Initialize an empty DataFrame to store the output
        output_data1 = pd.DataFrame()
        output_data2 = pd.DataFrame()

        # Define output_data1 DataFrame with appropriate column names
        output_data1 = pd.DataFrame(columns=[
            'Physio', 'Information Received - S/N/D', 'Assessment Provided - S/N/D', 
            'Advice Provided - S/N/D', 'Service Provided by Ascenti - S/N/D', 
            'Virtual Appointment Satisfaction - S/N/D'
        ])
        # Define a custom aggregation function
        def custom_agg(group):
            return pd.Series({
                'Information Received - S/N/D': count_s_n_d(group['Information_Received'].tolist()),
                'Assessment Provided - S/N/D': count_s_n_d(group['Assessment_provided'].tolist()),
                'Advice Provided - S/N/D': count_s_n_d(group['Advice_provided'].tolist()),
                'Service Provided by Ascenti - S/N/D': count_s_n_d(group['Service_provided_by_Ascenti'].tolist()),
                'Virtual Appointment Satisfaction - S/N/D': count_s_n_d(group['Virtual_appt_satisfaction'].tolist()),
            })

        # Apply the custom_agg function to the grouped data
        output_data1 = grouped_data1.apply(custom_agg)

        # Reset the index and rename the index column to 'Physio'
        output_data1.reset_index(inplace=True)
        
         # Define a custom aggregation function
        def custom_agg2(group):
            return pd.Series({
                'Effectiveness of Treatment - S/N/D': count_s_n_d(group['Effectiveness_Treatment'].tolist()),
                'Professional Satisfaction - S/N/D': count_s_n_d(group['Satisfaction_professional'].tolist()),
                'Effort of Understanding - S/N/D': count_s_n_d(group['Effort_of_understanding'].tolist()),
                'Effort of Listening - S/N/D': count_s_n_d(group['Effort_of_listening'].tolist()),
                'Effort of Choosing - S/N/D': count_s_n_d(group['Effort_of_choosing'].tolist()),
                'ARecommend Clinic to Friends & Family - L/N/U ': count_s_n_d(group['RecommendClinicFriendsFamily'].tolist()),
                'Overall Satisfaction - S/N/D': count_s_n_d(group['Overall_Satisfaction'].tolist()),
            })

        # Apply the custom_agg function to the grouped data
        output_data2 = grouped_data2.apply(custom_agg2)

        # Reset the index and rename the index column to 'Physio'
        output_data2.reset_index(inplace=True)
        output_data1 = output_data1.rename(columns = {'IA F2F':'Physio'})
        output_data2= output_data2.rename(columns = {'F2F lookup 2':'Physio'})
        IA_DC = output_data1.merge(output_data2, on='Physio', how = 'left')
        
        comments = self.concat_comments()
        IA_DC = IA_DC.merge(comments, on='Physio')
        return  IA_DC
    
if __name__ == '__main__':
    giannis_app = change_excel('Survey data for therapists Mar 2023 - 16.04.xlsx').change_physio_otputs()
    print(giannis_app)
    