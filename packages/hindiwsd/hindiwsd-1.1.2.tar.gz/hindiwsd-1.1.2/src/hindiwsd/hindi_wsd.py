from hindiwsd import wsd, lesks


def wordsense(sentence):

    hinglish, hindi = wsd.preprocess_transliterate(sentence)
    print("Hindi Sentence:", hindi)
    pos = wsd.POS_tagger(hindi)

    for i in pos:
        lesks.lesk(i[0], i[1], hindi)

#wordsense("sentence here")


