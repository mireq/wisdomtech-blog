(function() {

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
	document.body.classList.add('no-animate');
}

var delayedEnableAnimations = debounce(enableAnimations, 100);

bindEvent(window, 'resize', function() {
	disableAnimations();
	delayedEnableAnimations();
});

}());
