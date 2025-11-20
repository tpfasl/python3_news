class BaseSummarizer:

    def summarize(self, text: str, max_sentences: int = 3) -> str:
        raise NotImplementedError


class DummySummarizer(BaseSummarizer):
    
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        sentences = text.split(".")
        summary = ". ".join(sentences[:max_sentences]).strip()
        return summary + "..."



class FakeModel:
    def generate(self, text: str, max_sentences: int = 3):
       
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        reversed_sentences = list(reversed(sentences))
        summary = ". ".join(reversed_sentences[:max_sentences])
        return summary + "..."


class ModelSummarizer(BaseSummarizer):
  
    
    def __init__(self, model_path: str = "models/news_summary_model.pt"):
        self.model_path = model_path

       
        self.model = FakeModel()

    def summarize(self, text: str, max_sentences: int = 3) -> str:
       
        return self.model.generate(text, max_sentences=max_sentences)


def get_summarizer(model_ready: bool = False):
    
    if model_ready:
        return ModelSummarizer()
    return DummySummarizer()



if __name__ == "__main__":
    text = "첫 문장입니다. 두 번째 문장입니다. 세 번째 문장입니다. 네 번째 문장입니다."

    print("=== Dummy Summarizer ===")
    s1 = get_summarizer(model_ready=False)
    print(s1.summarize(text))

    print("\n=== Fake Model Summarizer ===")
    s2 = get_summarizer(model_ready=True)
    print(s2.summarize(text))
