//>>built
define("dijit/Destroyable",["dojo/_base/array","dojo/aspect","dojo/_base/declare"],function(c,g,e){return e("dijit.Destroyable",null,{destroy:function(c){this._destroyed=!0},own:function(){var e=["destroyRecursive","destroy","remove"];c.forEach(arguments,function(b){function f(){k.remove();c.forEach(h,function(a){a.remove()})}var d,k=g.before(this,"destroy",function(a){b[d](a)}),h=[];b.then?(d="cancel",b.then(f,f)):c.forEach(e,function(a){"function"===typeof b[a]&&(d||(d=a),h.push(g.after(b,a,f,!0)))})},
this);return arguments}})});
//# sourceMappingURL=Destroyable.js.map