import pandas as pd


def main(frame_file: str = '..data/results-survey.csv'):
    frame = pd.read_csv(frame_file)
    cols = frame.columns.tolist()[121:132]
    frame = frame[cols]
    print(frame.columns)
    col_names = ['The test code is readable',
                 'The test code is maintainable',
                 'The test has correct input-output pairs',
                 'The test is able to find faults',
                 'The test is not flaky',
                 'The test has good code design',
                 'The test withstands in the long run',
                 'Parts of the unit test are reusable',
                 'The test code has low complexity',
                 'The test code has good mutation coverage',
                 'The test code has short execution time']
    frame = frame.rename(columns=dict(zip(cols, col_names)))
    frame = frame.apply(pd.value_counts).fillna(0).T
    reorder = ['I do not know', 'not at all important', 'slightly', 'moderately', 'very', 'extremely important']
    frame = frame[reorder]
    frame = frame.reset_index()
    frame.to_csv('..data/likert.csv', index=False)



if __name__ == '__main__':
    main()
