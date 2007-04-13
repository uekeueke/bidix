//last update: RSSReaderPlugin v 1.1.0//

!Description
This plugin provides a RSSReader for TiddlyWiki
* It accesses asynchronously an RSSFeed
*Depending on the chanel item format, each item could be written as :
**simple text wikified
**html

!Usage
{{{
<<rssReader noDesc|asHtml|asText rssUrl ['filtering string']>>
	noDesc: only title of item is printed

	asHtml: if you know that description contain html (links, img ...), 
		the text is enclosed with <html> </html> tags

 	asText: if the description should not be interpreted as html the 
		description is wikified

	rssUrl: the rssFeed url that could be accessed. 
	
	'filtering string': if present, the rssfeed item title must contained 
		this string to be displayed. 
		If 'filering string' contained space characters only, the tiddler 
		title is used for filtering.

}}}

For security reasons, if the TiddlyWiki is accessed from http, a ProxyService should be used to access an rssFeed from an other site.

!examples
| !reader | !RSSFeed type | !working from | !importTiddler |
| BidiXTWRSS |TiddlyWiki RSSNamespace | file: or tiddlywiki.bidix.info | yes |
| [[Le Monde]] | Description asText | file: or tiddlywiki.bidix.info using proxy | no |
| YahooNewsSport | Description asHtml | file: or tiddlywiki.bidix.info using proxy | no |
| TiddlyWikiRSS | Description asText | file: or tiddlywiki.bidix.info using proxy | no |
| [[Libération]] | noDesc | file: or tiddlywiki.bidix.info using proxy | no |
| [[TestComment]] | asText and filters | file: or tiddlywiki.bidix.info using proxy | no |

!Revision history
* V1.1.0 (2207/04/13)
**No more import functions
* V1.0.0 (2006/11/11)
**refactoring using core loadRemoteFile function
**import using new tiddlywiki:tiddler element
**import and presentation preserved without EricShulman's NestedSliderPlugin
**better display of items 
* v0.3.0 (24/08/2006)
** Filter on RSS item title
** Place to display redefined for asynchronous processing
* v0.2.2 (22/08/2006)
**Haloscan feed has no pubDate.
* v0.2.1 (08/05/2006)
* v0.2.0 (01/05/2006)
**Small adapations for del.icio.us feed
* v0.1.1 (28/04/2006)
**Bug : Channel without title 
* v0.1.0 (24/04/2006)
** initial release


