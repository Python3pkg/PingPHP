#!/bin/env python
# codeing: utf8

from ply import lex
from helper import *

reserved = set([
    # namespace
    'namespace', 'use', 'as', 'insteadof',
    # class and interface
    'class', 'extends', 'implements',
    'public', 'private', 'protected',
    'static', 'abstract', 'final',
    'interface', 'trait',

    # ctrl flow
    'if', 'elif', 'else',
    'for', 'in',
    'switch', 'case', 'default',
    'while', 'do',
    'declare',

    # function
    'def',

    # op
    'new', 'clone',
    'instanceof',

    'not', 'or', 'and',

    'const', 'global',

    'try', 'catch', 'finally',

    'yield',

    'lambda'

])

strStatment = set(['pass', 'break', 'continue', 'echo', 'print', 'require', 'require_once', 
    'include', 'include_once', 'return', 'throw'])

reservedMap = {
    'not' : '!',
    'and' : '&&',
    'or' : '||'
}

commentAndNative = [
    'DOCCOMMENT',
    'INLINECOMMENT',
    'NATIVEPHP',
    'EMPTYLINE'
]

braces = [
    'LPARENT',
    'RPARENT',
    #'LBRACE',
    #'RBRACE',
    'LBRACKET',
    'RBRACKET'
]

bit = [
    'SHIFT',
    'ANDOP',
    'BITNOT',
    'BITOR',
    'BITXOR'
]


t_ANDOP = r'&'
t_BITNOT = r'~'
t_BITOR = r'\|'
t_BITXOR = r'\^'

math = [
    'EXPONENT',
    'MATH1',
    'MATH2',
    'INDECREMENT',
]

t_EXPONENT = r'\*\*     '
t_MATH1 = r'\*|/|%'
t_MATH2 = r'\+|-'
t_INDECREMENT = r'(\+\+)|(--)'

slash = [
    'SLASH',
    'FOLDLINE'
]

numAndStr = [
    'STRING',
    'NUMBER'
]

inOutdent = [
    'INDENT',
    'OUTDENT'
]

tokens = [
    'ASSIGN',
    'COMPARE',
    'CAST',
    'AT',
    'STRCAT',
    'SCOPEOP',
    'INDENTIFIER',
    'COMMA',
    'THREEDOT',
    'DOT',
    'COLON',
    'SPACE',
    'TAB',
    'NEWLINE',
    'TERMINATOR',
    'STATEMENT',
    'NAMESPACEBEFORESLASH',
    'EXEC'

] + map(lambda x: x.upper(), reserved) + commentAndNative + braces + bit + math + slash + numAndStr + inOutdent

def lineNoInc(t):
    t.lexer.lineno += t.value.count('\n')

t_CAST = r'\([ \t]*((int)|(float)|(double)|(string)|(array)|(object)|(binary)|(bool)|(unset))[ \t]*\)'
t_AT = r'@'
def t_DOCCOMMENT(t):
    r'((\'\'\'((?!\'\'\')[\s\S])*\'\'\')|(\'{6,8})|("""((?!""")[\s\S])*""")|("{6,8}))[ \t]*\n'
    lineNoInc(t)
    pos = t.value.rfind('"""')
    if pos == -1:
        pos = t.value.rfind('\'\'\'')
    t.value = '/**' + t.value[3:pos] + '**/'
    return t

def t_NATIVEPHP(t):
    r'<\?php((?!<\?php)[\s\S])*\?>[ \t]*(?=\n)'
    lineNoInc(t)
    t.value = t.value[6:].lstrip()
    pos2 = t.value.rfind('?>')
    t.value = t.value[0:pos2].rstrip()
    #print t.value
    return t


def t_EXEC(t):
    r'`(((?<!\\)`)|([^`]))*`'
    return t

t_SCOPEOP = r'::'
t_SPACE = r'[ ]'
t_TAB = r'\t'

def t_ASSIGN(t):
    r'(((\+|-|\*|/|%|&|\||^|(<<<)|(<<)|(>>))\s*)?=)(?![=])'
    if t.value[0:3] == '<<<':
        t.value = '.='
    return t


def t_STRCAT(t):
    r'<<<'
    t.value = '.'
    return t

def t_SHIFT(t):
    r'(<<)|(>>)'
    return t

def t_COMPARE(t):
    r'([=!]=[=]?)|(<>)|(>=?)|(<=?)'
    return t


t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_THREEDOT = r'\.\.\.'
t_DOT = r'\.'
t_SLASH = r'\\'


def t_FOLDLINE(t):
    r'\\[ ]*\n'
    lineNoInc(t)


def t_INLINECOMMENT(t):
    r'\#[^\n]*\n'
    lineNoInc(t)
    t.value = '//' + t.value[1:-1]
    return t

def t_NAMESPACEBEFORESLASH(t):
    r'namespace(?=[ \t]*\\[ \t]*[_a-zA-Z0-9])'
    return t

def t_NUMBER(t):
    r'(([0-9]+|(([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)))[eE][+-]?[0-9]+)|(([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*))|([1-9][0-9]*)|(0b[01]+)|(0[0-7]+)|(0[xX][0-9a-fA-F]+)|(true)|(false)|(null)|0'
    return t

def t_STRING(t):
    r'b?((\'(([^\'])|((?<=\\)(?<!\\\\)\'))*\')|("(([^"\n])|((?<=\\)(?<!\\\\)"))*"))'
    lineNoInc(t)
    return t
 
# handle id and reversed
def t_INDENTIFIER(t):
    r'(\$?[_a-zA-Z][_a-zA-Z0-9]*)|(__[A-Z_]+__)'
    if t.value in reserved:
        t.type = t.value.upper()
        if t.value in reservedMap:
            t.value = reservedMap[t.value]
    elif t.value in strStatment:
        t.type = 'STATEMENT'
    return t


t_COLON = r':'


def t_error(t):
    from helper import errorMsg
    errorMsg('Lexical', t)


def t_NEWLINE(t):
    r'\n'
    lineNoInc(t) 
    return t


def token_list(lexer):
    return [t for t in lexer]


def make_lexToken(type, value, lineno, lexpos):
    tok = lex.LexToken()  # 'NEWLINE','\n',0,0)
    tok.type = type
    tok.value = value
    tok.lineno = lineno
    tok.lexpos = lexpos
    return tok


def change_token_list_new(tok_list):
    # from ply import lex
    dummy = make_lexToken('NEWLINE', '\n', 0, 0)
    tok_list.insert(0, dummy)

    dummy = make_lexToken('EOF', '', tok_list[-1].lineno + 1, tok_list[-1].lexpos + 1)
    tok_list.append(dummy)

    pre_space = 0
    count_start = False
    space_stack = [0]
    content_cache = []

    result_tok_list = []
    for tok in tok_list:
        if count_start == False and (tok.type in ('NEWLINE', 'INLINECOMMENT')):
            pre_space = 0
            count_start = True
            if tok.type == 'NEWLINE':
                tok = make_lexToken('TERMINATOR', '', tok.lineno, tok.lexpos)
            result_tok_list.append(tok)
            continue
        if count_start:
            if tok.type == 'SPACE':
                pre_space += 1
            elif tok.type == 'TAB':
                pre_space += 4
            elif tok.type in ['NEWLINE', 'INLINECOMMENT', 'DOCCOMMENT']:
                pre_space = 0
                if tok.type == 'NEWLINE':
                    tok = make_lexToken('EMPTYLINE', '', tok.lineno, tok.lexpos)
                content_cache.append(tok)
            else:
                count_start = False

                if space_stack[-1] < pre_space:
                    space_stack.append(pre_space)
                    indent = make_lexToken('INDENT', '', tok.lineno, tok.lexpos)
                    result_tok_list.append(indent)
                    # print 'INDENT'
                else:
                    while (space_stack[-1] > pre_space):
                        space_stack.pop()
                        indent = make_lexToken('OUTDENT', '', tok.lineno, tok.lexpos)
                        result_tok_list.append(indent)
                        # print 'OUTDENT'

                result_tok_list.extend(content_cache)
                result_tok_list.append(tok)
                content_cache = []
        else:
            if tok.type != 'SPACE' and tok.type != 'TAB':
                result_tok_list.append(tok)

    return result_tok_list[1:-1]



class PingLexer(object):
    def __init__(self, inputStr):
        lexer = lex.lex()
        lexer.input(inputStr)
        self.tokList = token_list(lexer)
        self.tokList = change_token_list_new(self.tokList)
        self.nowIndex = 0

    def token(self):
        if self.nowIndex < len(self.tokList):
            result = self.tokList[self.nowIndex]
            self.nowIndex += 1
            return result

    # Iterator interface
    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next


if __name__ == '__main__':
    filename = './test/Functions/anonymous.ping'
    initLogging()
    import sys
    print(sys.argv)
    if len(sys.argv)>1:
        filename = sys.argv[1]
    lexer = lex.lex()
    lexer.input(read(filename))
    tokList = token_list(lexer)
    for item in change_token_list_new(tokList):
        print item
