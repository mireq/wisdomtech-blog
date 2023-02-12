(function() {

var doc = document;
var body = doc.body;

function getCookie(name) {
	var cookieValue = null;
	var cookie = doc.cookie;
	if (cookie && cookie !== '') {
		var cookies = cookie.split(';');
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

function setCookie(name, value, days) {
	var expires;
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		expires = "; expires="+date.toGMTString();
	}
	else {
		expires = "";
	}
	doc.cookie = name+"="+value+expires+"; path=/; SameSite=Lax";
}

function bindEvent(element, name, fn) {
	element.addEventListener(name, fn, false);
}

function debounce(fn, delay) {
	var timer = null;
	var closure = function () {
		var context = this, args = arguments;
		clearTimeout(timer);
		timer = setTimeout(function () {
			fn.apply(context, args);
		}, delay);
	};
	return closure;
}

function disableAnimations() {
	body.classList.add('no-animate');
}

function enableAnimations() {
	body.classList.remove('no-animate');
}

function toggleDarkMode() {
	var mode = getCookie('mode');
	var newMode = mode === 'dark' ? 'light': 'dark';
	setCookie('mode', newMode, 3650);
	doc.getElementsByTagName('html')[0].classList.toggle('dark-mode', newMode === 'dark');
}

var delayedEnableAnimations = debounce(enableAnimations, 100);

bindEvent(window, 'resize', function() {
	disableAnimations();
	delayedEnableAnimations();
});
var darkModeButton = doc.getElementById('toggle_dark_mode');
bindEvent(darkModeButton, 'click', toggleDarkMode);
delayedEnableAnimations();

}());
