import sly

# read about sly
# here https://github.com/dabeaz/sly
# and here https://sly.readthedocs.io/en/latest/


class ExampleLexer(sly.Lexer):
    # a set of tokes we spit out
    tokens = { NUMBER }

    # these are also tokens, but they don't have state and take up exactly one
    # symbol, so it's more convinient this way. Otherwise this is completely
    # equivalent to defining PLUS, LPAREN, RPAREN.
    literals = { '+', '(', ')' }

    # ignore any of these symbols
    ignore = ' \r\t\n'

    # we can also ignore any regular expression (start the name with `ignore_`)
    #
    # read about the r'' strings here https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
    # basically, it's so don't have to type '\\' each time.
    #
    # read about regular expressions
    # here https://docs.python.org/3/howto/regex.html#regex-howto
    # and here https://docs.python.org/3/library/re.html
    ignore_comment = r'\#.*'

    # this is a definition of a token, also a regex, we must provide one for every token in `tokens` set.
    #
    # this one reads "one or more digits, then a stop ('.'), then one or more digits.
    # not the best one, but good enough as an example
    @_(r'[0-9]+\.[0-9]+')
    def NUMBER(self, t):
        # the token is a string by default.
        # we can define a function that does some "preprocessing".
        # here we convert it to a float.
        # if we didn't want to convert anything, we could just write
        # NUMBER = r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t


# base class for our tree
# AST stands for Abstract Syntax Tree
# read about it here https://en.wikipedia.org/wiki/Abstract_syntax_tree
class ASTNode(object):
    # AST nodes should be computable, i.e. return a number
    def compute(self):
        raise NotImplementedError

    # AST nodes should have a text representation
    def __str__(self):
        raise NotImplementedError

# this one represents a number
class NumNode(ASTNode):
    # we just store a number in this type of AST node
    def __init__(self, n):
        self.n = n

    # we alredy know this node's numeric value
    def compute(self):
        return self.n

    # to convert it to text, we just return the number as text
    def __str__(self):
        return str(self.n)

# this one represents a sum of two expressions
class AddNode(ASTNode):
    # we store references to another two AST nodes, the left operand of the
    # plus, and the right
    def __init__(self, l, r):
        self.l = l
        self.r = r

    # to compute this node's numeric value, we must compute values of our left
    # and right children and add them
    def compute(self):
        return self.l.compute() + self.r.compute()

    # the textual representation is '(left)+(right)'
    def __str__(self):
        return f'({self.l})+({self.r})'


class ExampleParser(sly.Parser):
    # this means that
    # a + b + c
    # is parsed as
    # (a + b) + c
    # rather than
    # a + (b + c)
    # read about precedence here https://en.wikipedia.org/wiki/Order_of_operations
    # and here https://en.wikipedia.org/wiki/Operator_associativity
    precedence = (
        ('left', '+'),
    )
    # declare that we use tokens from the ExampleLexer
    tokens = ExampleLexer.tokens

    # number is an expression
    @_('NUMBER')
    def expr(self, p):
        return NumNode(p.NUMBER)

    # expression in parentheses in an expression
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    # expression, then plus, then expression is an expression
    @_('expr "+" expr')
    def expr(self, p):
        return AddNode(p.expr0, p.expr1)


# this is a kind of function that you need to write, but for the full grammar
def parse(s):
    lexer = ExampleLexer()
    parser = ExampleParser()
    return parser.parse(lexer.tokenize(s))


if __name__ == '__main__':
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        try:
            res = parse(s)
            print('tree representation:', res)
            print('tree value:', res.compute())
        except Exception as e:
            print(e)
    print()
