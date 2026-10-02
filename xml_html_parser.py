import tkinter as tk
from tkinter import ttk
import re


# ============================================================
# CONTEXT-FREE GRAMMAR
# ============================================================

CFG_TEXT = """Document → Element

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
"""


# ============================================================
# ALLOWED TAGS
# ============================================================

ALLOWED_TAGS = {
    "html",
    "head",
    "title",
    "body",
    "div",
    "p",
    "h1"
}


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = {

    "TC01 - Correct HTML":
"""<html>
<body>
<p>Hello World</p>
</body>
</html>""",

    "TC02 - Nested DIV and P":
"""<div>
<p>Hello</p>
</div>""",

    "TC03 - Incorrect Nesting":
"""<div>
<p>Hello</div>
</p>""",

    "TC04 - Missing Closing Tag":
"""<html>
<body>
<p>Hello
</body>
</html>""",

    "TC05 - Unexpected Closing Tag":
"""</div>""",

    "TC06 - Unsupported Tag":
"""<xyz>
Hello
</xyz>""",

    "TC07 - Deep Nesting":
"""<html>
<body>
<div>
<div>
<p>Deep Content</p>
</div>
</div>
</body>
</html>""",

    "TC08 - Mismatched Closing Tag":
"""<body>
<div>
<p>Hello</div>
</p>
</body>""",

    "TC09 - Head and Body":
"""<html>
<head>
<title>Test Page</title>
</head>
<body>
<p>Welcome</p>
</body>
</html>""",

    "TC10 - Empty Document":
""" """
}


# ============================================================
# EXPECTED RESULTS
# ============================================================

EXPECTED_RESULTS = {

    "TC01 - Correct HTML": "VALID",
    "TC02 - Nested DIV and P": "VALID",
    "TC03 - Incorrect Nesting": "INVALID",
    "TC04 - Missing Closing Tag": "INVALID",
    "TC05 - Unexpected Closing Tag": "INVALID",
    "TC06 - Unsupported Tag": "INVALID",
    "TC07 - Deep Nesting": "VALID",
    "TC08 - Mismatched Closing Tag": "INVALID",
    "TC09 - Head and Body": "VALID",
    "TC10 - Empty Document": "INVALID"
}


# ============================================================
# TOKENIZER
# ============================================================

def tokenize(document):

    pattern = r"</?[a-zA-Z][a-zA-Z0-9]*>|[^<>]+"

    matches = re.findall(
        pattern,
        document
    )

    tokens = []

    for item in matches:

        item = item.strip()

        if item != "":
            tokens.append(item)

    return tokens


# ============================================================
# PARSER
# ============================================================

def parse_document(document):

    tokens = tokenize(document)

    stack = []
    trace = []

    opening_tags = 0
    closing_tags = 0
    text_tokens = 0
    maximum_stack_depth = 0

    error_message = ""

    # --------------------------------------------------------
    # Empty document
    # --------------------------------------------------------

    if len(tokens) == 0:

        return {
            "valid": False,
            "tokens": [],
            "trace": [
                "ERROR → Empty document"
            ],
            "stack": [],
            "error": "Document is empty.",
            "opening_tags": 0,
            "closing_tags": 0,
            "text_tokens": 0,
            "maximum_stack_depth": 0
        }


    # ========================================================
    # PROCESS TOKENS
    # ========================================================

    for token in tokens:

        # ----------------------------------------------------
        # Opening tag
        # ----------------------------------------------------

        if re.fullmatch(
            r"<[a-zA-Z][a-zA-Z0-9]*>",
            token
        ):

            tag_name = token[1:-1].lower()

            # Unsupported tag
            if tag_name not in ALLOWED_TAGS:

                trace.append(
                    f"ERROR → Unsupported tag <{tag_name}>"
                )

                error_message = (
                    f"Unsupported tag: <{tag_name}>"
                )

                return {
                    "valid": False,
                    "tokens": tokens,
                    "trace": trace,
                    "stack": stack,
                    "error": error_message,
                    "opening_tags": opening_tags,
                    "closing_tags": closing_tags,
                    "text_tokens": text_tokens,
                    "maximum_stack_depth": maximum_stack_depth
                }


            opening_tags += 1

            # PUSH
            stack.append(tag_name)


            # Maximum stack depth
            if len(stack) > maximum_stack_depth:
                maximum_stack_depth = len(stack)


            trace.append(
                f"PUSH {tag_name} → {stack}"
            )


        # ----------------------------------------------------
        # Closing tag
        # ----------------------------------------------------

        elif re.fullmatch(
            r"</[a-zA-Z][a-zA-Z0-9]*>",
            token
        ):

            tag_name = token[2:-1].lower()

            closing_tags += 1


            # Closing tag when stack is empty
            if len(stack) == 0:

                trace.append(
                    f"ERROR → Unexpected closing tag </{tag_name}>"
                )

                error_message = (
                    f"Unexpected closing tag: </{tag_name}>"
                )

                return {
                    "valid": False,
                    "tokens": tokens,
                    "trace": trace,
                    "stack": stack,
                    "error": error_message,
                    "opening_tags": opening_tags,
                    "closing_tags": closing_tags,
                    "text_tokens": text_tokens,
                    "maximum_stack_depth": maximum_stack_depth
                }


            # Top of stack
            top = stack[-1]


            # Mismatch
            if top != tag_name:

                trace.append(
                    f"ERROR → Expected </{top}> "
                    f"but found </{tag_name}>"
                )

                error_message = (
                    f"Mismatched closing tag. "
                    f"Expected </{top}> "
                    f"but found </{tag_name}>."
                )

                return {
                    "valid": False,
                    "tokens": tokens,
                    "trace": trace,
                    "stack": stack,
                    "error": error_message,
                    "opening_tags": opening_tags,
                    "closing_tags": closing_tags,
                    "text_tokens": text_tokens,
                    "maximum_stack_depth": maximum_stack_depth
                }


            # POP
            stack.pop()

            trace.append(
                f"POP {tag_name} → {stack}"
            )


        # ----------------------------------------------------
        # Text
        # ----------------------------------------------------

        else:

            text_tokens += 1

            trace.append(
                f"TEXT → {token}"
            )


    # ========================================================
    # FINAL STACK CHECK
    # ========================================================

    if len(stack) == 0:

        trace.append(
            "FINAL STACK → EMPTY"
        )

        return {
            "valid": True,
            "tokens": tokens,
            "trace": trace,
            "stack": stack,
            "error": "",
            "opening_tags": opening_tags,
            "closing_tags": closing_tags,
            "text_tokens": text_tokens,
            "maximum_stack_depth": maximum_stack_depth
        }


    else:

        trace.append(
            f"ERROR → Unclosed tags remain: {stack}"
        )

        error_message = (
            f"Unclosed tag(s): {', '.join(stack)}"
        )

        return {
            "valid": False,
            "tokens": tokens,
            "trace": trace,
            "stack": stack,
            "error": error_message,
            "opening_tags": opening_tags,
            "closing_tags": closing_tags,
            "text_tokens": text_tokens,
            "maximum_stack_depth": maximum_stack_depth
        }


# ============================================================
# GUI APPLICATION
# ============================================================

class XMLHTMLParserApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "XML / HTML PARSER - Context-Free Grammar"
        )

        self.root.geometry(
            "1250x850"
        )

        self.root.minsize(
            1100,
            750
        )


        # ====================================================
        # TITLE
        # ====================================================

        title = tk.Label(
            root,
            text="XML / HTML PARSER",
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(12, 2)
        )


        subtitle = tk.Label(
            root,
            text="Context-Free Grammar + Stack-Based Validation",
            font=("Arial", 11)
        )

        subtitle.pack(
            pady=(0, 10)
        )


        # ====================================================
        # NOTEBOOK
        # ====================================================

        self.notebook = ttk.Notebook(
            root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )


        # ====================================================
        # PARSER TAB
        # ====================================================

        self.parser_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.parser_tab,
            text="  Parser  "
        )

        self.create_parser_tab()


        # ====================================================
        # RESULTS TAB
        # ====================================================

        self.results_tab = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.results_tab,
            text="  Test Results  "
        )

        self.create_results_tab()


        # ====================================================
        # STATUS BAR
        # ====================================================

        self.status_label = tk.Label(
            root,
            text="Ready",
            anchor="w",
            font=("Arial", 9)
        )

        self.status_label.pack(
            fill="x",
            padx=15,
            pady=(0, 8)
        )


        # Default example
        self.load_example()


    # ========================================================
    # PARSER TAB
    # ========================================================

    def create_parser_tab(self):

        main_frame = tk.Frame(
            self.parser_tab
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        # ====================================================
        # LEFT SIDE
        # ====================================================

        left_frame = tk.Frame(
            main_frame
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )


        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        input_label = tk.Label(
            left_frame,
            text="XML / HTML DOCUMENT",
            font=("Arial", 11, "bold")
        )

        input_label.pack(
            anchor="w",
            pady=(0, 5)
        )


        self.input_text = tk.Text(
            left_frame,
            height=14,
            font=("Consolas", 11),
            wrap="none"
        )

        self.input_text.pack(
            fill="x",
            pady=(0, 10)
        )


        # ====================================================
        # TEST CASE
        # ====================================================

        test_frame = tk.Frame(
            left_frame
        )

        test_frame.pack(
            fill="x",
            pady=(0, 10)
        )


        test_label = tk.Label(
            test_frame,
            text="Test Case:",
            font=("Arial", 10, "bold")
        )

        test_label.pack(
            side="left",
            padx=(0, 5)
        )


        self.test_case_var = tk.StringVar()


        self.test_case_combo = tk.OptionMenu(
            test_frame,
            self.test_case_var,
            *TEST_CASES.keys()
        )

        self.test_case_combo.config(
            font=("Arial", 10),
            width=27
        )

        self.test_case_combo.pack(
            side="left",
            padx=5
        )


        load_test_button = tk.Button(
            test_frame,
            text="LOAD TEST CASE",
            font=("Arial", 10, "bold"),
            command=self.load_test_case
        )

        load_test_button.pack(
            side="left",
            padx=5
        )


        self.test_case_var.set(
            "TC01 - Correct HTML"
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            left_frame
        )

        button_frame.pack(
            fill="x",
            pady=(0, 10)
        )


        parse_button = tk.Button(
            button_frame,
            text="PARSE DOCUMENT",
            font=("Arial", 10, "bold"),
            command=self.parse
        )

        parse_button.pack(
            side="left",
            padx=(0, 5)
        )


        example_button = tk.Button(
            button_frame,
            text="LOAD EXAMPLE",
            font=("Arial", 10, "bold"),
            command=self.load_example
        )

        example_button.pack(
            side="left",
            padx=5
        )


        clear_button = tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 10, "bold"),
            command=self.clear_all
        )

        clear_button.pack(
            side="left",
            padx=5
        )


        # ====================================================
        # TOKENS
        # ====================================================

        token_label = tk.Label(
            left_frame,
            text="TOKENS",
            font=("Arial", 11, "bold")
        )

        token_label.pack(
            anchor="w",
            pady=(5, 5)
        )


        self.token_list = tk.Listbox(
            left_frame,
            height=8,
            font=("Consolas", 10)
        )

        self.token_list.pack(
            fill="both",
            expand=True,
            pady=(0, 8)
        )


        # ====================================================
        # CURRENT STACK
        # ====================================================

        stack_label = tk.Label(
            left_frame,
            text="CURRENT STACK",
            font=("Arial", 11, "bold")
        )

        stack_label.pack(
            anchor="w",
            pady=(3, 5)
        )


        self.stack_display = tk.Label(
            left_frame,
            text="[]",
            font=("Consolas", 11),
            anchor="w",
            relief="sunken",
            padx=8,
            pady=6
        )

        self.stack_display.pack(
            fill="x"
        )


        # ====================================================
        # RIGHT SIDE
        # ====================================================

        right_frame = tk.Frame(
            main_frame
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )


        # ====================================================
        # CFG
        # ====================================================

        cfg_label = tk.Label(
            right_frame,
            text="CONTEXT-FREE GRAMMAR",
            font=("Arial", 11, "bold")
        )

        cfg_label.pack(
            anchor="w",
            pady=(0, 5)
        )


        self.cfg_text = tk.Text(
            right_frame,
            height=14,
            font=("Consolas", 10),
            wrap="none"
        )

        self.cfg_text.pack(
            fill="x",
            pady=(0, 10)
        )


        self.cfg_text.insert(
            "1.0",
            CFG_TEXT
        )

        self.cfg_text.config(
            state="disabled"
        )


        # ====================================================
        # TRACE
        # ====================================================

        trace_label = tk.Label(
            right_frame,
            text="PARSING TRACE / STACK OPERATIONS",
            font=("Arial", 11, "bold")
        )

        trace_label.pack(
            anchor="w",
            pady=(5, 5)
        )


        self.trace_text = tk.Text(
            right_frame,
            height=11,
            font=("Consolas", 10),
            wrap="none"
        )

        self.trace_text.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )


        # ====================================================
        # STATISTICS
        # ====================================================

        stats_label = tk.Label(
            right_frame,
            text="PARSER STATISTICS",
            font=("Arial", 11, "bold")
        )

        stats_label.pack(
            anchor="w",
            pady=(2, 5)
        )


        stats_frame = tk.Frame(
            right_frame,
            relief="groove",
            borderwidth=2
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 8)
        )


        self.stats_label = tk.Label(
            stats_frame,
            text=(
                "Total Tokens       : 0\n"
                "Opening Tags      : 0\n"
                "Closing Tags      : 0\n"
                "Text Tokens       : 0\n"
                "Maximum Stack Depth : 0"
            ),
            font=("Consolas", 10),
            justify="left",
            anchor="w",
            padx=10,
            pady=7
        )

        self.stats_label.pack(
            fill="x"
        )


        # ====================================================
        # ERROR DETAILS
        # ====================================================

        self.error_label = tk.Label(
            right_frame,
            text="",
            font=("Arial", 9),
            anchor="w",
            justify="left"
        )

        self.error_label.pack(
            fill="x",
            pady=(0, 5)
        )


        # ====================================================
        # RESULT
        # ====================================================

        result_frame = tk.Frame(
            right_frame,
            relief="groove",
            borderwidth=2
        )

        result_frame.pack(
            fill="x"
        )


        self.result_label = tk.Label(
            result_frame,
            text="RESULT: NOT PARSED",
            font=("Arial", 13, "bold"),
            pady=8
        )

        self.result_label.pack()


    # ========================================================
    # RESULTS TAB
    # ========================================================

    def create_results_tab(self):

        heading = tk.Label(
            self.results_tab,
            text="AUTOMATIC TEST CASE EVALUATION",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=(20, 5)
        )


        description = tk.Label(
            self.results_tab,
            text=(
                "All predefined test cases are automatically "
                "validated using the CFG and stack-based parser."
            ),
            font=("Arial", 10)
        )

        description.pack(
            pady=(0, 15)
        )


        # ====================================================
        # RUN BUTTON
        # ====================================================

        run_button = tk.Button(
            self.results_tab,
            text="RUN ALL TEST CASES",
            font=("Arial", 11, "bold"),
            command=self.run_all_tests
        )

        run_button.pack(
            pady=(0, 15)
        )


        # ====================================================
        # TABLE
        # ====================================================

        table_frame = tk.Frame(
            self.results_tab
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )


        columns = (
            "testcase",
            "expected",
            "actual",
            "status"
        )


        self.results_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )


        self.results_table.heading(
            "testcase",
            text="Test Case"
        )

        self.results_table.heading(
            "expected",
            text="Expected"
        )

        self.results_table.heading(
            "actual",
            text="Actual"
        )

        self.results_table.heading(
            "status",
            text="Status"
        )


        self.results_table.column(
            "testcase",
            width=320,
            anchor="center"
        )

        self.results_table.column(
            "expected",
            width=150,
            anchor="center"
        )

        self.results_table.column(
            "actual",
            width=150,
            anchor="center"
        )

        self.results_table.column(
            "status",
            width=150,
            anchor="center"
        )


        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.results_table.yview
        )


        self.results_table.configure(
            yscrollcommand=scrollbar.set
        )


        self.results_table.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        summary_frame = tk.Frame(
            self.results_tab,
            relief="groove",
            borderwidth=2
        )

        summary_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )


        self.total_label = tk.Label(
            summary_frame,
            text="TOTAL TEST CASES : 0",
            font=("Arial", 11, "bold")
        )

        self.total_label.pack(
            pady=3
        )


        self.passed_label = tk.Label(
            summary_frame,
            text="PASSED           : 0",
            font=("Arial", 11, "bold")
        )

        self.passed_label.pack(
            pady=3
        )


        self.failed_label = tk.Label(
            summary_frame,
            text="FAILED           : 0",
            font=("Arial", 11, "bold")
        )

        self.failed_label.pack(
            pady=3
        )


        self.accuracy_label = tk.Label(
            summary_frame,
            text="ACCURACY         : 0%",
            font=("Arial", 11, "bold")
        )

        self.accuracy_label.pack(
            pady=3
        )


    # ========================================================
    # LOAD TEST CASE
    # ========================================================

    def load_test_case(self):

        selected_case = self.test_case_var.get()


        if selected_case not in TEST_CASES:
            return


        document = TEST_CASES[
            selected_case
        ]


        self.input_text.delete(
            "1.0",
            tk.END
        )


        self.input_text.insert(
            "1.0",
            document
        )


        self.clear_output()


        self.status_label.config(
            text=f"Loaded: {selected_case}"
        )


        self.notebook.select(
            self.parser_tab
        )


    # ========================================================
    # LOAD EXAMPLE
    # ========================================================

    def load_example(self):

        example = """<html>
<head>
<title>My Page</title>
</head>
<body>
<div>
<h1>Welcome</h1>
<p>Hello World</p>
</div>
</body>
</html>"""


        self.input_text.delete(
            "1.0",
            tk.END
        )


        self.input_text.insert(
            "1.0",
            example
        )


        self.clear_output()


        self.status_label.config(
            text="Example document loaded"
        )


    # ========================================================
    # PARSE DOCUMENT
    # ========================================================

    def parse(self):

        document = self.input_text.get(
            "1.0",
            tk.END
        ).strip()


        self.clear_output()


        if document == "":

            self.result_label.config(
                text="RESULT: INVALID"
            )


            self.error_label.config(
                text="ERROR: Document is empty."
            )


            self.trace_text.insert(
                tk.END,
                "ERROR → Empty document\n"
            )


            self.status_label.config(
                text="Error: Document is empty."
            )

            return


        # Parse
        result = parse_document(
            document
        )


        # ====================================================
        # TOKENS
        # ====================================================

        for index, token in enumerate(
            result["tokens"],
            start=1
        ):

            self.token_list.insert(
                tk.END,
                f"{index}. {token}"
            )


        # ====================================================
        # TRACE
        # ====================================================

        for line in result["trace"]:

            self.trace_text.insert(
                tk.END,
                line + "\n"
            )


        # ====================================================
        # CURRENT STACK
        # ====================================================

        self.stack_display.config(
            text=str(
                result["stack"]
            )
        )


        # ====================================================
        # STATISTICS
        # ====================================================

        self.stats_label.config(
            text=(
                f"Total Tokens         : "
                f"{len(result['tokens'])}\n"
                f"Opening Tags        : "
                f"{result['opening_tags']}\n"
                f"Closing Tags        : "
                f"{result['closing_tags']}\n"
                f"Text Tokens         : "
                f"{result['text_tokens']}\n"
                f"Maximum Stack Depth : "
                f"{result['maximum_stack_depth']}"
            )
        )


        # ====================================================
        # RESULT
        # ====================================================

        if result["valid"]:

            self.result_label.config(
                text="RESULT: VALID"
            )


            self.error_label.config(
                text="No errors detected."
            )


            self.status_label.config(
                text=(
                    "Document is VALID according "
                    "to the simplified CFG."
                )
            )


        else:

            self.result_label.config(
                text="RESULT: INVALID"
            )


            self.error_label.config(
                text=f"ERROR: {result['error']}"
            )


            self.status_label.config(
                text="Document validation failed."
            )


    # ========================================================
    # RUN ALL TESTS
    # ========================================================

    def run_all_tests(self):

        # Clear table
        for item in self.results_table.get_children():

            self.results_table.delete(
                item
            )


        passed = 0
        failed = 0


        # ====================================================
        # EVALUATE EACH TEST CASE
        # ====================================================

        for test_case, document in TEST_CASES.items():

            result = parse_document(
                document
            )


            # Actual result
            if result["valid"]:

                actual = "VALID"

            else:

                actual = "INVALID"


            # Expected
            expected = EXPECTED_RESULTS[
                test_case
            ]


            # Compare
            if actual == expected:

                status = "PASS"

                passed += 1

            else:

                status = "FAIL"

                failed += 1


            # Insert
            self.results_table.insert(
                "",
                tk.END,
                values=(
                    test_case,
                    expected,
                    actual,
                    status
                )
            )


        # ====================================================
        # SUMMARY
        # ====================================================

        total = len(
            TEST_CASES
        )


        if total > 0:

            accuracy = (
                passed / total
            ) * 100

        else:

            accuracy = 0


        self.total_label.config(
            text=f"TOTAL TEST CASES : {total}"
        )


        self.passed_label.config(
            text=f"PASSED           : {passed}"
        )


        self.failed_label.config(
            text=f"FAILED           : {failed}"
        )


        self.accuracy_label.config(
            text=f"ACCURACY         : {accuracy:.0f}%"
        )


        self.status_label.config(
            text=(
                f"Automatic evaluation completed: "
                f"{passed}/{total} test cases passed."
            )
        )


        self.notebook.select(
            self.results_tab
        )


    # ========================================================
    # CLEAR OUTPUT
    # ========================================================

    def clear_output(self):

        self.token_list.delete(
            0,
            tk.END
        )


        self.trace_text.delete(
            "1.0",
            tk.END
        )


        self.stack_display.config(
            text="[]"
        )


        self.stats_label.config(
            text=(
                "Total Tokens         : 0\n"
                "Opening Tags        : 0\n"
                "Closing Tags        : 0\n"
                "Text Tokens         : 0\n"
                "Maximum Stack Depth : 0"
            )
        )


        self.error_label.config(
            text=""
        )


        self.result_label.config(
            text="RESULT: NOT PARSED"
        )


    # ========================================================
    # CLEAR EVERYTHING
    # ========================================================

    def clear_all(self):

        self.input_text.delete(
            "1.0",
            tk.END
        )


        self.clear_output()


        self.test_case_var.set(
            "TC01 - Correct HTML"
        )


        self.status_label.config(
            text="All fields cleared"
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = XMLHTMLParserApp(
        root
    )

    root.mainloop()