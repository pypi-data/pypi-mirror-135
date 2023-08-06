# Visualization of tweet content
Just enter the username of the target account and you will be able to see the characteristics of the tweets of that account.<br>

We will use [wordcloud](https://github.com/amueller/word_cloud)  to visualize the tweet contents. This is a simple yet powerful visual representation object for text processing, which shows the most frequent word with bigger and bolder letters, and with different colors. The smaller the the size of the word the lesser it’s important.

# How to install whatweet

whattweew is available in public and can be installed by the following PyPI packaging command:
```
pip install whatweet
```

If you are using virtual environment, please use the package manager of the virtual environment (e.g., pipenv install, poetry add).

# How to run whatweet

whatweet needs at three parameters (`username`, `days`, `language`).

### Username

Enter the correct username for an account that has a certain number of tweets. However, **you cannot use a private account**.

### days

Enter the number of days to be counted backward from the current date ( **1 <= days <= 500** ).

For users with a relatively large number of tweets, it is recommended to enter a small number of days. The accuracy of the visualization will be better and the process will not be as heavy.

### language

Two languages, Japanese and English, are supported for this visualization. Each one is processed differently, so make sure you enter the user's language.

Enter `Japanese` for Japanese or `English` for English.

## Example

```
whatweet twitter 100 English
```

![twitter_image](https://github.com/hnt-series00/whatweet/blob/main/Figure_twitter.png?raw=true)