var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,a,o,i,u,l,s,d,f,c,p,h,v,b,g,m={8097:(e,r,t)=>{var n={"./index":()=>Promise.all([t.e(533),t.e(704)]).then((()=>()=>t(6704))),"./extension":()=>Promise.all([t.e(533),t.e(704)]).then((()=>()=>t(6704))),"./style":()=>Promise.all([t.e(533),t.e(643)]).then((()=>()=>t(6643)))},a=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n="default",a=t.S[n];if(a&&a!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>a,init:()=>o})}},y={};function x(e){var r=y[e];if(void 0!==r)return r.exports;var t=y[e]={id:e,exports:{}};return m[e].call(t.exports,t,t.exports,x),t.exports}x.m=m,x.c=y,x.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return x.d(r,{a:r}),r},x.d=(e,r)=>{for(var t in r)x.o(r,t)&&!x.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},x.f={},x.e=e=>Promise.all(Object.keys(x.f).reduce(((r,t)=>(x.f[t](e,r),r)),[])),x.u=e=>e+"."+{533:"d6b9fd7a31727b57ec5a",643:"bb10b0cf3cac77c8d13d",654:"37cda6b64b789e43ffac",704:"654ced8aac282e7771a2"}[e]+".js?v="+{533:"d6b9fd7a31727b57ec5a",643:"bb10b0cf3cac77c8d13d",654:"37cda6b64b789e43ffac",704:"654ced8aac282e7771a2"}[e],x.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),x.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@jupyterlab/katex-extension:",x.l=(t,n,a,o)=>{if(e[t])e[t].push(n);else{var i,u;if(void 0!==a)for(var l=document.getElementsByTagName("script"),s=0;s<l.length;s++){var d=l[s];if(d.getAttribute("src")==t||d.getAttribute("data-webpack")==r+a){i=d;break}}i||(u=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,x.nc&&i.setAttribute("nonce",x.nc),i.setAttribute("data-webpack",r+a),i.src=t),e[t]=[n];var f=(r,n)=>{i.onerror=i.onload=null,clearTimeout(c);var a=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),a&&a.forEach((e=>e(n))),r)return r(n)},c=setTimeout(f.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=f.bind(null,i.onerror),i.onload=f.bind(null,i.onload),u&&document.head.appendChild(i)}},x.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{x.S={};var e={},r={};x.I=(t,n)=>{n||(n=[]);var a=r[t];if(a||(a=r[t]={}),!(n.indexOf(a)>=0)){if(n.push(a),e[t])return e[t];x.o(x.S,t)||(x.S[t]={});var o=x.S[t],i="@jupyterlab/katex-extension",u=(e,r,t,n)=>{var a=o[e]=o[e]||{},u=a[r];(!u||!u.loaded&&(!n!=!u.eager?n:i>u.from))&&(a[r]={get:t,from:i,eager:!!n})},l=[];return"default"===t&&(u("@jupyterlab/katex-extension","3.3.0",(()=>Promise.all([x.e(533),x.e(704)]).then((()=>()=>x(6704))))),u("katex","0.12.0",(()=>x.e(654).then((()=>()=>x(6654)))))),e[t]=l.length?Promise.all(l).then((()=>e[t]=1)):1}}})(),(()=>{var e;x.g.importScripts&&(e=x.g.location+"");var r=x.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),x.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var a=e[n],o=(typeof a)[0];if(n>=r.length)return"u"==o;var i=r[n],u=(typeof i)[0];if(o!=u)return"o"==o&&"n"==u||"s"==u||"u"==o;if("o"!=o&&"u"!=o&&a!=i)return a<i;n++}},a=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(u=e[o]))[0]?"-":(n>0?".":"")+(n=2,u);return t}var i=[];for(o=1;o<e.length;o++){var u=e[o];i.push(0===u?"not("+l()+")":1===u?"("+l()+" || "+l()+")":2===u?i.pop()+" "+i.pop():a(u))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],a=n<0;a&&(n=-n-1);for(var i=0,u=1,l=!0;;u++,i++){var s,d,f=u<e.length?(typeof e[u])[0]:"";if(i>=r.length||"o"==(d=(typeof(s=r[i]))[0]))return!l||("u"==f?u>n&&!a:""==f!=a);if("u"==d){if(!l||"u"!=f)return!1}else if(l)if(f==d)if(u<=n){if(s!=e[u])return!1}else{if(a?s>e[u]:s<e[u])return!1;s!=e[u]&&(l=!1)}else if("s"!=f&&"n"!=f){if(a||u<=n)return!1;l=!1,u--}else{if(u<=n||d<f!=a)return!1;l=!1}else"s"!=f&&"n"!=f&&(l=!1,u--)}}var c=[],p=c.pop.bind(c);for(i=1;i<e.length;i++){var h=e[i];c.push(1==h?p()|p():2==h?p()&p():h?o(h,r):!p())}return!!p()},i=(e,r)=>{var t=x.S[e];if(!t||!x.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},u=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},l=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+a(n)+")",s=(e,r,t,n)=>{var a=u(e,t);return o(n,a)||"undefined"!=typeof console&&console.warn&&console.warn(l(e,t,a,n)),f(e[t][a])},d=(e,r,t)=>{var a=e[r];return(r=Object.keys(a).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&a[r]},f=e=>(e.loaded=1,e.get()),p=(c=e=>function(r,t,n,a){var o=x.I(r);return o&&o.then?o.then(e.bind(e,r,x.S[r],t,n,a)):e(r,x.S[r],t,n,a)})(((e,r,t,n)=>(i(e,t),s(r,0,t,n)))),h=c(((e,r,t,n,a)=>{var o=r&&x.o(r,t)&&d(r,t,n);return o?f(o):a()})),v={},b={2736:()=>p("default","@jupyterlab/rendermime",[1,3,2,8]),4674:()=>p("default","@jupyterlab/settingregistry",[1,3,2,8]),8509:()=>h("default","katex",[2,0,12,0],(()=>x.e(654).then((()=>()=>x(6654)))))},g={704:[2736,4674,8509]},x.f.consumes=(e,r)=>{x.o(g,e)&&g[e].forEach((e=>{if(x.o(v,e))return r.push(v[e]);var t=r=>{v[e]=0,x.m[e]=t=>{delete x.c[e],t.exports=r()}},n=r=>{delete v[e],x.m[e]=t=>{throw delete x.c[e],r}};try{var a=b[e]();a.then?r.push(v[e]=a.then(t).catch(n)):t(a)}catch(e){n(e)}}))},(()=>{var e={582:0};x.f.j=(r,t)=>{var n=x.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var a=new Promise(((t,a)=>n=e[r]=[t,a]));t.push(n[2]=a);var o=x.p+x.u(r),i=new Error;x.l(o,(t=>{if(x.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var a=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+a+": "+o+")",i.name="ChunkLoadError",i.type=a,i.request=o,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,a,[o,i,u]=t,l=0;if(o.some((r=>0!==e[r]))){for(n in i)x.o(i,n)&&(x.m[n]=i[n]);u&&u(x)}for(r&&r(t);l<o.length;l++)a=o[l],x.o(e,a)&&e[a]&&e[a][0](),e[a]=0},t=self.webpackChunk_jupyterlab_katex_extension=self.webpackChunk_jupyterlab_katex_extension||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var w=x(8097);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@jupyterlab/katex-extension"]=w})();