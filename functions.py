def countMessages(df, group, date_col, period="day"):
    """
    Returns dataframe with message count within
    given time period.

    Parameters
    ----------
    df : pd.dataframe
        pandas dataframe with 'date_col'.
    group : string
        Category to group message count by.
    date_col : string
        Timestamp column name within df.
    period : {'day', 'month', 'year'}, optional
        group count by this time period, by default 'day'.

    Returns
    -------
    pd.dataframe
        dataframe with value counts against period
    """
    df_dt = df.copy()
    if period.lower() == "day":
        df_dt[date_col] = df_dt[date_col].dt.to_period("D")
    elif period.lower() == "month":
        df_dt[date_col] = df_dt[date_col].dt.to_period("M")
    elif period.lower() == "year":
        df_dt[date_col] = df_dt[date_col].dt.to_period("Y")

    df_dt = df_dt.groupby([group, date_col]).size().reset_index(name="counts")
    df_dt[date_col] = df_dt[date_col].astype(dtype=str)
    return df_dt
