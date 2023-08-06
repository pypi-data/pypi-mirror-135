# fstep

This is my learning python project, mock up [pku-minic/first-step](https://github.com/pku-minic/first-step) with python.


## instal

```
$ pip install fstep
```

## example

```first-step
# calculate the nth term of the Fibonacci sequence
fib(n) {
  if n <= 2 {
    return 1
  }
  else {
    return fib(n - 1) + fib(n - 2)
  }
}

main() {
  print(fib(input()))
  return 0
}
```

You can evaluate this program using the interpreter by running:

```
$ fstep -s examples/fib.fstep -i
20
6765
0
```

Or compile it to RISC-V assembly:

```
$ fstep -s examples/fib.fstep -a
```

## EBNF of first-step

```ebnf
Program       ::= {FunctionDef};
FunctionDef   ::= IDENT "(" [ArgsDef] ")" Block;
ArgsDef       ::= IDENT {"," IDENT};

Block         ::= "{" {Statement} "}";
Statement     ::= IDENT ":=" Expression
                | IDENT "=" Expression
                | FunctionCall
                | IfElse
                | "return" Expression;
IfElse        ::= "if" Expression Block ["else" (IfElse | Block)];

Expression    ::= LOrExpr;
LOrExpr       ::= LAndExpr {"||" LAndExpr};
LAndExpr      ::= EqExpr {"&&" EqExpr};
EqExpr        ::= RelExpr {("==" | "!=") RelExpr};
RelExpr       ::= AddExpr {("<" | "<=") AddExpr};
AddExpr       ::= MulExpr {("+" | "-") MulExpr};
MulExpr       ::= UnaryExpr {("*" | "/" | "%") UnaryExpr};
UnaryExpr     ::= ["-" | "!"] Value;
Value         ::= INTEGER
                | IDENT
                | FunctionCall
                | "(" Expression ")";
FunctionCall  ::= IDENT "(" [Args] ")";
Args          ::= Expression {"," Expression};
```

