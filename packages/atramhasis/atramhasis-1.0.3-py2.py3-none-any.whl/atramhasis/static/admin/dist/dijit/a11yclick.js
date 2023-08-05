//>>built
define("dijit/a11yclick",["dojo/keys","dojo/mouse","dojo/on","dojo/touch"],function(e,h,c,g){function k(a){if((a.keyCode===e.ENTER||a.keyCode===e.SPACE)&&!/input|button|textarea/i.test(a.target.nodeName))for(a=a.target;a;a=a.parentNode)if(a.dojoClick)return!0}var d;c(document,"keydown",function(a){k(a)?(d=a.target,a.preventDefault()):d=null});c(document,"keyup",function(a){k(a)&&a.target==d&&(d=null,c.emit(a.target,"click",{cancelable:!0,bubbles:!0,ctrlKey:a.ctrlKey,shiftKey:a.shiftKey,metaKey:a.metaKey,
altKey:a.altKey,_origType:a.type}))});var b=function(a,f){a.dojoClick=!0;return c(a,"click",f)};b.click=b;b.press=function(a,f){var b=c(a,g.press,function(a){("mousedown"!=a.type||h.isLeft(a))&&f(a)}),d=c(a,"keydown",function(a){a.keyCode!==e.ENTER&&a.keyCode!==e.SPACE||f(a)});return{remove:function(){b.remove();d.remove()}}};b.release=function(a,b){var d=c(a,g.release,function(a){("mouseup"!=a.type||h.isLeft(a))&&b(a)}),f=c(a,"keyup",function(a){a.keyCode!==e.ENTER&&a.keyCode!==e.SPACE||b(a)});return{remove:function(){d.remove();
f.remove()}}};b.move=g.move;return b});
//# sourceMappingURL=a11yclick.js.map