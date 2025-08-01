# TÜPDİL: Türkçe Programlama DİLim

This project implements a compiler and interpreter for **TÜPDİL (Türkçe Programlama DİLim)**, a Turkish-based programming language developed for educational purposes. The system is capable of parsing and executing TÜPDİL code while detecting both compile-time and runtime errors.

## Overview

The TÜPDİL interpreter processes `.tup` source files written in a simplified Turkish syntax, supporting basic types and operations. The interpreter follows these steps:

1. **Compilation Phase**  
   - Performs syntax and semantic analysis  
   - Reports the first encountered **compile-time error**, if any

2. **Execution Phase**  
   - Executes valid programs line by line  
   - Handles assignments, expressions, control flow (line jumps), and output  
   - Stops execution and reports any **runtime error** encountered

## Supported Statements

- `Programı başlat.` and `Programı bitir.` — Entry and exit points of the program  
- `<var> bir <type> olsun.` — Variable declarations (`tam-sayı`, `reel-sayı`, `metin`)  
- `<var> değeri <expr> olsun.` — Value assignments  
- `<expr> yazdır.` — Output  
- `<expr>. satıra zıpla.` — Control flow (jump to line)  

## Expression Features

- Arithmetic operations: `artı`, `eksi`, `çarp`, `bölü`  
- Parentheses for precedence: `parantez-aç`, `parantez-kapa`  
- Operands may include constants or variables (not mixed in a single expression)  
- Type-specific behaviors and conversions are supported with constraints

## Error Handling

- **Compile-time Errors (CE):**
  - Incorrect syntax or grammar
  - Type mismatches with constant assignments
  - Invalid variable names, types, or keywords
  - Misuse of language-specific symbols or formats

- **Runtime Errors (RTE):**
  - Undefined or uninitialized variables
  - Type mismatches with variables in expressions
  - Out-of-range jumps or values
  - Metin length overflows or numeric precision violations

## Input and Output

- **Input:** Read from `input.tup`
- **Output:** Written to `output.txt`
  - Proper formatting for each data type
  - `metin` strings are printed without exclamation marks
  - Numeric values follow Turkish formatting (e.g., `1.234,0`)

## Notes

- Variable names must use Turkish characters and cannot exceed 20 characters.
- `metin` values are limited to 50 characters.
- Thousands separator: `.` — Decimal separator: `,`
- Re-declaration of variables with a different type is allowed; however, type consistency is required during assignments.
