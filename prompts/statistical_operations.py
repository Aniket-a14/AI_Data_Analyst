STATISTICAL_EXAMPLES = [
    # Basic Statistics
    {
        "task": "calculate mean of tip column",
        "code": "df['tip'].mean()"
    },
    {
        "task": "find median total bill",
        "code": "df['total_bill'].median()"
    },
    {
        "task": "calculate variance of tips",
        "code": "df['tip'].var()"
    },
    {
        "task": "show quartiles of total bill",
        "code": "df['total_bill'].quantile([0.25, 0.5, 0.75])"
    },
    
    # Advanced Statistics
    {
        "task": "calculate skewness of tips",
        "code": "df['tip'].skew()"
    },
    {
        "task": "find kurtosis of total bills",
        "code": "df['total_bill'].kurtosis()"
    },
    {
        "task": "calculate covariance of bill and tip",
        "code": "df[['total_bill', 'tip']].cov()"
    },
    
    # Aggregations
    {
        "task": "show all statistics for tip column",
        "code": "df['tip'].agg(['mean', 'median', 'std', 'var', 'min', 'max'])"
    },
    {
        "task": "calculate rolling average of tips",
        "code": "df['tip'].rolling(window=3).mean()"
    },
    {
        "task": "find cumulative sum of bills",
        "code": "df['total_bill'].cumsum()"
    },
    
    # Group Statistics
    {
        "task": "show statistics by day",
        "code": "df.groupby('day')['tip'].describe()"
    },
    {
        "task": "calculate z-scores of tips",
        "code": "(df['tip'] - df['tip'].mean()) / df['tip'].std()"
    }
] 