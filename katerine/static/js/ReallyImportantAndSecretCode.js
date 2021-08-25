$(function(){
	var code_keys = [], konami_code = "38,38,40,40,37,39,37,39,66,65";
	$(document).keydown(function(e) {
	code_keys.push(e.keyCode);
    if (code_keys.toString().indexOf(konami_code) >= 0 ){
			window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
			while (code_keys.length !== 0)
			{
				code_keys.pop()
			}
    	}
	});
});