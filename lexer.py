import re

class TokenError(Exception):
    def __init__(self, token_name, message):
        super().__init__(message)
        self.token = token_name
        self.message = message

def add_literal_tokens(token_info, literals):
    """Auguments token_info with token info for the token literals in literals."""

    for l in literals:
        token_info['@$' + l] = '(' + re.escape(l) + ')'

class Tokenizer(object):
    def __init__(self, token_info):
        """
        Initializes the tokenizer with token_info.

        token_info: Dictionary mapping tokens -> regexps. Must have '@@skip'.
        """

        # Verify that all tokens have only one capture group
        for k in token_info:
            try:
                c = re.compile(token_info[k])
            except re.error:
                raise TokenError(k, "Failed to compile regexp")
            if k == "@@skip":
                if c.groups != 0:
                    raise TokenError(k, "@@skip contains a capture group")
            elif c.groups != 1:
                raise TokenError(k, "Doesn't contain exactly one capture group")

        self.token_names_list = [k for k in token_info if not k.startswith('@@')]
        re_string = (token_info['@@skip'] +
            "(?:(?:" +
            ")|(?:".join([token_info[k] for k in self.token_names_list]) +
            ")|(.))" +
            token_info['@@skip']) # This is necessary so that skipping before EOF doesn't give errors

        self.lexing_re = re.compile(re_string)

        self.error_index = len(self.token_names_list) + 1

    def lex_input(self, input_str):
        """
        Lexes input, iterating over the read tokens.

        input_str: Source string to be lexed.
        Yields (token name, token text) tuples.
        """

        for m in self.lexing_re.finditer(input_str):
            if m.lastindex == self.error_index:
                raise TokenError(None, "Unexpected input `%s`" % (m.group(m.lastindex),))
            else:
                yield (self.token_names_list[m.lastindex-1], m.group(m.lastindex))
        yield ('@@eof', '')
