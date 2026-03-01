%{
    /* Lexical analyzer for var declaration */
%}

%%
"var"                     { return VAR; }
"integer66"               { return INTEGER; }
"real66"                  { return REAL; }
"boolean66"               { return BOOLEAN; }
"char66"                  { return CHAR; }
[a-zA-Z_][a-zA-Z_0-9]*    { return IDENTIFIER; }
":"                       { return COLON; }
","                       { return COMMA; }
"2"                       { return SEPARATOR; }
%%
int yywrap() { return 1; }