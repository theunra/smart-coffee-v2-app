prediction_dict = {
    'unclass' : 0,
    'light' : 1,
    'medium' : 2,
    'dark' : 3
}

pred = 'light'

print(pred)

pred = prediction_dict[pred]

print(pred)

pred = list(prediction_dict.keys())[pred]

print(pred)