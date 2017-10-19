// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// Textile tags example
// http://en.wikipedia.org/wiki/Textile_(markup_language)
// http://www.textism.com/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	previewParserPath:	'/markitup/preview/',
	onShiftEnter:		{keepDefault:false, replaceWith:'\n\n'},
	markupSet: [
		{name:'Heading 1', key:'1', openWith:'h1(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 2', key:'2', openWith:'h2(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 3', key:'3', openWith:'h3(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 4', key:'4', openWith:'h4(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 5', key:'5', openWith:'h5(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 6', key:'6', openWith:'h6(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Paragraph', key:'P', openWith:'p(!(([![Class]!]))!). '},
		{separator:'---------------' },
		{name:'Bold', key:'B', closeWith:'*', openWith:'*'},
		{name:'Italic', key:'I', closeWith:'_', openWith:'_'},
		{name:'Stroke through', key:'S', closeWith:'-', openWith:'-'},
		{separator:'---------------' },
		{name:'Bulleted list', openWith:'(!(* |!|*)!)'},
		{name:'Numeric list', openWith:'(!(# |!|#)!)'}, 
		{separator:'---------------' },
		{name:'Picture', replaceWith:function(markItUp) {
            MedialibraryBrowserHelper.show(markItUp);
            return false;
        }},
		{name:'Link', openWith:'"', closeWith:'([![Title]!])":[![Link:!:http://]!]', placeHolder:'Your text to link here...' },
		{separator:'---------------' },
		{name:'Quotes', openWith:'bq(!(([![Class]!])!)). '},
		{name:'Code', openWith:'@', closeWith:'@'}
	]
}

/**
 I added the FileBrowserHelper object so that it can store the original markitup
 object that fired the event / popup, so that I can use it when trying to return
 to the edittor.
 **/
var MedialibraryBrowserHelper = {

    markItUp: false,
    show: function(markItUp) {
        this.markItUp = markItUp;
        //var textarea_id = $(markItUp.textarea).attr('id');
        //FileBrowser.show(textarea_id, '/admin/filebrowser/browse/?pop=1&type=');
        showMediaLibraryPop('/admin/medialibrary/mediafile/');
    },

    triggerInsert: function(url) {

        $(this.markItUp.textarea).trigger('insertion',
            [{replaceWith: '!(left)'+url+'(description)!'}]);
    }
};

function showMediaLibraryPop(triggeringLink) {

    var name = 'Media bestand toevoegen';
    var href = triggeringLink + '?content=1';
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
