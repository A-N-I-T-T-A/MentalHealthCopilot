def clean_bert_tokens(tokens):
    """
    Cleans WordPiece tokens to reconstruct human-readable words.
    """
    words = []
    current_word = ""
    for token in tokens:
        if token in ["[CLS]", "[SEP]", "[PAD]"]:
            continue
        if token.startswith("##"):
            current_word += token[2:]
        elif token in ["'", "’"] and current_word:
            current_word += token
        else:
            if current_word:
                words.append(current_word)
            current_word = token
    if current_word:
        words.append(current_word)
    return [w for w in words if w.strip()]
