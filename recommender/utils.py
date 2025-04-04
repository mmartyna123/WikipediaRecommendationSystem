def saveDatabase(df, fileName):
    df.to_csv(fileName, index=False)
    return None

