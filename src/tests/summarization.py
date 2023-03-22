

words = []   # create an empty list to store the words

with open('stop_words_english.txt') as f:    # replace 'file.txt' with the name of your file
    for line in f:
        word = line.strip()    # remove any whitespace and newline characters from each line
        words.append(word)     # add the word to the list

ext = "I need a Python script that can scrape data from a given Wikipedia page. The script should be able to accept any URL page and " \
      "return that pages content."

ext_wrds = ext.split(sep=' ')

ext = [wrd for wrd in ext_wrds if wrd.lower() not in words]

print(ext)