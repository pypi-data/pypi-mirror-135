import oseti

class OsetiAnalyzer:
    """oseti Japanese text analyzer
    """

    def __init__(self):
        self.analyzer = oseti.Analyzer()

    def analyze(self, text: str) -> float:
        """get negative / positive value

        Args:
            text (str): text to analyze

        Returns:
            float: negative / positive value from -1 to 1
        """
        result = self.analyzer.analyze(text)
        return sum(result) / len(result)