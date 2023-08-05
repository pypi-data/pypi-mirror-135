# Genz Tokenize

[Github](https://github.com/nghiemIUH/genz-tokenize)

## install via pip (from PyPI):

    pip install genz-tokenize

## Using

    from genz_tokenize import Tokenize
    tokenize = Tokenize('vocab.txt', 'bpe.codes')
    print(tokenize(['sinh_viên công_nghệ', 'hello'], maxlen = 10))
