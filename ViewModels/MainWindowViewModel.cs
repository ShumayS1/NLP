using Avalonia.Controls;
using DIPLOMKA.Models;
using DIPLOMKA.Services;
using ReactiveUI;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Reactive;
using System.Threading.Tasks;
using DIPLOMKA.Utilities;

namespace DIPLOMKA.ViewModels;

public class MainWindowViewModel : ReactiveObject
{
    // Поля
    private string _inputText = string.Empty;
    private TeamAnalysisResult _analysisResult = new();
    private int _teamSizeIndex;
    private readonly NLPService _nlpService = new();
    private readonly TeamAnalyzerService _teamAnalyzer = new();
    private readonly FileDialogService _fileDialog = new();

    // Коллекция сотрудников (исправление CS0103)
    public ObservableCollection<EmployeeData> Employees { get; } = new();

    // Свойства
    public string InputText
    {
        get => _inputText;
        set => this.RaiseAndSetIfChanged(ref _inputText, value);
    }

    public int TeamSizeIndex
    {
        get => _teamSizeIndex;
        set => this.RaiseAndSetIfChanged(ref _teamSizeIndex, value);
    }

    public int TeamSize => TeamSizeIndex + 2; // 2-8 человек

    public TeamAnalysisResult AnalysisResult
    {
        get => _analysisResult;
        set => this.RaiseAndSetIfChanged(ref _analysisResult, value);
    }

    // Команды (исправление CS8618)
    public ReactiveCommand<Unit, Unit> LoadFilesCommand { get; }
    public ReactiveCommand<Unit, Unit> AnalyzeCommand { get; }

    public string LoadedFilesCount => $"Загружено файлов: {Employees.Count}";

    public MainWindowViewModel()
    {
        // Инициализация команд (исправление CS8618)
        LoadFilesCommand = ReactiveCommand.CreateFromTask(LoadFilesAsync);
        AnalyzeCommand = ReactiveCommand.Create(AnalyzeTeam);
    }

    private async Task LoadFilesAsync()
    {
        var files = await _fileDialog.OpenFilesAsync(new Window());
        if (files != null)
        {
            foreach (var file in files)
            {
                var content = await File.ReadAllTextAsync(file);
                Employees.Add(new EmployeeData
                {
                    Name = Path.GetFileNameWithoutExtension(file),
                    ResumeText = content
                });
            }
            this.RaisePropertyChanged(nameof(LoadedFilesCount));
        }
    }

    private void AnalyzeTeam()
    {
        if (Employees.Count < 2) return;

        var selectedTeam = Employees.Take(TeamSize).ToList();
        AnalysisResult = _teamAnalyzer.Analyze(selectedTeam); // Исправлено на _teamAnalyzer.Analyze
    }
}