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

| state | letter | `\d` | \. | [eE] | [+-] | \*  | /   | =  | `<` | `>` | !  | \⏐ | \& | `\` | [bfnrt'] | `"` | `[{}()\[\];,]` | [^\S\r\n] | [\r\n] |
|-------|--------|------|----|------|------|-----|-----|----|-----|-----|----|----|----|-----|----------|-----|----------------|----|-----|
| 0     | 1      | 2    | 3_ |      | 8    | 8   | 22  | 9  | 10  | 11  | 12 | 13 | 14 | 17  |          | 18  |                |    |     |
| 1     | 1      | 1    |    |      |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 2     |        | 2    | 3  | 5    |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 3     |        | 4    |    | 5    |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 3_    |        | 4    |    |      |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 4     |        | 4    |    | 5    |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 5     |        | 7    |    |      | 6    |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 6     |        | 7    |    |      |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 7     |        | 7    |    |      |      |     |     |    |     |     |    |    |    |     |          |     |                |    |     |
| 9     |        |      |    |      |      |     |     | eq |     |     |    |    |    |     |          |     |                |    |     |
| 10    |        |      |    |      |      |     |     | le |     |     |    |    |    |     |          |     |                |    |     |
| 11    |        |      |    |      |      |     |     | ge |     |     |    |    |    |     |          |     |                |    |     |
| 12    |        |      |    |      |      |     |     | ne |     |     |    |    |    |     |          |     |                |    |     |
| 13    |        |      |    |      |      |     |     | ne |     |     |    | 15 |    |     |          |     |                |    |     |
| 14    |        |      |    |      |      |     |     | ne |     |     |    |    | 16 |     |          |     |                |    |     |
| 17    |        |      |    |      |      |     |     | ne |     |     |    |    |    | esc | esc      | esc |                |    |     |
| 18    | 18     | 18   | 18 |      | 18   | 18  | 18  | 18 | 18  | 18  | 18 | 18 | 18 | 19  |          | 20  | 18             | 18 | err |
| 19    |        |      |    |      |      |     |     |    |     |     |    |    |    | 18  | 18       | 18  |                |    |     |
| 22    |        |      |    |      |      | 23  | 24  |    |     |     |    |    |    |     |          |     |                |    |     |
| 23    | 23     | 23   | 23 | 23   | 23   | 23_ | 23  | 23 | 23  | 23  | 23 | 23 | 23 | 23  | 23       | 23  | 23             | 23 | 23  |
| 23_   | 23     | 23   | 23 | 23   | 23   | 23_ | cc  | 23 | 23  | 23  | 23 | 23 | 23 | 23  | 23       | 23  | 23             | 23 | 23  |
| 24    | 24     | 24   | 24 | 24   | 24   | 24  | 24  | 24 | 24  | 24  | 24 | 24 | 24 | 24  | 24       | 24  | 24             | 24 |     |

| starting state |
|----------------|
| 0              |

| ending states | state name | is ignored |
|---------------|------------|------------|
| 1             | `identifier_keyword` | 0 |
| 2             | `int_literal` | 0 |
| 3             | `float_literal` | 0 |
| 4             | `float_literal` | 0 |
| 7             | `float_literal` | 0 |
| 8             | `math_op` | 0 |
| 9             | `assign_op` | 0 |
| 10            | `lt_op` | 0 |
| 11            | `gt_op` | 0 |
| 12            | `not_op` | 0 |
| eq            | `eq_op` | 0 |
| le            | `le_op` | 0 |
| ge            | `ge_op` | 0 |
| ne            | `ne_op` | 0 |
| 15            | `bool_or_op` | 0 |
| 16            | `bool_and_op` | 0 |
| esc           | `escape_sequence` | 0 |
| 20            | `string_literal` | 0 |
| 21            | `separator` | 1 |
| cc            | `multiline_comment` | 0 |
| 24            | `inline_comment` | 0 |

### note

- Transition table chỉ liệt kê những node có cung ra trên đồ thị chuyển.
- Những trạng thái dẫn đến lỗi sẽ được ghi là `err` trên transition table.

