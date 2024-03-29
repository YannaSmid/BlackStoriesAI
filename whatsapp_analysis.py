import pandas as pd
import os

def do_analysis():
    # get the right file, name it \\pp_[number]_bs_[number]
    path = os.getcwd()
    file_path_test = path + f"\\pp_{pp_number}_bs_{bs_number}.txt"
    df2 = pd.read_csv(file_path_test, sep=": ", names=['date', 'text'], engine='python')

    # get the file for adding the results for the analysis
    file_path_analysis = path + "\\NHC_analysis.xlsx"
    df = pd.read_excel(file_path_analysis, sep=",")

    # split into right columns and add column
    df2[['date', 'name']] = df2.iloc[:,0].str.split('- ', expand=True)
    df2['name+text'] = df2['name'] + ': ' + df2['text']

    # get names of the ones in the chat
    names = df2['name'].unique()
    experimenter_name = names[0]
    participant_name = names[1]

    # make seperate dfs of the questions from the participant & answers of the experimenter
    participant_df = df2[df2['name'].str.contains(participant_name, na=False)]
    experimenter_df = df2[df2['name'].str.contains(experimenter_name, na=False)]

    # calculate amount of questions & make two list of questions asked & whole chat history
    nr_questions = len(participant_df)
    questions_asked = list(participant_df['text'])
    chat_history = list(df2['name+text'])

    # calculate how many yes, no and make list of other answers given by experimenter (also to see hints given)
    nr_yes = experimenter_df['text'].str.contains('yes', case=False).sum()
    nr_no = experimenter_df['text'].str.contains('no', case=False).sum()
    other_answers = experimenter_df[~experimenter_df['text'].isin(['yes', 'no', 'Yes', 'No'])]
    other = list(other_answers['text'])

    # make new row for data analysis
    new_row = {"Medium": pp_number, "Group member": experimenter_name, "Blackstory": bs_number,
               "Questions": nr_questions,
               "Hints": 'tbd', "Score": 'tbd', "Age": age, "Chat history": chat_history,
               "Questions asked": questions_asked, "Yes": nr_yes, "No": nr_no, "Other": other}
    df.loc[len(df)] = new_row
    df.to_excel(path + f'\\NHC_analysis.xlsx', index=False)


if __name__ == "__main__":
    # variables for dataframe
    bs_number = int(input("Blackstory number: "))
    pp_number = int(input("Participant number: "))
    age = int(input("age participant: "))

    do_analysis()