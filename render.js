// Add function to launch .py/folderRead.py to read the folder and return the list of files

function readFolder() {
    var python = require('child_process').spawn('python', ['./py/folderRead.py', input.value]);
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        var dataString = data.toString();
        console.log(dataString);
    });
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
    }
    );
}