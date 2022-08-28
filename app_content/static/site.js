window.addEventListener('load', load_content);

async function load_content(){
loadTag('/get_articles?category=SPACE', 'tab1-box');
loadTag('/get_articles?category=NATURE', 'tab2-box');
loadTag('/get_articles?category=PHYSIOLOGY', 'tab3-box');
loadTag('/get_articles?category=SOCIOLOGY', 'tab4-box');
}

async function reverse_tag(id){
	switch(id) {
		case 1:
			loadTag('/get_articles?category=SPACE', 'tab1-box');
			break;	
		case 2:
			loadTag('/get_articles?category=NATURE', 'tab2-box');
			break;	
		case 3:
			loadTag('/get_articles?category=PHYSIOLOGY', 'tab3-box');
			break;	
		case 4:
			loadTag('/get_articles?category=SOCIOLOGY', 'tab4-box');
			break;	
	}
}

async function reverse_tags(){
	var id = document.getElementsByClassName('tab-pane active')[0].children[0].id;
	switch(id) {
		case 'tab1-box':
			loadTag('/get_articles?category=SPACE', 'tab1-box');
			break;	
		case 'tab2-box':
			loadTag('/get_articles?category=NATURE', 'tab2-box');
			break;	
		case 'tab3-box':
			loadTag('/get_articles?category=PHYSIOLOGY', 'tab3-box');
			break;	
		case 'tab4-box':
			loadTag('/get_articles?category=SOCIOLOGY', 'tab4-box');
			break;	
	}
}

async function loadTag(category, target, cb){
	var template = document.getElementById('article_template').innerHTML;

var results = await fetch(category)
results = await results.json();

var target = document.getElementById(target);
target.innerHTML = '';
	
	// Pick 5 random articles
	// quick sol: https://www.codegrepper.com/code-examples/javascript/generate+5+unique+random+numbers+javascript
	var articleInds = [];
	while(articleInds.length < 5){
    	var r = Math.round(Math.random() * 30);
    	if(articleInds.indexOf(r) === -1) articleInds.push(r);
	}
	
	
for (var i = 0; i < 5; i ++) {
	// gen tags
	if(results[articleInds[i]].Keywords != null) {
	var tags = results[articleInds[i]].Keywords.split(',');
	var tagHTML = '';
	for (var e = 0; e < tags.length; e++)
		tagHTML += '<div class="box-main0-tag box-main' + e + '-tag" onclick="show_tag(event,\'' + tags[e] + '\')">' + tags[e] + '</div>'
	}
	
    target.innerHTML += template
        .replaceAll('%TITLE%', results[articleInds[i]].ArticleName.replaceAll('â€™','\'').replaceAll('â€˜','').replaceAll('â€“','-'))
        .replaceAll('%URL%', results[articleInds[i]].ArticleURL)
        .replaceAll('%DESC%', results[articleInds[i]].Description.replaceAll('â€™','\'').replaceAll('â€˜','').replaceAll('â€“','-'))
        .replaceAll('%AUTHOR%', results[articleInds[i]].Author)
        .replaceAll('%IMGSRC%', '/static/images/icons/' + results[articleInds[i]].ArticleID + '.jpg')
        .replaceAll('%DATE%', new Date(results[articleInds[i]].Date).toDateString())
		.replaceAll('%TAGS%', tagHTML)
	
}
if (cb != null)
	cb();
}

function show_tag(event, tagname) {
	event.stopImmediatePropagation();
	event.preventDefault();
	var id = document.getElementsByClassName('tab-pane active')[0].children[0].id;
	var target = document.getElementById(id);

	loadTag('/get_related_articles?tag=' + tagname, id,()=>{
	target.innerHTML = '<center><h2 class="keyword-label">Showing keywords related to ' + tagname + '</h2><button type="button" class="btn btn-primary keyword-back" onclick="reverse_tags()">Back</button></center>' + target.innerHTML;
});
}