//>>built
define("dgrid/Tree","dojo/_base/declare dojo/_base/lang dojo/_base/array dojo/aspect dojo/dom-construct dojo/dom-class dojo/on dojo/query dojo/when ./util/has-css3 ./Grid dojo/has!touch?./util/touch".split(" "),function(x,y,z,C,q,n,A,u,B,w,D,r){return x(null,{collapseOnRefresh:!1,enableTreeTransitions:!0,treeIndentWidth:9,constructor:function(){this._treeColumnListeners=[]},shouldExpand:function(a,b,c){return c},expand:function(a,b,c){if(this._treeColumn){var d=this,e=a.element?a:this.row(a),l=!!this._expanded[e.id],
h=w("transitionend"),m;a=e.element;a=-1<a.className.indexOf("dgrid-expando-icon")?a:u(".dgrid-expando-icon",a)[0];c=c||!this.enableTreeTransitions;if(a&&a.mayHaveChildren&&(c||b!==l)){var g=void 0===b?!this._expanded[e.id]:b;n.replace(a,"ui-icon-triangle-1-"+(g?"se":"e"),"ui-icon-triangle-1-"+(g?"e":"se"));n.toggle(e.element,"dgrid-row-expanded",g);b=e.element;var f=b.connected,p,v,k={};if(!f){var f=k.container=b.connected=q.create("div",{className:"dgrid-tree-container"},b,"after"),t=function(a){var b=
d._renderedCollection.getChildren(e.data);d.sort&&0<d.sort.length&&(b=b.sort(d.sort));b.track&&d.shouldTrackCollection&&(f._rows=a.rows=[],b=b.track(),f._handles=[b.tracking,d._observeCollection(b,f,a)]);return"start"in a?b.fetchRange({start:a.start,end:a.start+a.count}):b.fetch()};"level"in a&&(f.level=t.level=a.level+1);if(this.renderQuery)m=this.renderQuery(t,k);else{var r=q.create("div",null,f);m=this._trackError(function(){return d.renderQueryResults(t(k),r,y.mixin({rows:k.rows},"level"in t?
{queryLevel:t.level}:null)).then(function(a){q.destroy(r);return a})})}h&&A(f,h,this._onTreeTransitionEnd)}f.hidden=!g;p=f.style;!h||c?(p.display=g?"block":"none",p.height=""):(g?(p.display="block",v=f.scrollHeight,p.height="0px"):(n.add(f,"dgrid-tree-resetting"),p.height=f.scrollHeight+"px"),setTimeout(function(){n.remove(f,"dgrid-tree-resetting");p.height=g?v?v+"px":"auto":"0px"},0));g?this._expanded[e.id]=!0:delete this._expanded[e.id]}return B(m)}},_configColumns:function(){var a=this.inherited(arguments);
this._expanded={};for(var b=0,c=a.length;b<c;b++)if(a[b].renderExpando){this._configureTreeColumn(a[b]);break}return a},insertRow:function(a,b,c,d,e){e=e||{};var l=e.queryLevel="queryLevel"in e?e.queryLevel:"level"in b?b.level:0,h=this.inherited(arguments),m=this.row(h);(l=this.shouldExpand(m,l,this._expanded[m.id]))&&this.expand(h,!0,!0);(l||!this.collection.mayHaveChildren||this.collection.mayHaveChildren(a))&&n.add(h,"dgrid-row-expandable");return h},removeRow:function(a,b){var c=a.connected,d=
{};c&&(c._handles&&(z.forEach(c._handles,function(a){a.remove()}),delete c._handles),c._rows&&(d.rows=c._rows),u("\x3e.dgrid-row",c).forEach(function(a){this.removeRow(a,!0,d)},this),c._rows&&(c._rows.length=0,delete c._rows),b||q.destroy(c));this.inherited(arguments)},_refreshCellFromItem:function(a,b){if(!a.column.renderExpando)return this.inherited(arguments);this.inherited(arguments,[a,b,{queryLevel:u(".dgrid-expando-icon",a.element)[0].level}])},cleanup:function(){this.inherited(arguments);this.collapseOnRefresh&&
(this._expanded={})},_destroyColumns:function(){this.inherited(arguments);for(var a=this._treeColumnListeners,b=a.length;b--;)a[b].remove();this._treeColumnListeners=[];this._treeColumn=null},_calcRowHeight:function(a){var b=a.connected;return this.inherited(arguments)+(b?b.offsetHeight:0)},_configureTreeColumn:function(a){var b=this,c=".dgrid-content .dgrid-column-"+a.id,d;this._treeColumn=a;if(!a._isConfiguredTreeColumn){var e=a.renderCell||this._defaultRenderCell;a._isConfiguredTreeColumn=!0;a.renderCell=
function(c,d,g,f){var h=f&&"queryLevel"in f?f.queryLevel:0,m=!b.collection.mayHaveChildren||b.collection.mayHaveChildren(c),k;k=a.renderExpando(h,m,b._expanded[b.collection.getIdentity(c)],c);k.level=h;k.mayHaveChildren=m;(c=e.call(a,c,d,g,f))&&c.nodeType?(g.appendChild(k),g.appendChild(c)):g.insertBefore(k,g.firstChild)};"function"!==typeof a.renderExpando&&(a.renderExpando=this._defaultRenderExpando)}var l=this._treeColumnListeners;0===l.length&&(l.push(this.on(a.expandOn||".dgrid-expando-icon:click,"+
c+":dblclick,"+c+":keydown",function(a){var c=b.row(a);b.collection.mayHaveChildren&&!b.collection.mayHaveChildren(c.data)||"keydown"===a.type&&32!==a.keyCode||"dblclick"===a.type&&d&&1<d.count&&c.id===d.id&&-1<a.target.className.indexOf("dgrid-expando-icon")||b.expand(c);-1<a.target.className.indexOf("dgrid-expando-icon")&&(d&&d.id===b.row(a).id?d.count++:d={id:b.row(a).id,count:1})})),w("touch")&&l.push(this.on(r.selector(c,r.dbltap),function(){b.expand(this)})))},_defaultRenderExpando:function(a,
b,c){var d=this.grid.isRTL?"right":"left",e="dgrid-expando-icon";b&&(e+=" ui-icon ui-icon-triangle-1-"+(c?"se":"e"));return q.create("div",{className:e,innerHTML:"\x26nbsp;",style:"margin-"+d+": "+a*this.grid.treeIndentWidth+"px; float: "+d+";"})},_onNotification:function(a,b){"delete"===b.type&&delete this._expanded[b.id];this.inherited(arguments)},_onTreeTransitionEnd:function(a){var b=this,c=this.style.height;c&&(this.style.display="0px"===c?"none":"block");a&&(n.add(this,"dgrid-tree-resetting"),
setTimeout(function(){n.remove(b,"dgrid-tree-resetting")},0));this.style.height=""}})});
//# sourceMappingURL=Tree.js.map