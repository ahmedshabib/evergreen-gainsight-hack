"""
Generate a tsv submission file to kaggle's 'Sentiment Analysis on Movie Reviews' (samr)
competition using the samr module with a given json configuration file.
"""



def fix_json_dict(config):
    new = {}
    for key, value in config.items():
        if isinstance(value, dict):
            value = fix_json_dict(value)
        elif isinstance(value, str):
            if value == "true":
                value = True
            elif value == "false":
                value = False
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
        new[key] = value
    return new



if __name__ == "__main__":
    # print("hello")
    import argparse
    import json
    import csv
    import sys

    from samr.corpus import iter_corpus, iter_test_corpus
    from samr.predictor import PhraseSentimentPredictor
    from samr.data import Datapoint
    global predictor


    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename")
    config = parser.parse_args()
    config = json.load(open(config.filename))
    # print("I am printing Configs")
    # print(config)
    predictor = PhraseSentimentPredictor(**config)
    # print(list(iter_corpus())[:10])

    predictor.fit(list(iter_corpus()))
    # print("prediction Fitting Done")
    test = list(iter_test_corpus())
    # print("Testing Fitting Done")

    # print("Testing done")



    dataF = open("../data/outfinal2.csv")
    header_csv = dataF.readline()
    data = dataF.read().splitlines()
    test = [Datapoint(d.split(",")[0],None) for d in data]
    prediction = predictor.predict(test)

    print(header_csv[:-1]+",Sentiment")
    i=0
    for datapoint, sentiment in zip(test, prediction):
        data[i]+=","+str(sentiment)
        print(data[i])
        i+=1









