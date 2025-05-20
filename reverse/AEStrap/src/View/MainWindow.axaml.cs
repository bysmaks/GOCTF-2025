using Avalonia.Controls;
using AEStrap.ViewModels;

namespace AEStrap.View;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = new MainWindowViewModel();
    }
}