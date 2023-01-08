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
