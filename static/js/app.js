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
	document.cookie = name+"="+value+expires+"; path=/; SameSite=Lax";
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
	document.body.classList.add('no-animate');
}

function enableAnimations() {
	document.body.classList.remove('no-animate');
}

function toggleDarkMode() {
	var mode = getCookie('mode');
	var newMode = mode === 'dark' ? 'light': 'dark';
	setCookie('mode', newMode, 3650);
	document.getElementsByTagName('html')[0].classList.toggle('dark-mode', newMode === 'dark');
}

var delayedEnableAnimations = debounce(enableAnimations, 100);

bindEvent(window, 'resize', function() {
	disableAnimations();
	delayedEnableAnimations();
});
var darkModeButton = document.getElementById('toggle_dark_mode');
bindEvent(darkModeButton, 'click', toggleDarkMode);
darkModeButton.style.visibility = 'visible';
delayedEnableAnimations();

}());
