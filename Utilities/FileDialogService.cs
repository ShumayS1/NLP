using Avalonia.Controls;
using System.Threading.Tasks;
namespace DIPLOMKA.Utilities;

public class FileDialogService
{
    public async Task<string[]?> OpenFilesAsync(Window parent)
    {
        var dialog = new OpenFileDialog
        {
            AllowMultiple = true,
            Filters = { new FileDialogFilter { Name = "Text Files", Extensions = { "txt" } } }
        };
        return await dialog.ShowAsync(parent);
    }
}