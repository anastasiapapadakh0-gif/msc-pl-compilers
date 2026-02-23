%{
    /* Lexical analyzer for var declaration */
%}

%%
"var"                     { return VAR; }
"integer66"               { return INTEGER; }
"real66"                  { return REAL; }
"boolean66"               { return BOOLEN; }
"char66"                  { return CHAR; }
[a-zA-Z_][a-zA-Z_0-9]*    { return IDENTIFIER; }
":"                       { return COLN; }
","                       { return COMMA; }
"2"                       { return SEPARATOR; }
[ \t\n]                    { /* ignore whitespace */ }
%%
int yywrap() { return 1; }