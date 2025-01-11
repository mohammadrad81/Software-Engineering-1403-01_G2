class PositionalTokenizer:
    
    SPLITTERS: set[str] = {" ",
                           "\u200c",
                           "\u2009",
                           "\n",
                           "\t",
                           ".",
                           ",",
                           ";",
                           "?",
                           "!",
                           ".",
                           "،",
                           "؛",
                           "!",
                           "؟",
                           "(",
                           ")",
                           "0",
                           "1",
                           "2",
                           "3",
                           "4",
                           "5",
                           "6",
                           "7",
                           "8",
                           "9",
                           "۰",
                           "۱",
                           "۲",
                           "۳",
                           "۴",
                           "۵",
                           "۶",
                           "۷",
                           "۸",
                           "۹",
                           "#",
                           "-",
                           "_"}

    def tokenize(self, text: str) -> list[tuple[int, int, str]]:
        """
            tokenizes a text
            each token has 3 entries
            (start: int, end: int, word: str)
            start is inclusive
            end is exclusive
            word is the string of token
        """
        if len(text) == 0:
            return []
        result: list[tuple[int, int, str]] = []
        start: int = None
        end: int = None
        for i in range(len(text)):
            character: str = text[i]
            if character in PositionalTokenizer.SPLITTERS:
                if start is not None:
                    end = i
                    word = text[start:end]
                    token = (start, end, word)
                    result.append(token)
                    start = None
                    end = None
            else:
                if start is None:
                    start = i
        if start is not None:
            end = len(text)
            word = text[start:end]
            token = (start, end, word)
            result.append(token)
        return result