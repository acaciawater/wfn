(function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'wfn-icons\'">' + entity + '</span>' + html;
	}
	var icons = {
		'icon-twitter': '&#xe600;',
		'icon-search': '&#xe601;',
		'icon-quote-open': '&#xe602;',
		'icon-quote-close': '&#xe603;',
		'icon-profile': '&#xe604;',
		'icon-mail': '&#xe605;',
		'icon-linkedin': '&#xe606;',
		'icon-facebook': '&#xe607;',
		'icon-document': '&#xe608;',
		'icon-close': '&#xe609;',
		'icon-arrow-right': '&#xe60a;',
		'icon-arrow-dropdown': '&#xe60b;',
		'icon-arrow-down': '&#xe60c;',
		'icon-arrow-up': '&#xe60d;',
		'icon-youtube': '&#xe60e;',
		'0': 0
		},
		els = document.getElementsByTagName('*'),
		i, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
}());
