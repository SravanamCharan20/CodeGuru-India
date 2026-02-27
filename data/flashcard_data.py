"""Standalone flashcard database."""

FLASHCARD_DATABASE = {
    "Python": [
        {
            "front": "What is a list comprehension in Python?",
            "back": "A concise way to create lists. Syntax: [expression for item in iterable if condition]. Example: [x**2 for x in range(10) if x % 2 == 0] creates a list of squares of even numbers.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is the difference between append() and extend()?",
            "back": "append() adds a single element to the end of a list, while extend() adds all elements from an iterable. Example: list.append([1,2]) adds one element (a list), but list.extend([1,2]) adds two elements (1 and 2).",
            "difficulty": "Beginner"
        },
        {
            "front": "What is a decorator in Python?",
            "back": "A function that modifies the behavior of another function. Uses @decorator syntax. Example: @staticmethod, @property. Decorators wrap functions to add functionality before/after execution.",
            "difficulty": "Advanced"
        },
        {
            "front": "What is the difference between is and ==?",
            "back": "'is' checks if two variables point to the same object in memory (identity), while '==' checks if the values are equal. Example: a = [1,2]; b = [1,2]; a == b is True, but a is b is False.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is a lambda function?",
            "back": "An anonymous function defined with lambda keyword. Syntax: lambda arguments: expression. Example: square = lambda x: x**2. Used for short, simple functions.",
            "difficulty": "Beginner"
        }
    ],
    
    "JavaScript": [
        {
            "front": "What is the difference between let, const, and var?",
            "back": "var: function-scoped, can be redeclared. let: block-scoped, cannot be redeclared. const: block-scoped, cannot be reassigned or redeclared. Modern code uses let/const.",
            "difficulty": "Beginner"
        },
        {
            "front": "What is a Promise in JavaScript?",
            "back": "An object representing the eventual completion or failure of an asynchronous operation. Has three states: pending, fulfilled, rejected. Use .then() for success and .catch() for errors.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is the difference between map() and forEach()?",
            "back": "map() creates a new array with transformed elements and returns it. forEach() executes a function for each element but returns undefined. Use map() when you need the result.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is event bubbling?",
            "back": "When an event occurs on an element, it first runs handlers on that element, then on its parent, then all the way up to the document. Can be stopped with event.stopPropagation().",
            "difficulty": "Advanced"
        },
        {
            "front": "What is the spread operator (...)?",
            "back": "Expands an iterable into individual elements. Uses: copying arrays ([...arr]), merging arrays ([...arr1, ...arr2]), function arguments (func(...args)), object cloning ({...obj}).",
            "difficulty": "Intermediate"
        }
    ],
    
    "React": [
        {
            "front": "What is the difference between state and props?",
            "back": "State: mutable data managed within a component, changes trigger re-renders. Props: immutable data passed from parent to child, read-only. State is private, props are public.",
            "difficulty": "Beginner"
        },
        {
            "front": "When does useEffect run?",
            "back": "After every render by default. Control with dependency array: [] runs once on mount, [dep] runs when dep changes, no array runs on every render. Cleanup function runs before unmount.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is the virtual DOM?",
            "back": "A lightweight JavaScript representation of the real DOM. React compares virtual DOM snapshots (diffing) to find minimal changes needed, then updates only those parts of the real DOM (reconciliation).",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is prop drilling?",
            "back": "Passing props through multiple component layers to reach a deeply nested component. Problems: verbose, hard to maintain. Solutions: Context API, state management libraries (Redux, Zustand).",
            "difficulty": "Advanced"
        },
        {
            "front": "What is React.memo()?",
            "back": "A higher-order component that memoizes a component, preventing re-renders if props haven't changed. Use for expensive components. Example: const MemoComponent = React.memo(MyComponent).",
            "difficulty": "Advanced"
        }
    ],
    
    "Data Structures": [
        {
            "front": "What is Big O notation?",
            "back": "A way to describe algorithm efficiency. O(1): constant, O(log n): logarithmic, O(n): linear, O(n log n): linearithmic, O(n²): quadratic. Describes worst-case time/space complexity.",
            "difficulty": "Intermediate"
        },
        {
            "front": "When to use a Stack vs Queue?",
            "back": "Stack (LIFO): undo/redo, function calls, backtracking, expression evaluation. Queue (FIFO): task scheduling, breadth-first search, printer queue, message queues.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is a Binary Search Tree (BST)?",
            "back": "A tree where each node has at most 2 children, left child < parent < right child. Allows O(log n) search, insert, delete in balanced trees. Becomes O(n) if unbalanced.",
            "difficulty": "Advanced"
        },
        {
            "front": "What is the difference between Array and Linked List?",
            "back": "Array: contiguous memory, O(1) access, O(n) insert/delete. Linked List: scattered memory, O(n) access, O(1) insert/delete at known position. Arrays better for access, lists for modifications.",
            "difficulty": "Beginner"
        },
        {
            "front": "What is a Hash Collision?",
            "back": "When two different keys hash to the same index. Solutions: chaining (linked list at each index) or open addressing (find next empty slot). Good hash functions minimize collisions.",
            "difficulty": "Advanced"
        }
    ],
    
    "SQL": [
        {
            "front": "What is the difference between INNER JOIN and LEFT JOIN?",
            "back": "INNER JOIN: returns only matching rows from both tables. LEFT JOIN: returns all rows from left table and matching rows from right (NULL if no match). Use LEFT JOIN to keep all left table data.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is normalization?",
            "back": "Organizing database to reduce redundancy. 1NF: atomic values. 2NF: no partial dependencies. 3NF: no transitive dependencies. Benefits: less redundancy, easier updates, data integrity.",
            "difficulty": "Advanced"
        },
        {
            "front": "What is an index in SQL?",
            "back": "A data structure that improves query speed. Like a book index - helps find data without scanning entire table. Trade-off: faster reads, slower writes. Create on frequently queried columns.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is a transaction?",
            "back": "A sequence of operations treated as a single unit. ACID properties: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent safety), Durability (permanent changes).",
            "difficulty": "Advanced"
        },
        {
            "front": "What is the difference between WHERE and HAVING?",
            "back": "WHERE: filters rows before grouping, cannot use aggregate functions. HAVING: filters groups after GROUP BY, can use aggregate functions. Example: WHERE filters individuals, HAVING filters groups.",
            "difficulty": "Intermediate"
        }
    ],
    
    "Git": [
        {
            "front": "What is the difference between git fetch and git pull?",
            "back": "git fetch: downloads changes from remote but doesn't merge. git pull: downloads and automatically merges (fetch + merge). Use fetch to review changes before merging.",
            "difficulty": "Beginner"
        },
        {
            "front": "What is a merge conflict?",
            "back": "Occurs when Git can't automatically merge changes (same lines modified differently). Resolve by: editing conflicted files, removing conflict markers (<<<<, ====, >>>>), staging, and committing.",
            "difficulty": "Intermediate"
        },
        {
            "front": "What is git rebase?",
            "back": "Moves or combines commits to a new base. Rewrites history for cleaner linear history. Use for local branches. Never rebase public/shared branches. Alternative to merge.",
            "difficulty": "Advanced"
        },
        {
            "front": "What is .gitignore?",
            "back": "A file specifying which files/folders Git should ignore. Common entries: node_modules/, .env, *.log, .DS_Store. Patterns: * (wildcard), / (directory), ! (negate). Must commit .gitignore itself.",
            "difficulty": "Beginner"
        },
        {
            "front": "What is a detached HEAD state?",
            "back": "When HEAD points to a specific commit instead of a branch. Happens when checking out a commit directly. Changes made here are lost unless you create a branch. Use git checkout -b <branch> to save work.",
            "difficulty": "Advanced"
        }
    ]
}
