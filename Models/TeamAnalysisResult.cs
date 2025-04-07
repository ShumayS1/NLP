namespace DIPLOMKA.Models;
using System.Collections.Generic;
public class TeamAnalysisResult
{
    public double CompatibilityScore { get; set; } // 0-100%
    public List<string> Strengths { get; set; } = new();
    public List<string> Weaknesses { get; set; } = new();
    public string SuccessProbability => CompatibilityScore > 70 ? "Высокая" : "Средняя";
}