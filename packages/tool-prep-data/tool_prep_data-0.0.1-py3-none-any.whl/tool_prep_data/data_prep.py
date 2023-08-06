import pandas as pd

def replace_drop_reset_index(data, column_to_drop, axis=0):
    """Drops one column

        Parameters
        ----------
        data : DataFrame
            A dataframe with at least a conversions column
        column_to_drop : str
            Column you would like to drop

        Returns
        -------
        DataFrame
            A Dataframe with a boolean column i.e True/False

        """

    data = data.drop(column_to_drop, axis=axis)
    data = data.reset_index()
    data = data.drop(['index'], axis=1)

    return data

def lowercase_drop_spaces(data):
    """Removes spaces and changes column headers to lowercase

            Parameters
            ----------
            data : DataFrame
                A dataframe with at least a conversions column
            Returns
            -------
            DataFrame
                A Dataframe with a Did Convert column
            """
    data.columns = data.columns.str.lower().str.replace(' ', "_").str.replace('-', "_")
    return data

def scale_data(data, scaler_name):
    """Removes spaces and changes column headers to lowercase
        Parameters
        ----------
        data : DataFrame
            A dataframe with at least a conversions column
        scaler_name : str
            One of: minmax, standard, maxabs, robust, qts, pts-yj, pts-bc
        Returns
        -------
        DataFrame
            A Dataframe with a Did Convert column
        """
    if scaler_name == 'minmax':
        from sklearn.preprocessing import MinMaxScaler

        scaler = MinMaxScaler()
        print("Applying Min-Max Scaler")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'standard':
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        print("Applying Standard Scaler")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'maxabs':
        from sklearn.preprocessing import MaxAbsScaler

        scaler = MaxAbsScaler()
        print("Applying MaxAbs Scaler")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'robust':
        from sklearn.preprocessing import RobustScaler

        scaler = RobustScaler()
        print("Applying Robust Scaler")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'qts':
        from sklearn.preprocessing import QuantileTransformer

        scaler = QuantileTransformer()
        print("Applying QuantileTransformer Scaler")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'pts-yj':
        from sklearn.preprocessing import PowerTransformer

        scaler = PowerTransformer(method='yeo-johnson')
        print("Applying PowerTransformer Scaler (Yeo-Johnson)")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    elif scaler_name == 'pts-bc':
        from sklearn.preprocessing import PowerTransformer

        scaler = PowerTransformer(method='box-cox')
        print("Applying PowerTransformer Scaler (Box-Cox)")
        scaled_data = pd.DataFrame(scaler.fit_transform(data))
        scaled_data.columns = data.columns.values
        scaled_data.index = data.index.values

    # elif scaler_name == 'help':
    #     scaled_data = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTsa3ZmWJP4POGMNarr \
    #                                 -Rtk0vc1W5H8joMOBZzx6bROAX9-RJKS_xsKKJ99KT28KTqg-J4753conA4r/pub? \
    #                                 gid=0&single=true&output=csv')
    #     print("Generating Help")

    return scaled_data

def transform_fit_objects(data, encoder, unique_vals):
    """Transforms categorical(object) columns into numerical values
        Parameters
        ----------
        data : DataFrame
            A dataframe with at least a conversions column
        encoder : string
            One of label-encoder, one-hot-encoder
        unique_vals : int
            The amount of unique values present in a column to be considered categorical

        Returns
        -------
        DataFrame
            A Dataframe with a numerical values only.
        """
    object_columns = data.columns[data.dtypes == "object"]
    cat_columns = [each_column for each_column in object_columns if data[each_column].nunique() <= unique_vals]

    if encoder == "label-encoder":
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        for col in cat_columns:
            le.fit(data[col])
            data[col] = le.transform(data[col])

    if encoder == "onehot-encoder":
        df_dummies = pd.get_dummies(data[cat_columns])
        data_dummies = pd.concat([data, df_dummies], axis=1)
        data = data_dummies.drop(cat_columns, axis=1)
    return data