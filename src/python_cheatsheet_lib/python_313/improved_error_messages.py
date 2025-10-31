"""
Demonstrates Python 3.13's improved error messages and traceback quality.

Python 3.13 introduced significant improvements to error messages,
making debugging easier and more intuitive.
"""

from __future__ import annotations


def demonstrate_error_improvements() -> None:
    """
    Show various error improvements in Python 3.13.

    Why?
    - Better developer experience
    - Faster debugging
    - More informative error messages
    - Clearer indication of error location

    Examples:
        >>> # demonstrate_error_improvements()  # Uncomment to see errors
    """
    print("Python 3.13 Error Message Improvements\n")

    # Example 1: Better attribute error messages
    print("1. Improved AttributeError with suggestions:")
    print("   If you type obj.metod() instead of obj.method(),")
    print("   Python 3.13 will suggest: 'Did you mean: method?'\n")

    # Example 2: Better name error messages
    print("2. Improved NameError with suggestions:")
    print("   If you type 'prnit()' instead of 'print()',")
    print("   Python 3.13 will suggest: 'Did you mean: print?'\n")

    # Example 3: More specific import error messages
    print("3. More specific ImportError messages:")
    print("   Clearer distinction between module not found vs attribute not found\n")

    # Example 4: Better syntax error locations
    print("4. Improved syntax error locations:")
    print("   More precise caret (^) pointing to the exact error location\n")


def demonstrate_traceback_improvements() -> None:
    """
    Demonstrate enhanced traceback readability in Python 3.13.

    Features:
    - Color-coded tracebacks (in supported terminals)
    - Better formatting
    - Clearer error chains

    Examples:
        >>> # This would show improved traceback formatting
        >>> demonstrate_traceback_improvements()
        Traceback improvements are active in Python 3.13+
    """
    print("Python 3.13 Traceback Improvements:")
    print("- Color-coded output in supported terminals")
    print("- Improved formatting for nested exceptions")
    print("- Better indication of error propagation\n")


def example_attribute_suggestion() -> None:
    """
    Example of improved AttributeError with suggestions.

    In Python 3.13, if you mistype an attribute name, you get helpful suggestions.
    """

    class DataProcessor:
        def process_data(self, data: list[int]) -> int:
            return sum(data)

        def validate_data(self, data: list[int]) -> bool:
            return all(isinstance(x, int) for x in data)

    processor = DataProcessor()

    # Correct usage
    result = processor.process_data([1, 2, 3])
    print(f"Correct usage: {result}")

    # Uncomment to see improved error message:
    # processor.proces_data([1, 2, 3])  # Would suggest: Did you mean 'process_data'?


def example_name_suggestion() -> None:
    """
    Example of improved NameError with suggestions.

    Python 3.13 suggests similar variable names when you make a typo.
    """

    def calculate_statistics(data: list[float]) -> dict[str, float]:
        """Calculate basic statistics."""
        total_sum = sum(data)
        count = len(data)
        average = total_sum / count if count > 0 else 0.0

        # Uncomment to see suggestion:
        # return {"sum": total_sum, "count": count, "avg": avarage}  # Suggests 'average'

        return {"sum": total_sum, "count": count, "avg": average}

    stats = calculate_statistics([1.0, 2.0, 3.0, 4.0, 5.0])
    print(f"Statistics: {stats}")


def example_better_syntax_errors() -> None:
    """
    Demonstrate more precise syntax error reporting.

    Python 3.13 shows exact location of syntax errors with improved carets.
    """
    print("Better syntax error location in Python 3.13:")
    print("The error caret (^) now points to the exact problematic token")
    print("rather than just the line.\n")

    # Example of what improved errors look like:
    example_code = """
    # Before Python 3.13:
    # SyntaxError: invalid syntax (whole line highlighted)

    # Python 3.13:
    # SyntaxError: invalid syntax
    #     if x = 5:  # Assignment in condition
    #          ^
    # The caret points exactly at the '=' sign
    """
    print(example_code)


def exception_notes_example() -> None:
    """
    Demonstrate exception notes feature (PEP 678).

    Python 3.11+ allows adding notes to exceptions for additional context.
    This is particularly useful in Python 3.13 with improved error display.

    Examples:
        >>> exception_notes_example()
        Demonstrating exception notes...
    """
    print("Exception Notes Example (PEP 678):")

    try:
        data = [1, 2, "three", 4]
        _total = sum(data)  # type: ignore
    except TypeError as e:
        e.add_note("This error occurred while processing user input")
        e.add_note("Data should contain only numbers")
        print(f"Caught exception: {e}")
        print(f"Notes: {e.__notes__}")


def demonstrate_all() -> None:
    """Run all error message improvement examples."""
    demonstrate_error_improvements()
    print("\n" + "=" * 60 + "\n")

    demonstrate_traceback_improvements()
    print("\n" + "=" * 60 + "\n")

    example_attribute_suggestion()
    print("\n" + "=" * 60 + "\n")

    example_name_suggestion()
    print("\n" + "=" * 60 + "\n")

    example_better_syntax_errors()
    print("\n" + "=" * 60 + "\n")

    exception_notes_example()


if __name__ == "__main__":
    demonstrate_all()
