//>>built
define("dgrid/ColumnSet","dojo/_base/declare dojo/_base/lang dojo/dom-class dojo/dom-construct dojo/on dojo/aspect dojo/query dojo/has ./util/misc dojo/_base/sniff".split(" "),function(A,B,C,h,m,q,l,f,u){function r(a,b){var c=a._columnSetScrollLefts;l(".dgrid-column-set",b).forEach(function(a){a.scrollLeft=c[a.getAttribute("data-dgrid-column-set-id")]})}function n(a,b){1!==a.nodeType&&(a=a.parentNode);for(;a&&!l.matches(a,".dgrid-column-set[data-dgrid-column-set-id]",b);){if(b&&a===b||C.contains(a,
"dgrid"))return null;a=a.parentNode}return a}function t(a){var b=f("pointer");return b?(a=D[a]||a,"MS"===b.slice(0,2)?"MSPointer"+a.slice(0,1).toUpperCase()+a.slice(1):"pointer"+a):"touch"+a}function z(a,b,c){b=b.getAttribute("data-dgrid-column-set-id");a=a._columnSetScrollers[b];c=a.scrollLeft+c;a.scrollLeft=0>c?0:c}f.add("event-mousewheel",function(a,b,c){return"onmousewheel"in c});f.add("event-wheel",function(a,b,c){return"onwheel"in c});var D={start:"down",end:"up"},E=f("touch")&&function(a){return function(b,
c){var d=[m(b,t("start"),function(c){if(!a._currentlyTouchedColumnSet){var d=n(c.target,b);!d||c.pointerType&&"touch"!==c.pointerType&&2!==c.pointerType||(a._currentlyTouchedColumnSet=d,a._lastColumnSetTouchX=c.clientX,a._lastColumnSetTouchY=c.clientY)}}),m(b,t("move"),function(b){if(null!==a._currentlyTouchedColumnSet){var d=n(b.target);d&&(c.call(null,a,d,a._lastColumnSetTouchX-b.clientX),a._lastColumnSetTouchX=b.clientX,a._lastColumnSetTouchY=b.clientY)}}),m(b,t("end"),function(){a._currentlyTouchedColumnSet=
null})];return{remove:function(){for(var a=d.length;a--;)d[a].remove()}}}},F=f("event-mousewheel")||f("event-wheel")?function(a){return function(b,c){return m(b,f("event-wheel")?"wheel":"mousewheel",function(d){var e=n(d.target,b);e&&(d=d.deltaX||-d.wheelDeltaX/3)&&c.call(null,a,e,d)})}}:function(a){return function(b,c){return m(b,".dgrid-column-set[data-dgrid-column-set-id]:MozMousePixelScroll",function(b){1===b.axis&&c.call(null,a,this,b.detail)})}};return A(null,{postCreate:function(){var a=this;
this.inherited(arguments);this.on(F(this),z);if(f("touch"))this.on(E(this),z);this.on(".dgrid-column-set:dgrid-cellfocusin",function(b){a._onColumnSetCellFocus(b,this)});"function"===typeof this.expand&&q.after(this,"expand",function(b,c){b.then(function(){var b=a.row(c[0]);a._expanded[b.id]&&r(a,b.element.connected)});return b})},columnSets:[],createRowCells:function(a,b,c,d,e){for(var f=h.create("table",{className:"dgrid-row-table"}),k=h.create("tbody",null,f),k=h.create("tr",null,k),g=0,m=this.columnSets.length;g<
m;g++){var l=h.create(a,{className:"dgrid-column-set-cell dgrid-column-set-"+g},k),l=h.create("div",{className:"dgrid-column-set"},l);l.setAttribute("data-dgrid-column-set-id",g);var p;if((p=c||this.subRows)&&p.length){for(var q=[],r=g+"-",n=0,t=p.length;n<t;n++){var v=p[n],w=[];w.className=v.className;for(var x=0,u=v.length;x<u;x++){var y=v[x];null!=y.id&&0===y.id.indexOf(r)&&w.push(y)}q.push(w)}p=q}else p=void 0;l.appendChild(this.inherited(arguments,[a,b,p||this.columnSets[g],d,e]))}return f},
renderArray:function(){for(var a=this.inherited(arguments),b=0;b<a.length;b++)r(this,a[b]);return a},insertRow:function(){var a=this.inherited(arguments);r(this,a);return a},renderHeader:function(){function a(){d._positionScrollers()}this.inherited(arguments);var b=this.columnSets,c=this._columnSetScrollers,d=this,e;this._columnSetScrollerContents={};this._columnSetScrollLefts={};if(c)for(e in c)h.destroy(c[e]);else q.after(this,"resize",a,!0),q.after(this,"styleColumn",a,!0),this._columnSetScrollerNode=
h.create("div",{className:"dgrid-column-set-scroller-container"},this.footerNode,"after");c=this._columnSetScrollers={};e=0;for(c=b.length;e<c;e++)this._putScroller(b[e],e);this._positionScrollers()},styleColumnSet:function(a,b){var c=this.addCssRule("#"+u.escapeCssIdentifier(this.domNode.id)+" .dgrid-column-set-"+u.escapeCssIdentifier(a,"-"),b);this._positionScrollers();return c},configStructure:function(){this.columns={};this.subRows=[];for(var a=0,b=this.columnSets.length;a<b;a++)for(var c=this.columnSets[a],
d=0;d<c.length;d++)c[d]=this._configColumns(a+"-"+d+"-",c[d]);this.inherited(arguments)},_positionScrollers:function(){var a=this.domNode,b=this._columnSetScrollers,c=this._columnSetScrollerContents,d=this.columnSets,e=0,h=0,k,g;k=0;for(d=d.length;k<d;k++)g=l('.dgrid-column-set[data-dgrid-column-set-id\x3d"'+k+'"]',a)[0],e=g.offsetWidth,g=g.firstChild.offsetWidth,c[k].style.width=g+"px",b[k].style.width=e+"px",9>f("ie")&&(b[k].style.overflowX=g>e?"scroll":"auto"),g>e&&h++;this._columnSetScrollerNode.style.bottom=
this.showFooter?this.footerNode.offsetHeight+"px":"0";this.bodyNode.style.bottom=h?f("dom-scrollbar-height")+(f("ie")?1:0)+"px":"0"},_putScroller:function(a,b){var c=this._columnSetScrollers[b]=h.create("span",{className:"dgrid-column-set-scroller dgrid-column-set-scroller-"+b+(9>f("ie")?" dgrid-scrollbar-height":"")},this._columnSetScrollerNode);c.setAttribute("data-dgrid-column-set-id",b);this._columnSetScrollerContents[b]=h.create("div",{className:"dgrid-column-set-scroller-content"},c);m(c,"scroll",
B.hitch(this,"_onColumnSetScroll"))},_onColumnSetScroll:function(a){var b=a.target.scrollLeft;a=a.target.getAttribute("data-dgrid-column-set-id");var c;this._columnSetScrollLefts[a]!==b&&(l('.dgrid-column-set[data-dgrid-column-set-id\x3d"'+a+'"],.dgrid-column-set-scroller[data-dgrid-column-set-id\x3d"'+a+'"]',this.domNode).forEach(function(a,e){a.scrollLeft=b;e||(c=a.scrollLeft)}),this._columnSetScrollLefts[a]=c)},_setColumnSets:function(a){this._destroyColumns();this.columnSets=a;this._updateColumns()},
_scrollColumnSet:function(a,b){var c=a.tagName?a.getAttribute("data-dgrid-column-set-id"):a;this._columnSetScrollers[c].scrollLeft=0>b?0:b},_onColumnSetCellFocus:function(a,b){var c=a.target,d=b.getAttribute("data-dgrid-column-set-id"),d=this._columnSetScrollers[d];(c.offsetLeft-d.scrollLeft+c.offsetWidth>b.offsetWidth||d.scrollLeft>c.offsetLeft)&&this._scrollColumnSet(b,c.offsetLeft)}})});
//# sourceMappingURL=ColumnSet.js.map