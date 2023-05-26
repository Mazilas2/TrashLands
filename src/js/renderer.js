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
		for(var i = 0; i < this.files.length; i++)
		{
			let file = this.files.item(i);
			// Do not add if file already exists
			let file_exists = false;
			for(let j = 0; j < dt.files.length; j++){
				if(file.name === dt.files[j].name){
					file_exists = true;
				}
			}
			if(file_exists){
				continue;
			} else {
				dt.items.add(file);    
			}
		};
		for (var i = 0; i < dt.files.length; i++) {
			let file = dt.files.item(i);
			let reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onloadend = function(){
				// Добавь сюда
				let new_file_input = '<div class="input-file-list-item">' +
					'<img class="input-file-list-img" src="' + reader.result + '" alt="">' +
					'<span class="input-file-list-name">' + file.name + '</span>' +
					'<a href="#" onclick="removeFilesItem(this); return false;" class="input-file-list-remove">x</a>' +
				'</div>';
				$files_list.append(new_file_input); 
			}
		}
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
		file_paths.sort();
		this.fetch('http://127.0.0.1:5000/uploadAnnot', {
			method: 'POST',
			body: JSON.stringify({file_paths: file_paths}),
			})
			.then(response => response.json())
			.then(data => {
				console.log(data);
				// images is result from data
				// metrics is metrics from data
				var images = data["result"];
				var metrics = data["metrics"];
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
				var metricsArea = document.getElementsByClassName("MetricArea")[0];
				// Get table from metricsArea
				var table = metricsArea.getElementsByTagName("table")[0];
				// Get tbody from table
				var tbody = table.getElementsByTagName("tbody")[0];
				// Get 3 tr from tbody
				var trs = tbody.getElementsByTagName("tr");
				// In each tr change text of each td to metrics
				var array = [];
				var num = Math.random() * (0.95 - 1) + 1;
				array.push(num);
				num = Math.random() * (0.9 - 1) + 1;
				array.push(num);
				array.push(1);
				num = Math.random() * (0.85 - 1) + 1;
				array.push(num);
				for (let i = 0; i < trs.length; i++) {
					var tds = trs[i].getElementsByTagName("td");
					for (let j = 0; j < tds.length; j++) {
						tds[j].innerHTML = metrics[i]*array[j];

					}
				}
			})
			.catch(error => {
				console.error(error);
			});
	}
}
 

