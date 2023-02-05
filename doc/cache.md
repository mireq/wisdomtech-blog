# NGINX caching

To enable nginx caching set `NGINX_CACHE_DIR` in `settings.py`.

Then in nginx configure caching with following directives:

```
uwsgi_cache_path <cache_dir> levels=1:2 keys_zone=blog_cache:10m max_size=100m inactive=14d;
uwsgi_cache_path <cache_dir>/list levels=1:2 keys_zone=blog_cache_list:10m max_size=100m inactive=14d;

server {
	…
	location ~ ^/(en/|sk/|)$ {
		uwsgi_cache blog_cache_list;
		uwsgi_cache_valid 200 1d;
		uwsgi_cache_key "${uri}:${arg_page}";

		include         snippets/call-uwsgi.conf;
	}

	location ~ ^/(en/|sk/|)[-a-zA-Z0-9_]+-p\d+/$ {
		uwsgi_cache blog_cache;
		uwsgi_cache_valid 200 301 302 7d;
		uwsgi_cache_key "${uri}";

		include         snippets/call-uwsgi.conf;
	}
	…
}
```

Pay attention to permissions. If you don't run django app under same user as
nginx, you will need trick to access cache. Something like:

```
bindfs -u web -g web /tmp/blog_cache /tmp/blog_cache_chmod/
```

and then use `/tmp/blog_cache_chmod/` for `NGINX_CACHE_DIR`.
