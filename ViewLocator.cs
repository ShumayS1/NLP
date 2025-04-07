using Avalonia.Controls;
using Avalonia.Controls.Templates;
using ReactiveUI;  // Добавьте эту директиву
using System;

namespace DIPLOMKA;

public class ViewLocator : IDataTemplate
{
    public Control Build(object? data)
    {
        var name = data?.GetType().FullName?.Replace("ViewModel", "View");
        if (name == null)
            return new TextBlock { Text = "Invalid ViewModel" };

        var type = Type.GetType(name);
        if (type != null)
            return (Control)Activator.CreateInstance(type)!;

        return new TextBlock { Text = $"View Not Found: {name}" };
    }

    public bool Match(object? data) => data is ReactiveObject;
}