var QueryString = function () {
  // This function is anonymous, is executed immediately and
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    	// If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = pair[1];
    	// If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]], pair[1] ];
      query_string[pair[0]] = arr;
    	// If third or later entry with this name
    } else {
      query_string[pair[0]].push(pair[1]);
    }
  }
    return query_string;
} ();
function removeParameter(url, parameter)
{
  var urlparts= url.split('?');

  if (urlparts.length>=2)
  {
      var urlBase=urlparts.shift(); //get first part, and remove from array
      var queryString=urlparts.join("?"); //join it back up

      var prefix = encodeURIComponent(parameter)+'=';
      var pars = queryString.split(/[&;]/g);
      for (var i= pars.length; i-->0;)               //reverse iteration as may be destructive
          if (pars[i].lastIndexOf(prefix, 0)!==-1)   //idiom for string.startsWith
              pars.splice(i, 1);
      if(pars.length > 0){
        url = urlBase+'?'+pars.join('&');
      }else {
        url = urlBase;
      }
  }
  return url;
}
/*
if(QueryString['download'] && parent === window){
    window.open(
       window.location.toString().split(window.location.pathname)[0] + QueryString['download'], '_blank');


}
if(QueryString['success'] && parent != window){
    var search = parent.location.search.substr(1).split('&').concat(window.location.search.substr(1).split('&'));

    var prefix = encodeURIComponent('success')+'=';
    //var pars = queryString.split(/[&;]/g);
    for (var i= search.length; i-->0;)               //reverse iteration as may be destructive
      if (search[i].lastIndexOf(prefix, 0)!==-1)   //idiom for string.startsWith
          search.splice(i, 1);
    parent.location.search = search.join('&');
}
*/