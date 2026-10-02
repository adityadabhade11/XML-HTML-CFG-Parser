# XML/HTML Parser using Context-Free Grammar

A software-based XML/HTML Parser developed as a Theory of Computation (TOC) case study. The project demonstrates how Context-Free Grammar (CFG) and stack-based parsing can be used to validate the nested structure of XML/HTML documents.

## Project Overview

Markup languages such as XML and HTML use nested tags to organize structured information. A tag must be properly opened and closed, and the nesting order must be maintained.

This project implements a simplified XML/HTML structural parser that:

- Tokenizes XML/HTML input
- Validates supported tags
- Uses a stack to maintain nested tags
- Detects incorrect tag nesting
- Detects missing closing tags
- Detects unexpected closing tags
- Detects unsupported tags
- Displays parsing trace and stack operations
- Calculates parser statistics
- Automatically evaluates predefined test cases

The project is designed for educational demonstration of the relationship between **Context-Free Grammar (CFG)** and **Pushdown Automata (PDA)**.

## Objectives

- To understand the use of Context-Free Grammar for nested structures.
- To implement stack-based tag validation.
- To demonstrate LIFO (Last In, First Out) behavior.
- To identify valid and invalid XML/HTML structures.
- To provide a simple graphical interface for parser demonstration.
- To evaluate the parser using multiple test cases.

## Context-Free Grammar

The simplified grammar used in this project is:

```text
Document → Element

Element → <html> Content </html>
        | <head> Content </head>
        | <title> Text </title>
        | <body> Content </body>
        | <div> Content </div>
        | <p> Text </p>
        | <h1> Text </h1>

Content → Element Content
        | Text Content
        | ε

Text → text
