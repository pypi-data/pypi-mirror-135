//>>built
define("dojo/has",["./global","require","module"],function(b,g,h){var a=g.has||function(){};a.add("dom-addeventlistener",!!document.addEventListener);a.add("touch","ontouchstart"in document||"onpointerdown"in document&&0<navigator.maxTouchPoints||window.navigator.msMaxTouchPoints);a.add("touch-events","ontouchstart"in document);a.add("pointer-events","pointerEnabled"in window.navigator?window.navigator.pointerEnabled:"PointerEvent"in window);a.add("MSPointer",window.navigator.msPointerEnabled);a.add("touch-action",
a("touch")&&a("pointer-events"));a.add("device-width",screen.availWidth||innerWidth);b=document.createElement("form");a.add("dom-attributes-explicit",0==b.attributes.length);a.add("dom-attributes-specified-flag",0<b.attributes.length&&40>b.attributes.length);a.clearElement=function(a){a.innerHTML="";return a};a.normalize=function(c,b){var d=c.match(/[\?:]|[^:\?]*/g),f=0,e=function(b){var c=d[f++];if(":"==c)return 0;if("?"==d[f++]){if(!b&&a(c))return e();e(!0);return e(b)}return c||0};return(c=e())&&
b(c)};a.load=function(a,b,d){a?b([a],d):d()};return a});
//# sourceMappingURL=has.js.map