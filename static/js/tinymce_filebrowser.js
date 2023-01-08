(function() {


function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


function attachments_filebrowser(callback, value, meta) {
	var url = tinyMCE.activeEditor.settings.images_upload_url;
	url += url.indexOf('?') === -1 ? '?' : '&';
	url += 'filetype=' + encodeURIComponent(meta.filetype);

	tinyMCE.activeEditor.windowManager.openUrl(
		{
			'title': 'Files',
			'url': url,
			'onMessage': function (dialogApi, details) {
				callback(details.data.url, {alt: details.data.name});
				dialogApi.close();
			},
		},
	);
}


function attachments_upload_handler(blobInfo, success, failure, progress) {
	var xhr, formData;
	var url = tinyMCE.activeEditor.settings.images_upload_url;

	console.log(blobInfo);

	xhr = new XMLHttpRequest();
	xhr.withCredentials = false;
	xhr.open('POST', url);

	xhr.upload.onprogress = function (e) {
		progress(e.loaded / e.total * 100);
	};

	xhr.onload = function() {
		var json;

		if (xhr.status === 403) {
			failure('HTTP Error: ' + xhr.status, { remove: true });
			return;
		}

		if (xhr.status < 200 || xhr.status >= 300) {
			failure('HTTP Error: ' + xhr.status);
			return;
		}

		json = JSON.parse(xhr.responseText);

		if (!json || typeof json.location != 'string') {
			failure('Invalid JSON: ' + xhr.responseText);
			return;
		}

		success(json.location);
	};

	xhr.onerror = function () {
		failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
	};

	formData = new FormData();
	formData.append('file', blobInfo.blob(), blobInfo.filename());
	formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

	xhr.send(formData);
};


window.attachments_filebrowser = attachments_filebrowser;
window.attachments_upload_handler = attachments_upload_handler;


}());
