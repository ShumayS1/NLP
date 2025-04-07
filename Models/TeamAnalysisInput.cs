
using Microsoft.ML.Data;
namespace DIPLOMKA.Models;

public class TeamAnalysisInput
{
    [LoadColumn(0)]
    public float ExperienceYears { get; set; }
        
    [LoadColumn(1)]
    public string Skills { get; set; }
}

public class TeamAnalysisPrediction
{
    [ColumnName("PredictedLabel")]
    public bool WillBeSuccessful { get; set; }
}