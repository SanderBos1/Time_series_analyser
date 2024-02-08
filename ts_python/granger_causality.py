from statsmodels.tsa.stattools import grangercausalitytests


def granger_causality_calculation(df, column1, column2, lag, test):
    df = df[[column1, column2]]
    df = df.dropna()
    test_result  = grangercausalitytests(df, lag)
    p_values = []
    for i in range(lag):
        p_values.append([i+1, round(test_result[i+1][0][test][1], 4)])
    return p_values
        
 