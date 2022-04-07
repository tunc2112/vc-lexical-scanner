```
delimiter -> "{" | "}" | "(" | ")" | "[" | "]" | ";" | ","

letter -> "A" ... "Z" | "a" ... "z" | "_" // or "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
digit -> "0" ... "9"
escape_sequence -> \\b | \\f | \\n | \\r | \\t | \\' | \\" | \\\\
nonquote_character -> letter | digit

identifier -> letter (letter | digit)*
type_keyword -> boolean | int | float | void
nontype_keyword -> if | else | for | while | break | continue | return
keyword -> type_keyword | nontype_keyword

comp_operator ->  "<" | ">" | ">=" | "<=" | "==" | "!="
binary_ops -> "+" | "-" | "*" | "/" | comp_operator
unary_ops -> "!" | "+" | "-" 

literal -> int_literal | bool_literal | float_literal | string_literal

int_literal -> digit (digit)*
bool_literal -> true | false

float_literal -> digit* . digit+ exponent? | digit+ . | digit+ .? exponent
exponent -> (E | e) (+ | -)? digit+

string_literal -> " (nonquote_character | escape_sequence)* "

Nếu một dòng mới xuất hiện sau dấu mở " và trước dấu đóng ", sẽ có lỗi biên dịch.

comparison -> expression comp_operator expression
bool_expr -> bool_literal | comparison | "!" comparison | comparison ("||" | "&&") comparison

m_expr -> u_expr | m_expr ("*" | "/" | "%") u_expr
a_expr -> m_expr | a_expr ("+" | "-") m_expr
u_expr -> "-" u_expr | "+" u_expr
math_expr -> m_expr | a_expr

expression_list -> expression ("," expression)*
assignment_expression -> identifier = expression
define_expression -> type_keyword assignment_expression ("," assignment_expression)*
expression -> literal | assignment_expression | math_expr | bool_expr | "(" expression ")"

comment -> /\*(^\*)*\*/ | //.*$
```
Các chú thích không lồng vào nhau.

## transition table

In every case, starting state is state 0.

| state | letter | digit | "." | [eE] | [+-] | `=` | `<` | `>` |
|-------|--------|-------|-----|------|------|-----|-----|-----|
| 0     | 1      | 2     | 3_  |      |      | 8   | 9   | 10  |
| 1     | 1      | 1     |     |      |      |     |     |     |
| 2     |        | 2     | 3   |      |      |     |     |     |
| 3     |        | 4     |     | 5    |      |     |     |     |
| 3_    |        | 4     |     |      |      |     |     |     |
| 4     |        | 4     |     | 5    |      |     |     |     |
| 5     |        | 7     |     |      | 6    |     |     |     |
| 6     |        | 7     |     |      |      |     |     |     |
| 7     |        | 7     |     |      |      |     |     |     |
| 8     |        |       |     |      |      | eq  |     |     |
| 9     |        |       |     |      |      | le  |     |     |
| 10    |        |       |     |      |      | ge  |     |     |

| ending states | state name |
|---------------|------------|
| 1             | identifier |
| 2             | int_literal |
| 3             | float_literal_1 |
| 4             | float_literal_2 |
| 7             | float_literal_3 |
| 8             | assign_op |
| 9             | lt_op |
| 10            | gt_op |
| eq            | eq_op |
| le            | le_op |
| ge            | ge_op |
