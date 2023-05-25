window.$ = window.jQuery = require('jquery');
const { spawn } = require('child_process');

var submitButton;
var dt = new DataTransfer();

onload = function() 
{
  const form = document.getElementById('uploadForm');
  form.addEventListener('submit', (event) => {
    event.preventDefault();
  });
	funcAddFiles();
  const submitButton = document.getElementById('submitButton');
  submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    submitFunc();
  });
}

function funcAddFiles()
{
	submitButton = document.getElementById("submitButton");
	submitButton.style.display = "none";
	$('.input-file input[type=file]').on('change', function(){
		let $files_list = $(this).closest('.input-file').next();
		$files_list.empty();
		dt.items.clear();
		for(var i = 0; i < this.files.length; i++)
		{
			let file = this.files.item(i);
			dt.items.add(file);    
	
			let reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onloadend = function(){
				let new_file_input = '<div class="input-file-list-item">' +
					'<img class="input-file-list-img" src="' + reader.result + '">' +
					'<span class="input-file-list-name">' + file.name + '</span>' +
					'<a href="#" onclick="removeFilesItem(this); return false;" class="input-file-list-remove">x</a>' +
				'</div>';
				$files_list.append(new_file_input); 
			}
		};
		if (dt.files.length > 0) {
			submitButton.style.display = "flex";
		}
	});
}

function removeFilesItem(target)
{
	let name = $(target).prev().text();
	let input = $(target).closest('.input-file-row').find('input[type=file]');	
	$(target).closest('.input-file-list-item').remove();	
	for(let i = 0; i < dt.items.length; i++){
		if(name === dt.items[i].getAsFile().name){
			dt.items.remove(i);
		}
	}
	input[0].files = dt.files;  
	if (dt.files.length < 1) {
		submitButton.style.display = "none";
	}
}

function submitFunc()
{
  var file_paths = [];
  var txt_selected = false;
  // Check if each image have .txt annotation file
  for (let i = 0; i < dt.files.length; i++) {
	if (dt.files[i].path.endsWith('.jpg')) 
	{
    	file_paths.push(dt.files[i].path);
	}
	else if (dt.files[i].path.endsWith('.txt'))
	{
		txt_selected = true;
		file_paths.push(dt.files[i].path);
	}
  }
  if (!txt_selected) 
  {
	this.fetch('http://127.0.0.1:5000/upload', {
		method: 'POST',
		body: JSON.stringify({file_paths: file_paths}),
		})
		.then(response => response.json())
		.then(data => {
			var images = data;
			var resultArea = document.getElementById("resultArea");
			while (resultArea.firstChild) {
				resultArea.removeChild(resultArea.firstChild);
			}
			for (let i = 0; i < images.length; i++) {
				var imgEncoded = images[i];
				var binaryString = atob(imgEncoded);
				var bytes = new Uint8Array(binaryString.length);
				for (var j = 0; j < binaryString.length; j++) {
					bytes[j] = binaryString.charCodeAt(j);
				}
				var blob = new Blob([bytes], { type: 'image/jpeg' });
				var url = URL.createObjectURL(blob);
				var img = new Image();
				img.src = url;
				resultArea.appendChild(img);
			}
		})
		.catch(error => {
			console.error(error);
		});
	} else {
		this.fetch('http://127.0.0.1:5000/uploadAnnot', {
			method: 'POST',
			body: JSON.stringify({file_paths: file_paths}),
			})
			.then(response => response.json())
			.then(data => {
				var images = data;
				console.log(images);
				var resultArea = document.getElementById("resultArea");
				while (resultArea.firstChild) {
					resultArea.removeChild(resultArea.firstChild);
				}
				for (let i = 0; i < images.length; i++) {
					var imgEncoded = images[i];
					var binaryString = atob(imgEncoded);
					var bytes = new Uint8Array(binaryString.length);
					for (var j = 0; j < binaryString.length; j++) {
						bytes[j] = binaryString.charCodeAt(j);
					}
					var blob = new Blob([bytes], { type: 'image/jpeg' });
					var url = URL.createObjectURL(blob);
					var img = new Image();
					img.src = url;
					img.style.width = "100%";
					img.style.height = "100%";
					resultArea.appendChild(img);
				}
			})
			.catch(error => {
				console.error(error);
			});
	}
}
 

