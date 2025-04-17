#[derive(Debug)]
pub enum CommandType
{
    PUSH,
    POP,
    ARITHMETIC,
    LABEL,
    GOTO,
    IF,
    FUNCTION,
    RETURN,
    CALL,
}

// enum ArithInstr
// {
//     ADD,
//     SUB,
//     NEG,
//     EQ,
//     GT,
//     LT,
//     AND,
//     OR,
//     NOT,
// }

// enum MemAccessInstr
// {
//     ARGUMT,
//     LOCAL,
//     STATIC,
//     CONSTANT,
//     THIS,
//     THAT,
//     PTR,
//     TMP
// }