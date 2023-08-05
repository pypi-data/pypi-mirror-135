"use strict";(self.webpackChunkvegafusion_jupyter=self.webpackChunkvegafusion_jupyter||[]).push([[375],{375:(n,t,e)=>{function r(n,t,e){return n.fields=t||[],n.fname=e,n}function u(n){return null==n?null:n.fname}function o(n){return null==n?null:n.fields}function l(n){return 1===n.length?c(n[0]):i(n)}e.d(t,{cG:()=>E,jj:()=>d,kI:()=>w,Hq:()=>M,uU:()=>k,ZE:()=>r,Oj:()=>o,el:()=>u,IX:()=>L,j2:()=>nn,l$:()=>Q,qu:()=>Y,a9:()=>un,Ds:()=>on,vU:()=>f,l7:()=>ln,We:()=>cn,dI:()=>fn,k:()=>m,Xr:()=>gn,EP:()=>a,yl:()=>pn,nr:()=>an,id:()=>h,yR:()=>g,XW:()=>bn,u5:()=>yn,kJ:()=>v,jn:()=>mn,J_:()=>jn,mf:()=>V,TW:()=>Mn,hj:()=>dn,Kn:()=>D,Kj:()=>kn,HD:()=>wn,Jy:()=>En,t7:()=>On,kg:()=>O,$m:()=>vn,TS:()=>Dn,fE:()=>A,kX:()=>b,vk:()=>An,Dw:()=>N,mJ:()=>W,QA:()=>X,Zw:()=>$,fj:()=>z,mS:()=>Z,rx:()=>_n,yP:()=>Rn,_k:()=>s,m8:()=>xn,sw:()=>zn,ZU:()=>Jn,He:()=>S,Rg:()=>Tn,BB:()=>Pn,$G:()=>Un,yb:()=>y,N3:()=>F,FP:()=>Hn,iL:()=>R,bM:()=>p,ay:()=>B,dH:()=>C,mK:()=>G,bV:()=>K});const c=n=>function(t){return t[n]},i=n=>{const t=n.length;return function(e){for(let r=0;r<t;++r)e=e[n[r]];return e}};function f(n){throw Error(n)}function s(n){const t=[],e=n.length;let r,u,o,l=null,c=0,i="";function s(){t.push(i+n.substring(r,u)),i="",r=u+1}for(n+="",r=u=0;u<e;++u)if(o=n[u],"\\"===o)i+=n.substring(r,u),i+=n.substring(++u,++u),r=u;else if(o===l)s(),l=null,c=-1;else{if(l)continue;r===c&&'"'===o||r===c&&"'"===o?(r=u+1,l=o):"."!==o||c?"["===o?(u>r&&s(),c=r=u+1):"]"===o&&(c||f("Access path missing open bracket: "+n),c>0&&s(),c=0,r=u+1):u>r?s():r=u+1}return c&&f("Access path missing closing bracket: "+n),l&&f("Access path missing closing quote: "+n),u>r&&(u++,s()),t}function a(n,t,e){const u=s(n);return n=1===u.length?u[0]:n,r((e&&e.get||l)(u),[n],t||n)}const h=a("id"),g=r((n=>n),[],"identity"),p=r((()=>0),[],"zero"),b=r((()=>1),[],"one"),y=r((()=>!0),[],"true"),m=r((()=>!1),[],"false");function j(n,t,e){const r=[t].concat([].slice.call(e));console[n].apply(console,r)}const M=0,d=1,k=2,w=3,E=4;function O(n,t,e=j){let r=n||M;return{level(n){return arguments.length?(r=+n,this):r},error(){return r>=d&&e(t||"error","ERROR",arguments),this},warn(){return r>=k&&e(t||"warn","WARN",arguments),this},info(){return r>=w&&e(t||"log","INFO",arguments),this},debug(){return r>=E&&e(t||"log","DEBUG",arguments),this}}}var v=Array.isArray;function D(n){return n===Object(n)}const _=n=>"__proto__"!==n;function A(...n){return n.reduce(((n,t)=>{for(const e in t)if("signals"===e)n.signals=x(n.signals,t.signals);else{const r="legend"===e?{layout:1}:"style"===e||null;R(n,e,t[e],r)}return n}),{})}function R(n,t,e,r){if(!_(t))return;let u,o;if(D(e)&&!v(e))for(u in o=D(n[t])?n[t]:n[t]={},e)r&&(!0===r||r[u])?R(o,u,e[u]):_(u)&&(o[u]=e[u]);else n[t]=e}function x(n,t){if(null==n)return t;const e={},r=[];function u(n){e[n.name]||(e[n.name]=1,r.push(n))}return t.forEach(u),n.forEach(u),r}function z(n){return n[n.length-1]}function S(n){return null==n||""===n?null:+n}const J=n=>t=>n*Math.exp(t),P=n=>t=>Math.log(n*t),T=n=>t=>Math.sign(t)*Math.log1p(Math.abs(t/n)),U=n=>t=>Math.sign(t)*Math.expm1(Math.abs(t))*n,H=n=>t=>t<0?-Math.pow(-t,n):Math.pow(t,n);function I(n,t,e,r){const u=e(n[0]),o=e(z(n)),l=(o-u)*t;return[r(u-l),r(o-l)]}function N(n,t){return I(n,t,S,g)}function W(n,t){var e=Math.sign(n[0]);return I(n,t,P(e),J(e))}function X(n,t,e){return I(n,t,H(e),H(1/e))}function $(n,t,e){return I(n,t,T(e),U(e))}function q(n,t,e,r,u){const o=r(n[0]),l=r(z(n)),c=null!=t?r(t):(o+l)/2;return[u(c+(o-c)*e),u(c+(l-c)*e)]}function B(n,t,e){return q(n,t,e,S,g)}function C(n,t,e){const r=Math.sign(n[0]);return q(n,t,e,P(r),J(r))}function G(n,t,e,r){return q(n,t,e,H(r),H(1/r))}function K(n,t,e,r){return q(n,t,e,T(r),U(r))}function Z(n){return 1+~~(new Date(n).getMonth()/3)}function F(n){return 1+~~(new Date(n).getUTCMonth()/3)}function L(n){return null!=n?v(n)?n:[n]:[]}function Q(n,t,e){let r,u=n[0],o=n[1];return o<u&&(r=o,o=u,u=r),r=o-u,r>=e-t?[t,e]:[u=Math.min(Math.max(u,t),e-r),u+r]}function V(n){return"function"==typeof n}function Y(n,t,e){e=e||{},t=L(t)||[];const u=[],l=[],c={},i=e.comparator||tn;return L(n).forEach(((n,r)=>{null!=n&&(u.push("descending"===t[r]?-1:1),l.push(n=V(n)?n:a(n,null,e)),(o(n)||[]).forEach((n=>c[n]=1)))})),0===l.length?null:r(i(l,u),Object.keys(c))}const nn=(n,t)=>(n<t||null==n)&&null!=t?-1:(n>t||null==t)&&null!=n?1:(t=t instanceof Date?+t:t,(n=n instanceof Date?+n:n)!==n&&t==t?-1:t!=t&&n==n?1:0),tn=(n,t)=>1===n.length?en(n[0],t[0]):rn(n,t,n.length),en=(n,t)=>function(e,r){return nn(n(e),n(r))*t},rn=(n,t,e)=>(t.push(0),function(r,u){let o,l=0,c=-1;for(;0===l&&++c<e;)o=n[c],l=nn(o(r),o(u));return l*t[c]});function un(n){return V(n)?n:()=>n}function on(n,t){let e;return r=>{e&&clearTimeout(e),e=setTimeout((()=>(t(r),e=null)),n)}}function ln(n){for(let t,e,r=1,u=arguments.length;r<u;++r)for(e in t=arguments[r],t)n[e]=t[e];return n}function cn(n,t){let e,r,u,o,l=0;if(n&&(e=n.length))if(null==t){for(r=n[l];l<e&&(null==r||r!=r);r=n[++l]);for(u=o=r;l<e;++l)r=n[l],null!=r&&(r<u&&(u=r),r>o&&(o=r))}else{for(r=t(n[l]);l<e&&(null==r||r!=r);r=t(n[++l]));for(u=o=r;l<e;++l)r=t(n[l]),null!=r&&(r<u&&(u=r),r>o&&(o=r))}return[u,o]}function fn(n,t){const e=n.length;let r,u,o,l,c,i=-1;if(null==t){for(;++i<e;)if(u=n[i],null!=u&&u>=u){r=o=u;break}if(i===e)return[-1,-1];for(l=c=i;++i<e;)u=n[i],null!=u&&(r>u&&(r=u,l=i),o<u&&(o=u,c=i))}else{for(;++i<e;)if(u=t(n[i],i,n),null!=u&&u>=u){r=o=u;break}if(i===e)return[-1,-1];for(l=c=i;++i<e;)u=t(n[i],i,n),null!=u&&(r>u&&(r=u,l=i),o<u&&(o=u,c=i))}return[l,c]}const sn=Object.prototype.hasOwnProperty;function an(n,t){return sn.call(n,t)}const hn={};function gn(n){let t,e={};function r(n){return an(e,n)&&e[n]!==hn}const u={size:0,empty:0,object:e,has:r,get:n=>r(n)?e[n]:void 0,set(n,t){return r(n)||(++u.size,e[n]===hn&&--u.empty),e[n]=t,this},delete(n){return r(n)&&(--u.size,++u.empty,e[n]=hn),this},clear(){u.size=u.empty=0,u.object=e={}},test(n){return arguments.length?(t=n,u):t},clean(){const n={};let r=0;for(const u in e){const o=e[u];o===hn||t&&t(o)||(n[u]=o,++r)}u.size=r,u.empty=0,u.object=e=n}};return n&&Object.keys(n).forEach((t=>{u.set(t,n[t])})),u}function pn(n,t,e,r,u,o){if(!e&&0!==e)return o;const l=+e;let c,i=n[0],f=z(n);f<i&&(c=i,i=f,f=c),c=Math.abs(t-i);const s=Math.abs(f-t);return c<s&&c<=l?r:s<=l?u:o}function bn(n,t,e){const r=n.prototype=Object.create(t.prototype);return Object.defineProperty(r,"constructor",{value:n,writable:!0,enumerable:!0,configurable:!0}),ln(r,e)}function yn(n,t,e,r){let u,o=t[0],l=t[t.length-1];return o>l&&(u=o,o=l,l=u),r=void 0===r||r,((e=void 0===e||e)?o<=n:o<n)&&(r?n<=l:n<l)}function mn(n){return"boolean"==typeof n}function jn(n){return"[object Date]"===Object.prototype.toString.call(n)}function Mn(n){return n&&V(n[Symbol.iterator])}function dn(n){return"number"==typeof n}function kn(n){return"[object RegExp]"===Object.prototype.toString.call(n)}function wn(n){return"string"==typeof n}function En(n,t,e){n&&(n=t?L(n).map((n=>n.replace(/\\(.)/g,"$1"))):L(n));const u=n&&n.length,o=e&&e.get||l,c=n=>o(t?[n]:s(n));let i;if(u)if(1===u){const t=c(n[0]);i=function(n){return""+t(n)}}else{const t=n.map(c);i=function(n){let e=""+t[0](n),r=0;for(;++r<u;)e+="|"+t[r](n);return e}}else i=function(){return""};return r(i,n,"key")}function On(n,t){const e=n[0],r=z(n),u=+t;return u?1===u?r:e+u*(r-e):e}function vn(n){let t,e,r;n=+n||1e4;const u=()=>{t={},e={},r=0},o=(u,o)=>(++r>n&&(e=t,t={},r=1),t[u]=o);return u(),{clear:u,has:n=>an(t,n)||an(e,n),get:n=>an(t,n)?t[n]:an(e,n)?o(n,e[n]):void 0,set:(n,e)=>an(t,n)?t[n]=e:o(n,e)}}function Dn(n,t,e,r){const u=t.length,o=e.length;if(!o)return t;if(!u)return e;const l=r||new t.constructor(u+o);let c=0,i=0,f=0;for(;c<u&&i<o;++f)l[f]=n(t[c],e[i])>0?e[i++]:t[c++];for(;c<u;++c,++f)l[f]=t[c];for(;i<o;++i,++f)l[f]=e[i];return l}function _n(n,t){let e="";for(;--t>=0;)e+=n;return e}function An(n,t,e,r){const u=e||" ",o=n+"",l=t-o.length;return l<=0?o:"left"===r?_n(u,l)+o:"center"===r?_n(u,~~(l/2))+o+_n(u,Math.ceil(l/2)):o+_n(u,l)}function Rn(n){return n&&z(n)-n[0]||0}function xn(n){return v(n)?"["+n.map(xn)+"]":D(n)||wn(n)?JSON.stringify(n).replace("\u2028","\\u2028").replace("\u2029","\\u2029"):n}function zn(n){return null==n||""===n?null:!(!n||"false"===n||"0"===n||!n)}const Sn=n=>dn(n)||jn(n)?n:Date.parse(n);function Jn(n,t){return t=t||Sn,null==n||""===n?null:t(n)}function Pn(n){return null==n||""===n?null:n+""}function Tn(n){const t={},e=n.length;for(let r=0;r<e;++r)t[n[r]]=!0;return t}function Un(n,t,e,r){const u=null!=r?r:"…",o=n+"",l=o.length,c=Math.max(0,t-u.length);return l<=t?o:"left"===e?u+o.slice(l-c):"center"===e?o.slice(0,Math.ceil(c/2))+u+o.slice(l-~~(c/2)):o.slice(0,c)+u}function Hn(n,t,e){if(n)if(t){const r=n.length;for(let u=0;u<r;++u){const r=t(n[u]);r&&e(r,u,n)}}else n.forEach(e)}}}]);