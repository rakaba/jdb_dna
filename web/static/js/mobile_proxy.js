var d = window.document;
if (navigator.userAgent.indexOf('iPhone') > 0 || navigator.userAgent.indexOf('iPad') > 0 || navigator.userAgent.indexOf('iPod') > 0 || navigator.userAgent.indexOf('Android') > 0) {
	d.write('<meta name="viewport" content="width=device-width minimum-scale=1.0, maximum-scale=2.0, user-scalable=yes">');
}
if (navigator.userAgent.indexOf('iPad') > 0) {
	d.write('<meta name="viewport" content="width=1280">');
}
