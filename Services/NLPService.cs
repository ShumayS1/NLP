using Microsoft.ML;
using Microsoft.ML.Data;

public class NLPService
{
    private readonly MLContext _mlContext = new();

    public NLPAnalysisResult AnalyzeText(string text)
    {
        // 1. Анализ тональности (пример с ML.NET)
        var sentiment = AnalyzeSentiment(text);

        // 2. Определение стиля общения
        var communicationStyle = text.Length > 100 ? "Formal" : "Casual";

        // 3. Упрощённое предсказание MBTI
        var personalityType = sentiment > 0.5 ? "EXTJ" : "INFP";

        return new NLPAnalysisResult
        {
            CommunicationStyle = communicationStyle,
            PersonalityType = personalityType,
            SentimentScore = sentiment
        };
    }

    private float AnalyzeSentiment(string text)
    {
        // Заглушка: в реальности используйте обученную модель
        return text.Contains("great") ? 0.9f : 0.2f;
    }
}