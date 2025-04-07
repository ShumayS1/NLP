using ReactiveUI;
using System.Collections.ObjectModel;

public class MainWindowViewModel : ReactiveObject
{
    private string _inputText;
    public string InputText
    {
        get => _inputText;
        set => this.RaiseAndSetIfChanged(ref _inputText, value);
    }

    public ObservableCollection<EmployeeData> Employees { get; } = new();

    public void Analyze()
    {
        var service = new NLPService();
        var result = service.AnalyzeText(InputText);

        Employees.Add(new EmployeeData
        {
            Name = "Candidate",
            ResumeText = InputText,
            CommunicationStyle = result.CommunicationStyle,
            PersonalityType = result.PersonalityType
        });
    }
}