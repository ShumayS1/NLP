using System.Collections.Generic; // Добавляем эту директиву
using DIPLOMKA.Models; // И эту

namespace DIPLOMKA.Services;

public class TeamAnalyzerService
{
    public TeamAnalysisResult Analyze(List<EmployeeData> team)
    {
        // Реализация анализа команды
        return new TeamAnalysisResult
        {
            CompatibilityScore = CalculateScore(team),
            Strengths = GetStrengths(team),
            Weaknesses = GetWeaknesses(team)
        };
    }

    private double CalculateScore(List<EmployeeData> team)
    {
        // Логика расчёта
        return 75.0; // Пример
    }

    private List<string> GetStrengths(List<EmployeeData> team)
    {
        return new List<string> { "Хорошая комбинация типов личности" };
    }

    private List<string> GetWeaknesses(List<EmployeeData> team)
    {
        return new List<string> { "Разные стили коммуникации" };
    }
}