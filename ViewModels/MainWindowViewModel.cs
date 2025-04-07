using Avalonia.Controls;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using ReactiveUI;
using System.Reactive;

public class MainWindowViewModel : ReactiveObject
{
    // Загрузка файлов
    public ReactiveCommand<Unit, Unit> LoadFilesCommand { get; }
    public string LoadedFilesCount => $"Загружено файлов: {Employees.Count}";
    
    private async void LoadFiles()
    {
        var dialog = new OpenFileDialog
        {
            AllowMultiple = true,
            Filters = { new FileDialogFilter { Name = "Text Files", Extensions = { "txt" } } }
        };
        
        var files = await dialog.ShowAsync(new Window());
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
}