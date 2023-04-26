const path = require('path');
const url = require('url');
const electron = require('electron');
const {app, BrowserWindow} = electron;
const { ipcMain } = require('electron');
const {spawn} = require('child_process');



let win;

function createWindow() {
    win = new BrowserWindow({ 
        width: 1600, 
        height: 900,
        show: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    
    win.loadURL(
        url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
        })
    );
    const serverProcess = spawn('python', ['-u', path.join(__dirname, 'app.py')]);
    serverProcess.stdout.on('data', (data) => {
        console.log(data.toString());
      });
    
      // Логируем ошибки сервера в консоль
      serverProcess.stderr.on('data', (data) => {
        console.error(data.toString());
      });
    
      win.on('closed', () => {
        // Завершаем процесс сервера при закрытии окна
        serverProcess.kill();
        win = null;
      });
    win.on('closed', () => {
        win = null;
    });
    win.once('ready-to-show', () => {
        win.show();
    });
}

app.on('ready', () => 
{
    createWindow();
});

app.on('window-all-closed', () => {
        app.quit();
});

ipcMain.on('files', (event, arg) => {
    PythonShell.run('app.py', null, function (err, results) {
        console.log('finished');
        console.log(results);
    });
});




