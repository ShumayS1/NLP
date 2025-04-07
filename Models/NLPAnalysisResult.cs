namespace DIPLOMKA.Models;

public class NLPAnalysisResult
{
    public string CommunicationStyle { get; set; } = string.Empty;
    public string PersonalityType { get; set; } = string.Empty;
    public double SentimentScore { get; set; } // -1 (негатив) до 1 (позитив)
}