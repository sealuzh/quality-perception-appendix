__author__ = "Giovanni Grano"
__email__ = "grano@ifi.uzh.ch"
__license__ = "MIT"

import pandas as pd
import numpy as np
import metrics


def process_survey(save: bool = True, dev_features: bool = True, drop_test: bool = False,
                   remove_not_applicable: bool=True) -> pd.DataFrame:
    """
    Process the raw results of the survey
    :param remove_not_applicable:
    :param drop_test:
    :param save: flag for saving the resulting frame to CSV file
    :param dev_features: true if you want to include the features about developers (education and experience)
    :return: a pandas DataFrame
    """
    # reading raw results of the survey
    res = pd.read_csv('../data/results-survey.csv')

    # reading the test classes of the study
    context = pd.read_csv('../data/context.csv')
    test_classes = context['test_name'].tolist()
    context = context.set_index('test_name')

    # index of the columns containing the scores
    cols = [32, 41, 50, 59, 68, 77, 86, 95, 104, 113]

    # discarding people that do not declare the education and the years of experience
    if dev_features:
        res = res[(res.iloc[:, 133].notna()) & (res.iloc[:, 140].notna())]
        res = res[res.iloc[:, 140].astype(int) < 50]
        res.rename(columns={res.columns[133]: 'education',
                            res.columns[140]: 'experience'}, inplace=True)

    temp_frames = []
    # iterate over each pair of scores and test class
    for col, cls in zip(cols, test_classes):
        tmp = res[res.iloc[:, col].notna()]
        if dev_features:
            tmp = tmp.iloc[:, [col, 133, 140]]
        else:
            tmp = tmp.iloc[:, [col]]
        tmp.rename(columns={tmp.columns[0]: "score"}, inplace=True)
        if remove_not_applicable:
            tmp = tmp[tmp['score'] != 'not applicable']
        tmp['test_name'] = cls
        temp_frames.append(tmp)

    overall_scores = pd.concat(temp_frames)
    overall_scores = merge(overall_scores, drop_name=drop_test)
    if save:
        overall_scores.to_csv('../data/survey_processed.csv', index=False)
    return overall_scores


def merge(survey: pd.DataFrame, metrics_file: str = '../data/metrics.csv', drop_name: bool = True):
    """
    Cleans the frame with the metrics and merge it with the scores, line coverage and mutation score
    :param drop_name:
    :param survey: the pandas DataFrame containing the results of the survey
    :param metrics_file: the raw frame of the metrics
    :return: the resulting merged pandas DataFrame
    """
    m_frame = pd.read_csv(metrics_file)
    features = metrics.metrics
    m_frame = m_frame.set_index('test_name')
    m_frame = m_frame[features]
    m_frame = m_frame.fillna(0)
    m_frame = m_frame[[col for col in m_frame if not m_frame[col].nunique() == 1]]
    m_frame = m_frame.reset_index()
    m_frame = m_frame.merge(survey, on=['test_name'])
    m_frame['score'] = m_frame['score'].transform(lambda x: transform_frame(x))
    if drop_name:
        m_frame.drop(columns='test_name')
    return m_frame


def transform_frame(val: str):
    """
    Transforms a rating into numerical representation
    """
    if val == 'very poor':
        return 1
    if val == 'poor':
        return 2
    if val == 'fair':
        return 3
    if val == 'good':
        return 4
    if val == 'very good':
        return 5
    else:
        return -1


def ordinal_logit_problem(filename='../frames/ordinal_logit'):
    frame: pd.DataFrame = process_survey(save=False, dev_features=True)
    frame = frame[metrics.metrics + ['experience', 'score']]
    frame.to_csv('{}.csv'.format(filename), index=False)


def main():
    ordinal_logit_problem()


if __name__ == '__main__':
    main()
