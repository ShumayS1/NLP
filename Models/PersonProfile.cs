using System.IO;
using System.Linq;
using System;

namespace DIPLOMKA.Models;

public class PersonProfile
{
    public string Name { get; set; }
    public string Skills { get; set; }
    public int ExperienceYears { get; set; }
    public string Education { get; set; }
}
public class ProfileParser
{
    public static PersonProfile ParseProfile(string profileText)
    {
        int expectedNumberOfLines = 10;
        var lines = profileText.Split('\n').ToList();
        
        // Проверьте, что в массиве есть достаточно элементов
        if (lines.Count < expectedNumberOfLines) 
        {
            throw new InvalidOperationException("Profile text is incomplete.");
        }
        var name = lines.ElementAtOrDefault(0); // Возвращает null, если индекс выходит за пределы
        if (name == null)
        {
            throw new InvalidOperationException("Profile name is missing.");
        }
        var skills = lines[1].Split(':')[1].Trim();
        var experienceYears = int.Parse(lines[2].Split(':')[1].Trim());
        var education = lines[3].Split(':')[1].Trim();
            
        return new PersonProfile
        {
            Name = name,
            Skills = skills,
            ExperienceYears = experienceYears,
            Education = education
        };
    }
}