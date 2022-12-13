# Report of parameters

## 1

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "y",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "y",
    "lemmatization": "n"
}
ACIERTO = 64.43%
```

## 2

```js
{
    "numbers": "n",
    "long_words": "n",
    "lowercase": "n",
    "punctuation_marks": "n",
    "stopwords": "n",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 31.19%
```

## 3

```js
{
    "numbers": "y",
    "long_words": "n",
    "lowercase": "n",
    "punctuation_marks": "n",
    "stopwords": "n",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 32.02%
```

## 4

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "n",
    "punctuation_marks": "n",
    "stopwords": "n",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 32.17%
```

### POR AHORA ES MEJOR QUITAR NUMEROS Y LONG_WORDS

## 5

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "n",
    "stopwords": "n",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 36.16%
```

## 6

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 43.66%
```

## 7

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "y",
    "emojis": "n",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 43.21%
```

### QUITAR STOPWORDS ES MALA OPCION

## 8

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "w",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 43.68%
```

## 9

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "n",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 43.68%
```

### ES INDIFERENTE QUITAR O PONER EN PALABRAS LOS EMOTICONOS, ASI QUE LOS QUITAMOS PARA QUE SEA MAS EFICIENTE

## 10

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "n",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 49.68%
```

## 11

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "n",
    "lemmatization": "n"
}
ACIERTO = 55.19%
```

## 12

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "y",
    "lemmatization": "n"
}
ACIERTO = 64.83%
```

## 13

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "n",
    "lemmatization": "y"
}
ACIERTO = 61.36%
```

## BEST

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "y",
    "lemmatization": "n"
}
ACIERTO = 64.82%
```

## NOW TEST WITH UNK IN UNDER 3

```js
ACIERTO = 63.85%
```

## ...AND 4

```js
ACIERTO = 63.35%
```

## BEST, UNK -> 2

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "y",
    "lemmatization": "n"
}
ACIERTO = 64.82%
```

## WITH 2 OF LAPLACE

```js
ACIERTO = 64.77%
```

## WITH 3 OF LAPLACE

```js
ACIERTO = 64.79%
```

## BEST, UNK -> 2, LAPLACE -> 1

```js
{
    "numbers": "y",
    "long_words": "y",
    "lowercase": "y",
    "punctuation_marks": "y",
    "stopwords": "n",
    "emojis": "y",
    "url_html_hashtags": "y",
    "spell_check": "y",
    "stemming": "y",
    "lemmatization": "n"
}
ACIERTO = 64.82%
```

## BEST_TEST

No numbers? (y/n): n|y
No long words? (y/n): n|y
Lowercase? (y/n): y
No punctuation marks? (y/n): y
No stopwords? (y/n): n|y
No emojis? (y/n/w): n|y
No URLs and HTML hashtags? (y/n): y
Spell check? (y/n): n
Stemming? (y/n): n
Lemmatization? (y/n): n

80.65%
