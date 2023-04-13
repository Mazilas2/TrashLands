const path = require('path');
const url = require('url');
const electron = require('electron');
const {app, BrowserWindow} = electron;

let win;

function createWindow() {
    win = new BrowserWindow({ width: 1600, height: 900 });
    
    win.loadURL(
        url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
        })
    );
    
    win.on('closed', () => {
        win = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
        app.quit();
});

