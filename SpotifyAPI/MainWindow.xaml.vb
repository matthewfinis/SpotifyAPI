Class MainWindow

    Public Value As String

    Private Sub Button_Click(sender As Object, e As RoutedEventArgs)

        Dim artistId As String = "4qwGe91Bz9K2T8jXTZ815W?si=c422wsWIQ_-X2yCanLeHfg"
        Dim OutputValue As String
        OutputValue = FetchArtistData(artistId)

    End Sub

    Public Function FetchArtistData(artistId As String)

        Dim proc As Process = New Process

        proc.StartInfo.FileName = "C:\Users\matth\anaconda3\python.exe" 'change this file path to where you have python installed
        proc.StartInfo.Arguments = "main.py " + artistId

        proc.StartInfo.UseShellExecute = False
        proc.StartInfo.WindowStyle = ProcessWindowStyle.Hidden
        proc.StartInfo.CreateNoWindow = True
        proc.StartInfo.RedirectStandardOutput = True

        proc.Start()

        AddHandler proc.OutputDataReceived, AddressOf process_OutputDataReceived

        proc.BeginOutputReadLine()
        proc.WaitForExit()

        Return Value

    End Function

    Public Function process_OutputDataReceived(sender As Object, e As DataReceivedEventArgs) As Object
        On Error Resume Next
        If Not e.Data = "" Then
            Value = e.Data.ToString()
        Else
        End If
    End Function
End Class
