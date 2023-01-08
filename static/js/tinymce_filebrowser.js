function attachments_filebrowser(callback, value, meta) {
	var url = tinyMCE.activeEditor.settings.images_upload_url;
	url += url.indexOf('?') === -1 ? '?' : '&';
	url += 'filetype=' + encodeURIComponent(meta.filetype);

	tinyMCE.activeEditor.windowManager.openUrl(
		{
			'title': 'Files',
			'url': url,
			'width': 1024,
			'height': 800,
			'onMessage': function (dialogApi, details) {
				callback(details.content)
				dialogApi.close()
			}
		},
	);
}
