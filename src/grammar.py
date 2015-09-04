'''PingPHP grammar file
'''
from nodes import *
from lexer import *
import logging

'''
grammar:

    Root :
         | Body

    Body : Line
         | Body Line

    Line : CodeBlock
         | Statement
         | Embeded

    Embeded : DOCCOMMENT
            | NATIVEPHP
            | EMPTYLINE
            | INLINECOMMENT

    Statement : StatementWithoutTerminator Terminator
              | LambdaAssignStatement

    StatementWithoutTerminator : Expression
                               | STATEMENT
                               | Return
                               | Namespace
                               | UseNamespace
                               | GlobalDec
                               | ConstDefWithoutTerminator
                               | Throw
                               | Yield

    JustStrStatementWithTerminator : STATEMENT Terminator

    CodeBlock : If
              | Switch
              | For
              | While
              | DoWhile
              | Try
              | FuncDef
              | Class
              | Interface

    Expression : Value
               | Assign
               | Operation
               | Call
               | LPARENT Expression RPARENT
               | Lambda

    Block : INDENT Body OUTDENT


Value and Assign:
    InitModifier :
                 | AssignRightSide

    AssignRightSide : ASSIGN Expression

    Value : Assignable
          | Literal

    Literal : SimpleLiteral
            | ArrayLiteral

    SimpleLiteral : NUMBER
                  | STRING

    ArrayLiteral : LBRACKET ArrayLiteralContentList RBRACKET

    ArrayLiteralContentList : ArrayLiteralContent
                            | ArrayLiteralContentList COMMA ArrayLiteralContent

    ArrayLiteralContent : Expression
                        | SimpleLiteral COLON Expression

    Varible : NsContentName
            | NsContentName SCOPEOP INDENTIFIER

    Assignable : Varible
               | Assignable LBRACKET Expression RBRACKET
               | Assignable DOT INDENTIFIER

    Assign : Assignable AssignRightSide
           | ArrayLiteral AssignRightSide


Param and Arg
    ArgList :
            | Arg
            | ArgList COMMA Arg

    Arg : Expression ThreeDotModifier

    ParamList :
              | Param
              | ParamList COMMA Param

    Param : RefModifier INDENTIFIER ThreeDotModifier TypeModifier InitModifier

    TypeModifier : 
                 | COLON NsContentName

Call
    Call : Callable ArgList RPARENT

    Callable : NsContentName LPARENT
             | NsContentName SCOPEOP INDENTIFIER LPARENT
             | Expression LPARENT

Lambda
    Lambda : LAMBDA ParamList UseModifier COLON Terminator Block
    UseModifier : 
                | USE ParamList

Terminator
    Terminator : INLINECOMMENT
               | TERMINATOR

Namespace
    Namespace : NAMESPACE NsContentName
    UseNamespace : USE NsContentNameAsIdList

    NsContentName : INDENTIFIER
                  | NAMESPACEBEFORESLASH
                  | BACKSLASH INDENTIFIER
                  | NsContentName BACKSLASH INDENTIFIER

    NsContentNameList : NsContentName
                      | NsContentNameList COMMA NsContentName

    NsContentNameAsId : NsContentName
                      | NsContentName AS INDENTIFIER

    NsContentNameAsIdList : NsContentNameAsId
                          | NsContentNameAsIdList COMMA NsContentNameAsId
If
    If : IfBlock
       | IfBlock ELSE Block

    IfBlock : IF Expression COLON Terminator Block
            | IfBlock ELIF Expression COLON Terminator Block

Switch
    Switch : SWITCH Expression COLON Terminator SwitchContent

    SwitchContent : INDENT InSwitchDefList OUTDENT

    InSwitchDefList : InSwitchDef
                    | InSwitchDefList InSwitchDef

    InSwitchDef : Case
                | Embeded

    ValueList : Value
              | ValueList COMMA Value

    Case : CASE ValueList COLON Terminator Block
         | DEFAULT COLON Terminator Block

For
    For : FOR RefModifier INDENTIFIER IN Expression COLON Terminator Block
    For : FOR RefModifier INDENTIFIER COMMA RefModifier INDENTIFIER IN Expression COLON Terminator Block
 

While
    While : WHILE Expression COLON Terminator Block

DoWhile
    DoWhile : DO COLON Terminator Block WHILE Expression Terminator

Try
    Try : TRY COLON Terminator Block Catch
        | TRY COLON Terminator Block Catch FINALLY COLON Terminator Block

Catch : 
          | Catch CATCH LPARENT Varible COLON NsContentName RPARENT COLON Terminator Block

Class and Interface
    Class : CLASS INDENTIFIER ExtendsModifier ImplementsModifier COLON Terminator ClassContent

    ClassContent : INDENT InClassDefList OUTDENT

    InClassDefList : InClassDef
                   | InClassDefList InClassDef

    InClassDef : Embeded
               | JustStrStatementWithTerminator
               | DataMemberDef
               | ConstDef
               | MemberFuncDef

    Interface : INTERFACE INDENTIFIER ExtendsModifier COLON Terminator InterfaceContent

    InterfaceContent : INDENT InterfaceDefList OUTDENT

    InterfaceDefList : InterfaceDef
                     | InterfaceDefList InterfaceDef

    InterfaceDef : Embeded
                 | JustStrStatementWithTerminator
                 | ConstDef
                 | MemberFuncDec

    ExtendsModifier :
                    | EXTENDS NsContentName

    ImplementsModifier :
                       | IMPLEMENTS NsContentNameList

    AccessModifier :
                   | PUBLIC
                   | PRIVATE
                   | PROTECTED

    StaticModifier :
                   | STATIC

    RefModifier :
                | ANDOP

    MemberFuncDecWithoutTerminator: AccessModifier StaticModifier RefModifier INDENTIFIER LPARENT ParamList RPARENT

    MemberFuncDec : MemberFuncDecWithoutTerminator ReturnTypeModifierForDec Terminator

    ReturnTypeModifierForDec : 
                             | COLON NsContentName

    MemberFuncDef : MemberFuncDecWithoutTerminator COLON ReturnTypeModifier Terminator Block

    DataMemberDef : AccessModifier StaticModifier RefModifier INDENTIFIER InitModifier Terminator

FuncDef

    ReturnTypeModifier : 
                       | NsContentName

    FuncDef : DEF RefModifier INDENTIFIER LPARENT ParamList RPARENT COLON ReturnTypeModifier Terminator Block

    ConstDef : ConstDefWithoutTerminator Terminator

    ConstDefWithoutTerminator : CONST INDENTIFIER AssignRightSide

    Return : RETURN Expression
           | RETURN

    Throw : THROW Expression

    Yield : YIELD
          | YIELD Expression
          | YIELD Expression COMMA Expression

    GlobalDec : GLOBAL GlobalVaribleList

    GlobalVaribleList : INDENTIFIER
                      | GlobalVaribleList COMMA INDENTIFIER

Operation
    Operation : UMath
              | BMath
              | NewOrClone
              | Compare
              | Cast
              | InDecrement
              | UBit
              | BBit
              | ULogic
              | BLogic
              | InstanceOf
              | Ternary
              | At
              | Ref

    BMath : Expression MATH1 Expression
          | Expression MATH2 Expression

    UMath : MATH2 Expression %prec UMATH

    NewOrClone : NEW NsContentName LPARENT ArgList RPARENT
               | NEW Varible
               | CLONE Varible

    Compare : Expression COMPARE Expression

    Cast : CAST Expression

    InDecrement : INDECREMENT Assignable 
                | Assignable INDECREMENT

    UBit : BITNOT Expression

    BBit : Expression SHIFT Expression
         | Expression ANDOP Expression
         | Expression BITOR Expression
         | Expression BITXOR Expression

    InstanceOf : Expression INSTANCEOF NsContentName

    ULogic : NOT Expression
    BLogic : Expression AND Expression
           | Expression OR Expression

    Ternary : Expression IF Expression ELSE Expression

    At : AT Expression

    Ref : ANDOP Expression %prec REFOP

'''

start = 'Root'

precedence = [
    ('nonassoc', 'CLONE', 'NEW'),
    ('left', 'LBRACKET'),
    ('right', 'EXPONENT'),
    ('right', 'INDECREMENT', 'BITNOT', 'CAST', 'AT'),
    ('nonassoc', 'INSTANCEOF'),
    ('right', 'NOT'),
    ('right', 'UMATH'),
    ('left', 'MATH1'),
    ('left', 'MATH2'),
    ('left', 'SHIFT'),
    ('nonassoc', 'COMPARE'),
    ('left', 'ANDOP'),
    ('left', 'REFOP'),
    ('left', 'BITXOR'),
    ('left', 'BITOR'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'IF', 'ELSE'),
    ('right', 'ASSIGN'),
    ('left', 'COMMA')
]

precedence.reverse()


def p_Root(p):
    '''
    Root :
         | Body
    '''
    if len(p) < 2:
        p[0] = Root(None)
    else:
        p[0] = Root(p[1])


def p_Body(p):
    '''
    Body : Line
         | Body Line
    '''
    if not isinstance(p[1], Body):
        p[0] = Body(None, p[1])
    else:
        p[0] = Body(p[1], p[2])


def p_Line(p):
    '''
    Line : CodeBlock
         | Statement
         | Embeded
    '''
    p[0] = Line(p[1])


def p_Embeded(p):
    '''
    Embeded : DOCCOMMENT
            | NATIVEPHP
            | EMPTYLINE
            | INLINECOMMENT

    '''
    p[0] = Embeded(p[1])


def p_Statement(p):
    '''
    Statement : StatementWithoutTerminator Terminator
              | LambdaAssignStatement
    '''
    if len(p) < 3:
        term = Terminator('')
    else:
        term = p[2]
    p[0] = Statement(p[1], term)

def p_LambdaAssignStatement(p):
    '''
    LambdaAssignStatement : Assignable ASSIGN Lambda
    '''
    p[0] = LambdaAssignStatement(p[1], p[3])


def p_StatementWithoutTerminator(p):
    '''
    StatementWithoutTerminator : Expression
                               | STATEMENT
                               | Return
                               | Namespace
                               | UseNamespace
                               | GlobalDec
                               | ConstDefWithoutTerminator
                               | Throw
                               | Yield
    '''
    p[0] = StatementWithoutTerminator(p[1])


def p_JustStrStatementWithTerminator(p):
    '''
    JustStrStatementWithTerminator : STATEMENT Terminator
    '''
    p[0] = JustStrStatementWithTerminator(p[1], p[2])


def p_CodeBlock(p):
    '''
    CodeBlock : If
              | Switch
              | For
              | While
              | DoWhile
              | Try
              | FuncDef
              | Class
              | Interface
    '''
    p[0] = CodeBlock(p[1])


def p_Expression(p):
    '''
    Expression : Value
               | Assign
               | Operation
               | Call
               | LPARENT Expression RPARENT
               | Lambda
    '''
    if len(p)==2:
        p[0] = Expression(p[1])
    else:
        p[0] = Expression(p[2])


def p_Block(p):
    '''
    Block : INDENT Body OUTDENT
    '''
    p[0] = Block(p[2])


def p_InitModifier(p):
    '''
    InitModifier :
                 | AssignRightSide
    '''
    if len(p) < 2:
        p[0] = InitModifier(None)
    else:
        p[0] = InitModifier(p[1])


def p_AssignRightSide(p):
    '''
    AssignRightSide : ASSIGN Expression
    '''
    p[0] = AssignRightSide(p[1], p[2])


def p_Value(p):
    '''
    Value : Assignable
          | Literal
    '''
    p[0] = Value(p[1])


def p_Literal(p):
    '''
    Literal : SimpleLiteral
            | ArrayLiteral
    '''
    p[0] = Literal(p[1])


def p_SimpleLiteral(p):
    '''
    SimpleLiteral : NUMBER
                  | STRING
    '''
    p[0] = SimpleLiteral(p[1])


def p_ArrayLiteral(p):
    '''
    ArrayLiteral : LBRACKET ArrayLiteralContentList RBRACKET
    '''
    p[0] = ArrayLiteral(p[2])


def p_ArrayLiteralContentList(p):
    '''
    ArrayLiteralContentList : ArrayLiteralContent
                            | ArrayLiteralContentList COMMA ArrayLiteralContent
    '''
    if len(p) < 3:
        p[0] = ArrayLiteralContentList(None, p[1])
    else:
        p[0] = ArrayLiteralContentList(p[1], p[3])


def p_ArrayLiteralContent(p):
    '''
    ArrayLiteralContent : Expression
    ArrayLiteralContent : SimpleLiteral COLON Expression
    '''
    if len(p) < 3:
        p[0] = ArrayLiteralContent(None, p[1])
    else:
        p[0] = ArrayLiteralContent(p[1], p[3])


def p_Varible(p):
    '''
    Varible : NsContentName
            | NsContentName SCOPEOP INDENTIFIER
    '''
    if len(p) < 3:
        p[0] = Varible(None, p[1])
    else:
        p[0] = Varible(p[1], p[3])


def p_Assignable(p):
    '''
    Assignable : Varible
               | Assignable LBRACKET Expression RBRACKET
               | Assignable DOT INDENTIFIER
    '''
    if len(p) == 2:
        p[0] = Assignable(p[1], None, None)
    elif len(p) == 5:
        p[0] = Assignable(p[1], p[3], None)
    else:
        p[0] = Assignable(p[1], None, p[3])


def p_Assign(p):
    '''
    Assign : Assignable AssignRightSide
           | ArrayLiteral AssignRightSide
    '''
    p[0] = Assign(p[1], p[2])


def p_ArgList(p):
    '''
    ArgList :
            | Arg
            | ArgList COMMA Arg
    '''
    if len(p) == 1:
        p[0] = ArgList(None, None)
    elif len(p) == 2:
        p[0] = ArgList(None, p[1])
    else:
        p[0] = ArgList(p[1], p[3])


def p_Arg(p):
    '''
    Arg : Expression ThreeDotModifier
    '''
    if len(p) <= 2:
        p[0] = Arg(p[1], None)
    else:
        p[0] = Arg(p[1], p[2])


def p_ParamList(p):
    '''
    ParamList :
              | Param
              | ParamList COMMA Param
    '''
    if len(p) == 1:
        p[0] = ParamList(None, None)
    elif len(p) == 2:
        p[0] = ParamList(None, p[1])
    else:
        p[0] = ParamList(p[1], p[3])

def p_ThreeDotModifier(p):
    '''
    ThreeDotModifier :
                     | THREEDOT
    '''
    if len(p) <= 1:
        p[0] = ThreeDotModifier(None)
    else:
        p[0] = ThreeDotModifier(p[1])


def p_Param(p):
    '''
    Param : RefModifier INDENTIFIER ThreeDotModifier TypeModifier InitModifier
    '''
    p[0] = Param(p[1], p[2], p[3], p[4], p[5])

def p_TypeModifier(p):
    '''
    TypeModifier : 
                 | COLON NsContentName
    '''
    if len(p) <= 1:
        p[0] = TypeModifier(None)
    else:
        p[0] = TypeModifier(p[2])


def p_Call(p):
    '''
    Call : Callable ArgList RPARENT
    '''
    p[0] = Call(p[1], p[2])


def p_Callable(p):
    '''
    Callable : NsContentName LPARENT
             | NsContentName SCOPEOP INDENTIFIER LPARENT
             | Expression LPARENT
    '''
    if len(p) <= 3:
        p[0] = Callable(p[1], None)
    else:
        p[0] = Callable(p[1], p[3])

def p_Lambda(p):
    '''
    Lambda : LAMBDA LPARENT ParamList RPARENT UseModifier COLON Terminator Block
    '''
    p[0] = Lambda(p[3], p[5], p[7], p[8])

def p_UseModifier(p):
    '''
    UseModifier : 
                | USE LPARENT ParamList RPARENT
    '''
    if len(p) <= 1:
        p[0] = UseModifier(None)
    else:
        p[0] = UseModifier(p[3])


def p_Terminator(p):
    '''
    Terminator : INLINECOMMENT
               | TERMINATOR
    '''
    p[0] = Terminator(p[1])


def p_Namespace(p):
    '''
    Namespace : NAMESPACE NsContentName
    '''
    p[0] = Namespace(p[2])


def p_UseNamespace(p):
    '''
    UseNamespace : USE NsContentNameAsIdList
    '''
    p[0] = UseNamespace(p[2])


def p_NsContentName(p):
    '''
    NsContentName : INDENTIFIER
                  | NAMESPACEBEFORESLASH
                  | SLASH INDENTIFIER
                  | NsContentName SLASH INDENTIFIER
    '''
    if len(p) == 2:
        p[0] = NsContentName(None, p[1])
    elif len(p) == 3:
        p[0] = NsContentName(None, p[1] + p[2])
    else:
        p[0] = NsContentName(p[1], p[2] + p[3])


def p_NsContentNameList(p):
    '''
    NsContentNameList : NsContentName
                      | NsContentNameList COMMA NsContentName
    '''
    if len(p) == 2:
        p[0] = NsContentNameList(None, p[1])
    else:
        p[0] = NsContentNameList(p[1], p[3])


def p_NsContentNameAsId(p):
    '''
    NsContentNameAsId : NsContentName
                      | NsContentName AS INDENTIFIER
    '''
    if len(p) == 2:
        p[0] = NsContentNameAsId(p[1])
    else:
        p[0] = NsContentNameAsId(p[1], p[3])


def p_NsContentNameAsIdList(p):
    '''
    NsContentNameAsIdList : NsContentNameAsId
                          | NsContentNameAsIdList COMMA NsContentNameAsId
    '''
    if len(p) == 2:
        p[0] = NsContentNameAsIdList(None, p[1])
    else:
        p[0] = NsContentNameAsIdList(p[1], p[3])


def p_If(p):
    '''
    If : IfBlock
       | IfBlock ELSE COLON Terminator Block
    '''
    if len(p) == 2:
        p[0] = If(p[1], None, None)
    else:
        p[0] = If(p[1], p[5], p[4])


def p_IfBlock(p):
    '''
    IfBlock : IF Expression COLON Terminator Block
            | IfBlock ELIF Expression COLON Terminator Block
    '''
    if isinstance(p[1], basestring):
        p[0] = IfBlock(None, p[2], p[4], p[5])
    else:
        p[0] = IfBlock(p[1], p[3], p[5], p[6])


def p_Switch(p):
    '''
    Switch : SWITCH Expression COLON Terminator SwitchContent
    '''
    p[0] = Switch(p[2], p[4], p[5])


def p_SwitchContent(p):
    '''
    SwitchContent : INDENT InSwitchDefList OUTDENT
    '''
    p[0] = SwitchContent(p[2])


def p_InSwitchDefList(p):
    '''
    InSwitchDefList : InSwitchDef
                    | InSwitchDefList InSwitchDef
   '''
    if len(p) <= 2:
        p[0] = InSwitchDefList(None, p[1])
    else:
        p[0] = InSwitchDefList(p[1], p[2])

def p_InSwitchDef(p):
    '''
    InSwitchDef : Case
                | Embeded
    '''
    p[0] = InSwitchDef(p[1])

def p_ValueList(p):
    '''
    ValueList : Value
                | Value COMMA Value
    '''
    if len(p)<=2:
        p[0] = ValueList(None, p[1])
    else:
        p[0] = ValueList(p[1], p[3])


def p_Case(p):
    '''
    Case : CASE ValueList COLON Terminator Block
         | DEFAULT COLON Terminator Block
    '''
    if p[1] == 'case':
        p[0] = Case(p[1], p[2], p[4], p[5])
    else:
        p[0] = Case(p[1], None, p[3], p[4])


def p_For(p):
    '''
    For : FOR RefModifier INDENTIFIER IN Expression COLON Terminator Block
    For : FOR RefModifier INDENTIFIER COMMA RefModifier INDENTIFIER IN Expression COLON Terminator Block
    '''
    if p[4] == 'in':
        p[0] = For(p[2], p[3], None, None, p[5], p[7], p[8])
    else:
        p[0] = For(p[2], p[3], p[5], p[6], p[8], p[10], p[11])

def p_While(p):
    '''
    While : WHILE Expression COLON Terminator Block
    '''
    p[0] = While(p[2], p[4], p[5])


def p_DoWhile(p):
    '''
    DoWhile : DO COLON Terminator Block CommentOrEmptyLineList WHILE Expression Terminator
    '''
    p[0] = DoWhile(p[3], p[4], p[5], p[7], p[8])

def p_CommentOrEmptyLineList(p):
    '''
    CommentOrEmptyLineList : CommentOrEmptyLine
                           | CommentOrEmptyLineList CommentOrEmptyLine 
    '''
    if len(p) <= 2:
        p[0] = CommentOrEmptyLineList(None, p[1])
    else:
        p[0] = CommentOrEmptyLineList(p[1], p[2])

def p_CommentOrEmptyLine(p):
    '''
    CommentOrEmptyLine : EMPTYLINE
                       | DOCCOMMENT
                       | INLINECOMMENT
    '''
    p[0] = CommentOrEmptyLine(p[1])

def p_Try(p):
    '''
    Try : TRY COLON Terminator Block Catch
        | TRY COLON Terminator Block Catch FINALLY COLON Terminator Block
    '''
    if len(p) <= 6:
        p[0] = Try(p[3], p[4], p[5], None, None)
    else:
        p[0] = Try(p[3], p[4], p[5], p[8], p[9])

def p_Catch(p):
    '''
    Catch : 
          | Catch CATCH LPARENT Varible COLON NsContentName RPARENT COLON Terminator Block
    '''
    if len(p) <= 1:
        p[0] = Catch(None, None, None, None, None)
    else:
        p[0] = Catch(p[1], p[4], p[6], p[9], p[10])


def p_Class(p):
    '''
    Class : CLASS INDENTIFIER ExtendsModifier ImplementsModifier COLON Terminator ClassContent
    '''
    p[0] = Class(p[2], p[3], p[4], p[6], p[7])


def p_ClassContent(p):
    '''
    ClassContent : INDENT InClassDefList OUTDENT
    '''
    p[0] = ClassContent(p[2])


def p_InClassDefList(p):
    '''
    InClassDefList : InClassDef
                   | InClassDefList InClassDef
    '''
    if len(p) < 3:
        p[0] = InClassDefList(None, p[1])
    else:
        p[0] = InClassDefList(p[1], p[2])


def p_InClassDef(p):
    '''
    InClassDef : Embeded
               | JustStrStatementWithTerminator
               | DataMemberDef
               | ConstDef
               | MemberFuncDef
    '''
    p[0] = InClassDef(p[1])


def p_Interface(p):
    '''
    Interface : INTERFACE INDENTIFIER ExtendsModifier COLON Terminator InterfaceContent
    '''
    p[0] = Interface(p[2], p[3], p[5], p[6])


def p_InterfaceContent(p):
    '''
    InterfaceContent : INDENT InterfaceDefList OUTDENT
    '''
    p[0] = InterfaceContent(p[2])


def p_InterfaceDefList(p):
    '''
    InterfaceDefList : InterfaceDef
                     | InterfaceDefList InterfaceDef
    '''
    if len(p) < 3:
        p[0] = InterfaceDefList(None, p[1])
    else:
        p[0] = InterfaceDefList(p[1], p[2])


def p_InterfaceDef(p):
    '''
    InterfaceDef : Embeded
                 | JustStrStatementWithTerminator
                 | ConstDef
                 | MemberFuncDec
    '''
    p[0] = InterfaceDef(p[1])


def p_ExtendsModifier(p):
    '''
    ExtendsModifier :
                    | EXTENDS NsContentName
    '''
    if len(p) > 1:
        p[0] = ExtendsModifier(p[2])
    else:
        p[0] = ExtendsModifier(None)


def p_ImplementsModifier(p):
    '''
    ImplementsModifier :
                       | IMPLEMENTS NsContentNameList
    '''
    if len(p) > 1:
        p[0] = ImplementsModifier(p[2])
    else:
        p[0] = ImplementsModifier(None)


def p_AccessModifier(p):
    '''
    AccessModifier :
                   | PUBLIC
                   | PRIVATE
                   | PROTECTED
    '''
    if len(p) > 1:
        p[0] = AccessModifier(p[1])
    else:
        p[0] = AccessModifier('public')


def p_StaticModifier(p):
    '''
    StaticModifier :
                   | STATIC
    '''
    if len(p) > 1:
        p[0] = StaticModifier(p[1])
    else:
        p[0] = StaticModifier(None)

def p_RefModifier(p):
    '''
    RefModifier : 
                | ANDOP
    '''
    if len(p)<2:
        p[0] = RefModifier(None)
    else:
        p[0] = RefModifier(p[1])



def p_MemberFuncDecWithoutTerminator(p):
    '''
    MemberFuncDecWithoutTerminator : AccessModifier StaticModifier RefModifier INDENTIFIER LPARENT ParamList RPARENT
    '''
    p[0] = MemberFuncDecWithoutTerminator(p[1], p[2], p[3], p[4], p[6])


def p_MemberFuncDec(p):
    '''
    MemberFuncDec : MemberFuncDecWithoutTerminator ReturnTypeModifierForDec Terminator
    '''
    p[0] = MemberFuncDec(p[1], p[2], p[3])

def p_ReturnTypeModifierForDec(p):
    '''
    ReturnTypeModifierForDec : 
                             | COLON NsContentName
    '''
    if len(p) <= 1:
        p[0] = ReturnTypeModifierForDec(None)
    else:
        p[0] = ReturnTypeModifierForDec(p[2])


def p_MemberFuncDef(p):
    '''
    MemberFuncDef : MemberFuncDecWithoutTerminator COLON ReturnTypeModifier Terminator Block
    '''
    p[0] = MemberFuncDef(p[1], p[3], p[4], p[5])


def p_DataMemberDef(p):
    '''
    DataMemberDef : AccessModifier StaticModifier RefModifier INDENTIFIER InitModifier Terminator
    '''
    p[0] = DataMemberDef(p[1], p[2], p[4], p[5], p[6])

def p_ReturnTypeModifier(p):
    '''
    ReturnTypeModifier : 
                       | NsContentName
    '''
    if len(p) <= 1:
        p[0] = ReturnTypeModifier(None)
    else:
        p[0] = ReturnTypeModifier(p[1])

def p_FuncDef(p):
    '''
    FuncDef : DEF RefModifier INDENTIFIER LPARENT ParamList RPARENT COLON ReturnTypeModifier Terminator Block
    '''
    p[0] = FuncDef(p[2], p[3], p[5], p[8], p[9], p[10])


def p_ConstDefWithoutTerminator(p):
    '''
    ConstDefWithoutTerminator : CONST INDENTIFIER AssignRightSide
    '''
    p[0] = ConstDefWithoutTerminator(p[2], p[3])


def p_ConstDef(p):
    '''
    ConstDef : ConstDefWithoutTerminator Terminator
    '''
    p[0] = ConstDef(p[1], p[2])


def p_Return(p):
    '''
    Return : RETURN Expression
           | RETURN
    '''
    if len(p) >= 3:
        p[0] = Return(p[2])
    else:
        p[0] = Return(None)


def p_Throw(p):
    '''
    Throw : THROW Expression
    '''
    p[0] = Throw(p[2])


def p_Yield(p):
    '''
    Yield : YIELD
          | YIELD Expression
          | YIELD Expression COMMA Expression
    '''
    if len(p) == 2:
        p[0] = Yield(None, None)
    elif len(p) == 3:
        p[0] = Yield(p[2], None)
    else:
        p[0] = Yield(p[2], p[4])


def p_GlobalDec(p):
    '''
    GlobalDec : GLOBAL GlobalVaribleList
    '''
    p[0] = GlobalDec(p[2])


def p_GlobalVaribleList(p):
    '''
    GlobalVaribleList : INDENTIFIER
                      | GlobalVaribleList COMMA INDENTIFIER
    '''
    if len(p) > 2:
        p[0] = GlobalVaribleList(p[1], p[3])
    else:
        p[0] = GlobalVaribleList(None, p[1])


def p_Operation(p):
    '''
    Operation : UMath
              | BMath
              | NewOrClone
              | Compare
              | Cast
              | InDecrement
              | UBit
              | BBit
              | ULogic
              | BLogic
              | InstanceOf
              | Ternary
              | At
              | Ref
    '''
    p[0] = Operation(p[1])

def p_BMath(p):
    '''
    BMath : Expression MATH1 Expression
          | Expression MATH2 Expression
          | Expression EXPONENT Expression
    '''
    p[0] = BMath(p[1], p[2], p[3])

def p_UMath(p):
    '''
    UMath : MATH2 Expression %prec UMATH
    '''
    p[0] = UMath(p[1], p[2])


def p_Cast(p):
    '''
    Cast : CAST Expression
    '''
    p[0] = Cast(p[1], p[2])


def p_InDecrement(p):
    '''
    InDecrement : INDECREMENT Assignable 
                | Assignable INDECREMENT
    '''
    from helper import isString
    if isString(p[1]):
        p[0] = InDecrement(p[1], p[2], False)
    else:
        p[0] = InDecrement(p[2], p[1], True)

def p_UBit(p):
    '''
    UBit : BITNOT Expression
    '''
    p[0] =  UBit(p[1], p[2])

def p_BBit(p):
    '''
    BBit : Expression SHIFT Expression
         | Expression ANDOP Expression
         | Expression BITOR Expression
         | Expression BITXOR Expression
    '''
    p[0] = BBit(p[1], p[2], p[3])

def p_InstanceOf(p):
    '''
    InstanceOf : Expression INSTANCEOF NsContentName
    '''
    p[0] = InstanceOf(p[1], p[2], p[3])

def p_ULogic(p):
    '''
    ULogic : NOT Expression
    '''
    p[0] = ULogic(p[1], p[2])

def p_BLogic(p):
    '''
    BLogic : Expression AND Expression
           | Expression OR Expression
    '''
    p[0] = BLogic(p[1], p[2], p[3])

def p_NewOrClone(p):
    '''
    NewOrClone : NEW NsContentName LPARENT ArgList RPARENT
               | NEW Varible
               | CLONE Varible
    '''
    if len(p) > 3:
        p[0] = NewOrClone(p[1], p[2], p[4], None)
    else:
        p[0] = NewOrClone(p[1], None, None, p[2])


def p_Compare(p):
    '''
    Compare : Expression COMPARE Expression
    '''
    p[0] = Compare(p[1], p[2], p[3])


def p_Ternary(p):
    '''
    Ternary : Expression IF Expression ELSE Expression
    '''
    p[0] = Ternary(p[3], p[1], p[5])


def p_At(p):
    '''
    At : AT Expression
    '''
    p[0] = At(p[1],p[2])

def p_Ref(p):
    '''
    Ref : ANDOP Expression %prec REFOP
    '''
    p[0] = Ref(p[1],p[2])

def p_error(p):
    from helper import errorMsg
    errorMsg("Grammar", p)
