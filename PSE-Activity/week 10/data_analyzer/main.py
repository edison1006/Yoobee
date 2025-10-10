from analyzer import DataAnalyzer, DataAnalyzerPrinter

def main():

    # Example with string
    text_input = "Hello World!"
    analyzer1 = DataAnalyzer(text_input)
    DataAnalyzerPrinter.display_results(analyzer1)

    # Example with list
    list_input = ["Hello", "WORLD"]
    analyzer2 = DataAnalyzer(list_input)
    DataAnalyzerPrinter.display_results(analyzer2)

if __name__ == "__main__":
    main()