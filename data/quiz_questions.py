"""Standalone quiz questions database."""

QUIZ_DATABASE = {
    "Python Basics": {
        "difficulty": "Beginner",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "What is the correct way to create a list in Python?",
                "options": [
                    "list = []",
                    "list = ()",
                    "list = {}",
                    "list = <>"
                ],
                "correct_answer": "list = []",
                "explanation": "Square brackets [] are used to create lists in Python. Parentheses () create tuples, and curly braces {} create dictionaries or sets."
            },
            {
                "type": "multiple_choice",
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "function",
                    "def",
                    "func",
                    "define"
                ],
                "correct_answer": "def",
                "explanation": "The 'def' keyword is used to define functions in Python. Example: def my_function():"
            },
            {
                "type": "multiple_choice",
                "question": "What does the len() function do?",
                "options": [
                    "Returns the length of an object",
                    "Converts to lowercase",
                    "Sorts a list",
                    "Removes duplicates"
                ],
                "correct_answer": "Returns the length of an object",
                "explanation": "len() returns the number of items in an object like a list, string, tuple, or dictionary."
            },
            {
                "type": "multiple_choice",
                "question": "Which of these is NOT a valid Python data type?",
                "options": [
                    "int",
                    "float",
                    "char",
                    "str"
                ],
                "correct_answer": "char",
                "explanation": "Python doesn't have a 'char' data type. Single characters are represented as strings of length 1."
            },
            {
                "type": "multiple_choice",
                "question": "What is the output of: print(2 ** 3)?",
                "options": [
                    "6",
                    "8",
                    "9",
                    "23"
                ],
                "correct_answer": "8",
                "explanation": "The ** operator is the exponentiation operator in Python. 2 ** 3 means 2 to the power of 3, which equals 8."
            }
        ]
    },
    
    "JavaScript Fundamentals": {
        "difficulty": "Beginner",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "What is the correct way to declare a variable in modern JavaScript?",
                "options": [
                    "var x = 5",
                    "let x = 5",
                    "const x = 5",
                    "Both let and const"
                ],
                "correct_answer": "Both let and const",
                "explanation": "Modern JavaScript uses 'let' for variables that can be reassigned and 'const' for constants. 'var' is outdated."
            },
            {
                "type": "multiple_choice",
                "question": "What does === check in JavaScript?",
                "options": [
                    "Value only",
                    "Type only",
                    "Both value and type",
                    "Reference only"
                ],
                "correct_answer": "Both value and type",
                "explanation": "=== is the strict equality operator that checks both value and type. == only checks value after type coercion."
            },
            {
                "type": "multiple_choice",
                "question": "Which method adds an element to the end of an array?",
                "options": [
                    "push()",
                    "pop()",
                    "shift()",
                    "unshift()"
                ],
                "correct_answer": "push()",
                "explanation": "push() adds elements to the end of an array. pop() removes from the end, shift() removes from the beginning, and unshift() adds to the beginning."
            },
            {
                "type": "multiple_choice",
                "question": "What is a closure in JavaScript?",
                "options": [
                    "A function that closes the browser",
                    "A function with access to outer scope variables",
                    "A way to close files",
                    "A type of loop"
                ],
                "correct_answer": "A function with access to outer scope variables",
                "explanation": "A closure is a function that has access to variables in its outer (enclosing) function's scope, even after the outer function has returned."
            },
            {
                "type": "multiple_choice",
                "question": "What does JSON stand for?",
                "options": [
                    "JavaScript Object Notation",
                    "Java Standard Object Notation",
                    "JavaScript Online Network",
                    "Java Syntax Object Notation"
                ],
                "correct_answer": "JavaScript Object Notation",
                "explanation": "JSON (JavaScript Object Notation) is a lightweight data interchange format that's easy for humans to read and write."
            }
        ]
    },
    
    "React Basics": {
        "difficulty": "Intermediate",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "What is the purpose of useState in React?",
                "options": [
                    "To manage component state",
                    "To fetch data from APIs",
                    "To style components",
                    "To handle routing"
                ],
                "correct_answer": "To manage component state",
                "explanation": "useState is a React Hook that lets you add state to functional components. It returns a state value and a function to update it."
            },
            {
                "type": "multiple_choice",
                "question": "What does useEffect do?",
                "options": [
                    "Performs side effects in functional components",
                    "Creates visual effects",
                    "Manages state",
                    "Handles events"
                ],
                "correct_answer": "Performs side effects in functional components",
                "explanation": "useEffect lets you perform side effects like data fetching, subscriptions, or manually changing the DOM in functional components."
            },
            {
                "type": "multiple_choice",
                "question": "What is JSX?",
                "options": [
                    "A JavaScript extension",
                    "A syntax extension for JavaScript",
                    "A new programming language",
                    "A CSS framework"
                ],
                "correct_answer": "A syntax extension for JavaScript",
                "explanation": "JSX is a syntax extension for JavaScript that lets you write HTML-like code in your JavaScript files. It gets compiled to regular JavaScript."
            },
            {
                "type": "multiple_choice",
                "question": "What is the virtual DOM?",
                "options": [
                    "A lightweight copy of the real DOM",
                    "A database",
                    "A server",
                    "A CSS framework"
                ],
                "correct_answer": "A lightweight copy of the real DOM",
                "explanation": "The virtual DOM is a lightweight copy of the actual DOM. React uses it to optimize updates by comparing changes before updating the real DOM."
            },
            {
                "type": "multiple_choice",
                "question": "What are props in React?",
                "options": [
                    "Properties passed from parent to child components",
                    "CSS properties",
                    "Database properties",
                    "Server properties"
                ],
                "correct_answer": "Properties passed from parent to child components",
                "explanation": "Props (properties) are read-only data passed from parent components to child components. They allow components to be reusable and configurable."
            }
        ]
    },
    
    "Data Structures": {
        "difficulty": "Intermediate",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "What is the time complexity of binary search?",
                "options": [
                    "O(n)",
                    "O(log n)",
                    "O(n²)",
                    "O(1)"
                ],
                "correct_answer": "O(log n)",
                "explanation": "Binary search has O(log n) time complexity because it divides the search space in half with each iteration."
            },
            {
                "type": "multiple_choice",
                "question": "Which data structure uses LIFO (Last In First Out)?",
                "options": [
                    "Queue",
                    "Stack",
                    "Array",
                    "Tree"
                ],
                "correct_answer": "Stack",
                "explanation": "A stack follows the LIFO principle where the last element added is the first one to be removed, like a stack of plates."
            },
            {
                "type": "multiple_choice",
                "question": "What is a hash table?",
                "options": [
                    "A data structure that maps keys to values",
                    "A type of array",
                    "A sorting algorithm",
                    "A tree structure"
                ],
                "correct_answer": "A data structure that maps keys to values",
                "explanation": "A hash table uses a hash function to compute an index into an array of buckets, providing fast O(1) average-case lookups."
            },
            {
                "type": "multiple_choice",
                "question": "What is the main advantage of a linked list over an array?",
                "options": [
                    "Faster random access",
                    "Dynamic size and efficient insertions/deletions",
                    "Less memory usage",
                    "Better cache performance"
                ],
                "correct_answer": "Dynamic size and efficient insertions/deletions",
                "explanation": "Linked lists can grow/shrink dynamically and allow O(1) insertions/deletions at known positions, unlike arrays which require shifting elements."
            },
            {
                "type": "multiple_choice",
                "question": "In a binary tree, what is a leaf node?",
                "options": [
                    "The root node",
                    "A node with no children",
                    "A node with one child",
                    "The parent node"
                ],
                "correct_answer": "A node with no children",
                "explanation": "A leaf node (or terminal node) is a node that has no children - it's at the end of a branch in the tree."
            }
        ]
    },
    
    "SQL Basics": {
        "difficulty": "Beginner",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "Which SQL statement is used to retrieve data from a database?",
                "options": [
                    "GET",
                    "SELECT",
                    "RETRIEVE",
                    "FETCH"
                ],
                "correct_answer": "SELECT",
                "explanation": "SELECT is the SQL statement used to query and retrieve data from database tables."
            },
            {
                "type": "multiple_choice",
                "question": "What does the WHERE clause do?",
                "options": [
                    "Sorts results",
                    "Filters results based on conditions",
                    "Joins tables",
                    "Groups results"
                ],
                "correct_answer": "Filters results based on conditions",
                "explanation": "The WHERE clause filters records based on specified conditions, returning only rows that meet the criteria."
            },
            {
                "type": "multiple_choice",
                "question": "Which JOIN returns all records from both tables?",
                "options": [
                    "INNER JOIN",
                    "LEFT JOIN",
                    "RIGHT JOIN",
                    "FULL OUTER JOIN"
                ],
                "correct_answer": "FULL OUTER JOIN",
                "explanation": "FULL OUTER JOIN returns all records from both tables, with NULL values where there's no match."
            },
            {
                "type": "multiple_choice",
                "question": "What is a primary key?",
                "options": [
                    "A unique identifier for each record",
                    "The first column in a table",
                    "A foreign key reference",
                    "An index"
                ],
                "correct_answer": "A unique identifier for each record",
                "explanation": "A primary key uniquely identifies each record in a table and cannot contain NULL values."
            },
            {
                "type": "multiple_choice",
                "question": "Which SQL function counts the number of rows?",
                "options": [
                    "SUM()",
                    "COUNT()",
                    "TOTAL()",
                    "NUMBER()"
                ],
                "correct_answer": "COUNT()",
                "explanation": "COUNT() is an aggregate function that returns the number of rows that match a specified criterion."
            }
        ]
    },
    
    "Git & Version Control": {
        "difficulty": "Beginner",
        "questions": [
            {
                "type": "multiple_choice",
                "question": "What command creates a new Git repository?",
                "options": [
                    "git create",
                    "git init",
                    "git start",
                    "git new"
                ],
                "correct_answer": "git init",
                "explanation": "git init initializes a new Git repository in the current directory, creating a .git folder."
            },
            {
                "type": "multiple_choice",
                "question": "What does 'git clone' do?",
                "options": [
                    "Creates a copy of a repository",
                    "Deletes a repository",
                    "Renames a repository",
                    "Merges repositories"
                ],
                "correct_answer": "Creates a copy of a repository",
                "explanation": "git clone creates a local copy of a remote repository, including all files, branches, and commit history."
            },
            {
                "type": "multiple_choice",
                "question": "What is a commit in Git?",
                "options": [
                    "A snapshot of changes",
                    "A branch",
                    "A remote repository",
                    "A merge conflict"
                ],
                "correct_answer": "A snapshot of changes",
                "explanation": "A commit is a snapshot of your repository at a specific point in time, recording changes with a unique ID and message."
            },
            {
                "type": "multiple_choice",
                "question": "What does 'git pull' do?",
                "options": [
                    "Fetches and merges changes from remote",
                    "Pushes changes to remote",
                    "Creates a new branch",
                    "Deletes a branch"
                ],
                "correct_answer": "Fetches and merges changes from remote",
                "explanation": "git pull fetches changes from a remote repository and automatically merges them into your current branch."
            },
            {
                "type": "multiple_choice",
                "question": "What is a branch in Git?",
                "options": [
                    "An independent line of development",
                    "A commit message",
                    "A remote repository",
                    "A merge conflict"
                ],
                "correct_answer": "An independent line of development",
                "explanation": "A branch is a separate line of development that allows you to work on features without affecting the main codebase."
            }
        ]
    }
}
