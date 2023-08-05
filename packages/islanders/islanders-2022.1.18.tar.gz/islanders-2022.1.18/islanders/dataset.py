import pandas as pd
def datasets(name = None):
    '''this medoul is dessigned to allow you to download datasets that where created from the islander community'''

    datasets = {}
    datasets["titanic"] = "https://raw.githubusercontent.com/Islanderrobotics/titanic/master/titanic.csv"
    datasets["titanic.csv"] = datasets["titanic"]
    datasets["amazon electronics"] = "https://raw.githubusercontent.com/Islanderrobotics/islander-datasets/master/amazon%20electronics.csv"
    datasets["amazon electronics.csv"] = datasets["amazon electronics"]
    datasets["cleaned rotten tomatoes"] = "https://raw.githubusercontent.com/Islanderrobotics/islander-datasets/master/cleaned%20rotten%20tomato.csv"
    datasets["cleaned rotten tomatoes.csv"] = datasets["cleaned rotten tomatoes"]
    datasets["uncleaned rotten tomatoes"] = "https://raw.githubusercontent.com/Islanderrobotics/islander-datasets/master/uncleaned_tomatos.csv"
    datasets["uncleaned rotten tomatoes.csv"] = datasets["uncleaned rotten tomatoes"]
    datasets["movie"] = "https://raw.githubusercontent.com/Islanderrobotics/islander-datasets/master/movie.csv"
    datasets["movie.csv"] = datasets["movie"]
    return pd.read_csv(datasets[name.lower()], index_col=0)