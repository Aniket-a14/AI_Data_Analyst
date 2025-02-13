BASIC_EXAMPLES = [
    # Viewing Data
    {
        "task": "show first 5 rows",
        "code": "df.head(5)"
    },
    {
        "task": "show first 10 rows",
        "code": "df.head(10)"
    },
    {
        "task": "display last 5 rows",
        "code": "df.tail(5)"
    },
    {
        "task": "show basic information",
        "code": "df.info()"
    },
    {
        "task": "show column names",
        "code": "df.columns"
    },
    {
        "task": "show data types of columns",
        "code": "df.dtypes"
    },
    {
        "task": "show shape of dataset",
        "code": "df.shape"
    },
    {
        "task": "show index of dataframe",
        "code": "df.index"
    },
    {
        "task": "check for missing values",
        "code": "df.isnull().sum()"
    },
    {
        "task": "show memory usage",
        "code": "df.memory_usage(deep=True)"
    },
    # Full Dataset Display
    {
        "task": "show the full dataset",
        "code": "df"
    },
    {
        "task": "display all rows without truncation",
        "code": "pd.set_option('display.max_rows', None)\ndf"
    },
    {
        "task": "show all columns without truncation",
        "code": "pd.set_option('display.max_columns', None)\ndf"
    },
    {
        "task": "display dataset as string",
        "code": "df.to_string()"
    },
    {
        "task": "reset index and show all data",
        "code": "df.reset_index(drop=True)"
    }
] 