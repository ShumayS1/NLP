using DIPLOMKA.Models; // Добавляем эту директиву
using Microsoft.ML;
using Microsoft.ML.Data;

namespace DIPLOMKA.Services;

public class NLPService
{
    private readonly MLContext _mlContext = new();

    public NLPAnalysisResult AnalyzeText(string text)
    {
        return new NLPAnalysisResult
        {
            CommunicationStyle = AnalyzeCommunicationStyle(text),
            PersonalityType = PredictPersonalityType(text),
            SentimentScore = AnalyzeSentiment(text)
        };
    }

    private string AnalyzeCommunicationStyle(string text)
    {
        return text.Length > 100 ? "Formal" : "Casual";
    }

    private string PredictPersonalityType(string text)
    {
        return text.Contains("team") ? "EXTJ" : "INFP";
    }

    private float AnalyzeSentiment(string text)
    {
        // Заглушка для примера
        return text.Contains("success") ? 0.9f : 0.2f;
    }
}