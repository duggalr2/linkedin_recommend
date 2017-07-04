<%
Dim fs, f, v
Set fs = Server.CreateObject('Scripting.FileSystemObject')
Set f = fs.GetFile('test.txt', true)
f.write('hello')
f.close
set f=nothing
set fs=nothing
%>