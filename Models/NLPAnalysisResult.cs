public class NLPAnalysisResult
{
    public string CommunicationStyle { get; set; }
    public string PersonalityType { get; set; }
    public double SentimentScore { get; set; } // -1 (негатив) до 1 (позитив)
}