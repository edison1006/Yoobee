"""
analyzer.py

Provides classes for analyzing strings and lists:
- Total length
- Number of uppercase characters
"""

from typing import Union, List


class DataAnalyzer:
    """Base class for analyzing data."""

    def __init__(self, data: Union[str, List[str]]) -> None:
        """
        Initialize with data (string or list of strings).
        :param data: Input data (string or list)
        """
        self.data = data

    def total_length(self) -> int:
        """
        Calculate total length of the data.
        :return: Integer length
        """
        if isinstance(self.data, str):
            return len(self.data)
        if isinstance(self.data, list):
            return sum(len(item) for item in self.data)
        raise TypeError("Data must be a string or a list of strings.")

    def uppercase_count(self) -> int:
        """
        Count uppercase characters in the data.
        :return: Integer count of uppercase letters
        """
        if isinstance(self.data, str):
            return sum(1 for char in self.data if char.isupper())
        if isinstance(self.data, list):
            return sum(
                1 for item in self.data for char in item if char.isupper()
            )
        raise TypeError("Data must be a string or a list of strings.")


class DataAnalyzerPrinter:
    """
    Helper class to print analysis results.
    """

    @staticmethod
    def display_results(analyzer: DataAnalyzer) -> None:
        """
        Display total length and uppercase count.
        :param analyzer: DataAnalyzer instance
        """
        print("=== Data Analysis ===")
        print("Total Length:", analyzer.total_length())
        print("Uppercase Characters:", analyzer.uppercase_count())





