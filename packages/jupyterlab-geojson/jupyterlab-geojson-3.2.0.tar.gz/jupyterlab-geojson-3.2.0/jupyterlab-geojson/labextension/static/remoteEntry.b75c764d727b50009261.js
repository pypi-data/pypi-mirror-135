var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,o,a,i,u,l,s,f,d,p,c,h,v,g,b,m={957:(e,r,t)=>{var n={"./index":()=>t.e(41).then((()=>()=>t(41))),"./mimeExtension":()=>t.e(41).then((()=>()=>t(41))),"./style":()=>t.e(643).then((()=>()=>t(643)))},o=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),a=(e,r)=>{if(t.S){var n="default",o=t.S[n];if(o&&o!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>o,init:()=>a})}},y={};function w(e){var r=y[e];if(void 0!==r)return r.exports;var t=y[e]={id:e,exports:{}};return m[e].call(t.exports,t,t.exports,w),t.exports}w.m=m,w.c=y,w.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return w.d(r,{a:r}),r},w.d=(e,r)=>{for(var t in r)w.o(r,t)&&!w.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},w.f={},w.e=e=>Promise.all(Object.keys(w.f).reduce(((r,t)=>(w.f[t](e,r),r)),[])),w.u=e=>e+"."+{41:"0fe703a5cc833981b853",62:"8fb305ac8706f7626d62",643:"db1ae43fc09ae8518ae3"}[e]+".js?v="+{41:"0fe703a5cc833981b853",62:"8fb305ac8706f7626d62",643:"db1ae43fc09ae8518ae3"}[e],w.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),w.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@jupyterlab/geojson-extension:",w.l=(t,n,o,a)=>{if(e[t])e[t].push(n);else{var i,u;if(void 0!==o)for(var l=document.getElementsByTagName("script"),s=0;s<l.length;s++){var f=l[s];if(f.getAttribute("src")==t||f.getAttribute("data-webpack")==r+o){i=f;break}}i||(u=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,w.nc&&i.setAttribute("nonce",w.nc),i.setAttribute("data-webpack",r+o),i.src=t),e[t]=[n];var d=(r,n)=>{i.onerror=i.onload=null,clearTimeout(p);var o=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((e=>e(n))),r)return r(n)},p=setTimeout(d.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=d.bind(null,i.onerror),i.onload=d.bind(null,i.onload),u&&document.head.appendChild(i)}},w.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{w.S={};var e={},r={};w.I=(t,n)=>{n||(n=[]);var o=r[t];if(o||(o=r[t]={}),!(n.indexOf(o)>=0)){if(n.push(o),e[t])return e[t];w.o(w.S,t)||(w.S[t]={});var a=w.S[t],i="@jupyterlab/geojson-extension",u=(e,r,t,n)=>{var o=a[e]=a[e]||{},u=o[r];(!u||!u.loaded&&(!n!=!u.eager?n:i>u.from))&&(o[r]={get:t,from:i,eager:!!n})},l=[];return"default"===t&&(u("@jupyterlab/geojson-extension","3.2.0",(()=>w.e(41).then((()=>()=>w(41))))),u("leaflet","1.7.1",(()=>w.e(62).then((()=>()=>w(608)))))),e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;w.g.importScripts&&(e=w.g.location+"");var r=w.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),w.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var o=e[n],a=(typeof o)[0];if(n>=r.length)return"u"==a;var i=r[n],u=(typeof i)[0];if(a!=u)return"o"==a&&"n"==u||"s"==u||"u"==a;if("o"!=a&&"u"!=a&&o!=i)return o<i;n++}},o=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,a=1;a<e.length;a++)n--,t+="u"==(typeof(u=e[a]))[0]?"-":(n>0?".":"")+(n=2,u);return t}var i=[];for(a=1;a<e.length;a++){var u=e[a];i.push(0===u?"not("+l()+")":1===u?"("+l()+" || "+l()+")":2===u?i.pop()+" "+i.pop():o(u))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},a=(e,r)=>{if(0 in e){r=t(r);var n=e[0],o=n<0;o&&(n=-n-1);for(var i=0,u=1,l=!0;;u++,i++){var s,f,d=u<e.length?(typeof e[u])[0]:"";if(i>=r.length||"o"==(f=(typeof(s=r[i]))[0]))return!l||("u"==d?u>n&&!o:""==d!=o);if("u"==f){if(!l||"u"!=d)return!1}else if(l)if(d==f)if(u<=n){if(s!=e[u])return!1}else{if(o?s>e[u]:s<e[u])return!1;s!=e[u]&&(l=!1)}else if("s"!=d&&"n"!=d){if(o||u<=n)return!1;l=!1,u--}else{if(u<=n||f<d!=o)return!1;l=!1}else"s"!=d&&"n"!=d&&(l=!1,u--)}}var p=[],c=p.pop.bind(p);for(i=1;i<e.length;i++){var h=e[i];p.push(1==h?c()|c():2==h?c()&c():h?a(h,r):!c())}return!!c()},i=(e,r)=>{var t=w.S[e];if(!t||!w.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},u=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},l=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+o(n)+")",s=(e,r,t,n)=>{var o=u(e,t);return a(n,o)||"undefined"!=typeof console&&console.warn&&console.warn(l(e,t,o,n)),d(e[t][o])},f=(e,r,t)=>{var o=e[r];return(r=Object.keys(o).reduce(((e,r)=>!a(t,r)||e&&!n(e,r)?e:r),0))&&o[r]},d=e=>(e.loaded=1,e.get()),c=(p=e=>function(r,t,n,o){var a=w.I(r);return a&&a.then?a.then(e.bind(e,r,w.S[r],t,n,o)):e(r,w.S[r],t,n,o)})(((e,r,t,n)=>(i(e,t),s(r,0,t,n)))),h=p(((e,r,t,n,o)=>{var a=r&&w.o(r,t)&&f(r,t,n);return a?d(a):o()})),v={},g={538:()=>c("default","@jupyterlab/apputils",[1,3,2,8]),706:()=>c("default","@lumino/widgets",[1,1,19,0]),948:()=>h("default","leaflet",[1,1,5,0],(()=>w.e(62).then((()=>()=>w(608)))))},b={41:[538,706,948]},w.f.consumes=(e,r)=>{w.o(b,e)&&b[e].forEach((e=>{if(w.o(v,e))return r.push(v[e]);var t=r=>{v[e]=0,w.m[e]=t=>{delete w.c[e],t.exports=r()}},n=r=>{delete v[e],w.m[e]=t=>{throw delete w.c[e],r}};try{var o=g[e]();o.then?r.push(v[e]=o.then(t).catch(n)):t(o)}catch(e){n(e)}}))},(()=>{var e={103:0};w.f.j=(r,t)=>{var n=w.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var o=new Promise(((t,o)=>n=e[r]=[t,o]));t.push(n[2]=o);var a=w.p+w.u(r),i=new Error;w.l(a,(t=>{if(w.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var o=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+o+": "+a+")",i.name="ChunkLoadError",i.type=o,i.request=a,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,o,[a,i,u]=t,l=0;if(a.some((r=>0!==e[r]))){for(n in i)w.o(i,n)&&(w.m[n]=i[n]);u&&u(w)}for(r&&r(t);l<a.length;l++)o=a[l],w.o(e,o)&&e[o]&&e[o][0](),e[o]=0},t=self.webpackChunk_jupyterlab_geojson_extension=self.webpackChunk_jupyterlab_geojson_extension||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var j=w(957);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@jupyterlab/geojson-extension"]=j})();