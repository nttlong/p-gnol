/*!
* UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2018 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
*/
sap.ui.define(["jquery.sap.global","sap/ui/base/ManagedObject","sap/base/Log","sap/ui/core/Locale","sap/ui/core/LocaleData"],function(q,M,L,a,b){"use strict";var t={"bg":"непротивоконституционствувателствувайте","ca":"Psiconeuroimmunoendocrinologia","hr":"prijestolonasljednikovičičinima","cs":"nejnezdevětadevadesáteronásobitelnějšími","da":"Gedebukkebensoverogundergeneralkrigskommandersergenten","nl":"meervoudigepersoonlijkheidsstoornissen","en-us":"pneumonoultramicroscopicsilicovolcanoconiosis","et":"Sünnipäevanädalalõpupeopärastlõunaväsimus","fi":"kolmivaihekilowattituntimittari","fr":"hippopotomonstrosesquippedaliophobie","de":"Kindercarnavalsoptochtvoorbereidingswerkzaamhedenplan","el-monoton":"ηλεκτροεγκεφαλογράφημα","hi":"किंकर्तव्यविमूढ़","hu":"Megszentségteleníthetetlenségeskedéseitekért","it":"hippopotomonstrosesquippedaliofobia","lt":"nebeprisikiškiakopūstlapiaujančiuosiuose","nb-no":"supercalifragilisticexpialidocious","pl":"dziewięćdziesięciokilkuletniemu","pt":"pneumoultramicroscopicossilicovulcanoconiose","ru":"превысокомногорассмотрительствующий","sr":"Семпаравиливичинаверсаламилитипиковски","sl":"Dialektičnomaterialističen","es":"Electroencefalografistas","sv":"Realisationsvinstbeskattning","th":"ตัวอย่างข้อความที่จะใช้ในการยืนยันการถ่ายโอน","tr":"Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine","uk":"Нікотинамідаденіндинуклеотидфосфат"};var T={'bg':true,'ca':true,'hr':true,'cs':false,
// no valid license
'da':true,'nl':true,'en-us':true,'et':true,'fi':true,'fr':true,'de':true,'el-monoton':true,'hi':true,'hu':true,'it':true,'lt':true,'nb-no':true,'pl':false,'pt':true,'ru':true,'sr':false,'sl':true,'es':true,'sv':true,'th':true,'tr':true,'uk':true};var l={"bg":"Bulgarian","ca":"Catalan","hr":"Croatian","cs":"Czech","da":"Danish","nl":"Dutch","en":"English","et":"Estonian","fi":"Finnish","fr":"French","de":"German","el":"Greek","hi":"Hindi","hu":"Hungarian","it":"Italian","lt":"Lithuanian","nb":"Norwegian Bokmål","no":"Norwegian","pl":"Polish","pt":"Portuguese","ru":"Russian","sr":"Serbian","sl":"Slovenian","es":"Spanish","sv":"Swedish","th":"Thai","tr":"Turkish","uk":"Ukrainian"};var B={};var s={};var o={};var h=null;var f=null;var H={};var p={};var c=[];function i(A,C,D){L.info("[UI5 Hyphenation] Initializing third-party module for language "+x(A),"sap.ui.core.hyphenation.Hyphenation.initialize()");window.hyphenopoly.initializeLanguage(C).then(d.bind(this,A,D));}function r(A,C,D){L.info("[UI5 Hyphenation] Re-initializing third-party module for language "+x(A),"sap.ui.core.hyphenation.Hyphenation.initialize()");window.hyphenopoly.reInitializeLanguage(A,C).then(d.bind(this,A,D));}function d(A,C,D){H[A]=D;h.bIsInitialized=true;if(c.length>0){c.forEach(function(E){i(E.sLanguage,E.oConfig,E.resolve);});c=[];}h.bLoading=false;C(w(A));}function e(A,C){var D={"require":[A],"hyphen":"\u00AD","compound":"all","path":q.sap.getResourcePath("sap/ui/thirdparty/hyphenopoly")};if(C){if("hyphen"in C){D.hyphen=C.hyphen;}if("minWordLength"in C){D.minWordLength=C.minWordLength;}if("exceptions"in C){L.info("[UI5 Hyphenation] Add hyphenation exceptions '"+JSON.stringify(C.exceptions)+"' for language "+x(A),"sap.ui.core.hyphenation.Hyphenation");var W=[];Object.keys(C.exceptions).forEach(function(E){W.push(C.exceptions[E]);});if(W.length>0){D.exceptions={};D.exceptions[A]=W.join(", ");}}}return D;}function g(P,F){return new Promise(function(A,C){var D=document.createElement('script');D.async=true;D.src=P+F;D.addEventListener('load',A);D.addEventListener('error',function(){return C('Error loading script: '+F);});D.addEventListener('abort',function(){return C(F+' Script loading aborted.');});document.head.appendChild(D);});}var j=(function createCss(){var A=["visibility:hidden;","-moz-hyphens:auto;","-webkit-hyphens:auto;","-ms-hyphens:auto;","hyphens:auto;","width:48px;","font-size:12px;","line-height:12px;","border:none;","padding:0;","word-wrap:normal"];return A.join("");}());function k(A){if(!f){f=document.createElement("body");}var C=document.createElement("div");C.lang=A;C.id=A;C.style.cssText=j;C.appendChild(document.createTextNode(t[A]));f.appendChild(C);}function m(A){if(f){A.appendChild(f);return f;}return null;}function n(){if(f){f.parentNode.removeChild(f);}}function u(E){return(E.style.hyphens==="auto"||E.style.webkitHyphens==="auto"||E.style.msHyphens==="auto"||E.style["-moz-hyphens"]==="auto");}function v(A){var C;if(A){C=new a(A);}else{C=sap.ui.getCore().getConfiguration().getLocale();}var D=C.getLanguage().toLowerCase();switch(D){case"en":D="en-us";break;case"nb":D="nb-no";break;case"no":D="nb-no";break;case"el":D="el-monoton";break;}return D;}function w(P){if(typeof P==="string"){return P.substring(0,2);}else{return null;}}function x(P){var A=w(P);if(l.hasOwnProperty(A)){return"'"+l[A]+"' (code:'"+A+"')";}else{return"'"+A+"'";}}function y(E){h.fireError(E);L.error("[UI5 Hyphenation] "+E,"sap.ui.core.hyphenation.Hyphenation");h.bLoading=false;}var z=M.extend("sap.ui.core.hyphenation.Hyphenation",{metadata:{library:"sap.ui.core",events:{error:{parameters:{sErrorMessage:{type:"string"}}}}}});z.prototype.canUseNativeHyphenation=function(A){var C=v(A);var D;if(!this.isLanguageSupported(A)){return null;}if(!B.hasOwnProperty(C)){k(C);var E=m(document.documentElement);if(E!==null){var F=document.getElementById(C);if(u(F)&&F.offsetHeight>12){D=true;}else{D=false;}n();}B[C]=D;if(D){L.info("[UI5 Hyphenation] Browser-native hyphenation can be used for language "+x(C),"sap.ui.core.hyphenation.Hyphenation.canUseNativeHyphenation()");}else{L.info("[UI5 Hyphenation] Browser-native hyphenation is not supported by current platform for language "+x(C),"sap.ui.core.hyphenation.Hyphenation.canUseNativeHyphenation()");}}else{D=B[C];}return D;};z.prototype.canUseThirdPartyHyphenation=function(A){var C=v(A),D;if(!this.isLanguageSupported(A)){return null;}if(!o.hasOwnProperty(C)){D=T.hasOwnProperty(C)&&T[C];if(D){L.info("[UI5 Hyphenation] Third-party hyphenation can be used for language "+x(C),"sap.ui.core.hyphenation.Hyphenation.canUseThirdPartyHyphenation()");}else{L.info("[UI5 Hyphenation] Third-party hyphenation is not supported for language "+x(C),"sap.ui.core.hyphenation.Hyphenation.canUseThirdPartyHyphenation()");}o[C]=D;}else{D=o[C];}return D;};z.prototype.isLanguageSupported=function(A){var C=v(A),I;if(!s.hasOwnProperty(C)){I=t.hasOwnProperty(C);if(!I){L.info("[UI5 Hyphenation] Language "+x(C)+" is not known to the Hyphenation API","sap.ui.core.hyphenation.Hyphenation.isLanguageSupported()");}s[C]=I;}else{I=s[C];}return I;};z.prototype.hyphenate=function(A,C){var D=v(C);if(!H.hasOwnProperty(D)){y("Language "+x(D)+" is not initialized. You have to initialize it first with method 'initialize()'");return A;}return H[D](A);};z.prototype.getInitializedLanguages=function(){return Object.keys(H).map(function(A){return w(A);});};z.prototype.isLanguageInitialized=function(A){var A=v(A);return Object.keys(H).indexOf(A)!=-1;};z.prototype.getExceptions=function(A){var A=v(A);if(this.isLanguageInitialized(A)){return window.hyphenopoly.languages[A].exceptions;}else{y("Language "+x(A)+" is not initialized. You have to initialize it first with method 'initialize()'");}};z.prototype.addExceptions=function(A,E){var A=v(A);if(this.isLanguageInitialized(A)){L.info("[UI5 Hyphenation] Add hyphenation exceptions '"+JSON.stringify(E)+"' for language "+x(A),"sap.ui.core.hyphenation.Hyphenation.addExceptions()");Object.keys(E).forEach(function(C){window.hyphenopoly.languages[A].cache[C]=E[C];window.hyphenopoly.languages[A].exceptions[C]=E[C];});}else{y("Language "+x(A)+" is not initialized. You have to initialize it first with method 'initialize()'");}};z.prototype.initialize=function(A,C){var D=v(A);var C=e(D,C);if(T[D]){if(!h.bIsInitialized&&!h.bLoading){h.bLoading=true;p[D]=new Promise(function(F,G){g(C.path,"/hyphenopoly.bundle.js").then(i.bind(this,D,C,F));});return p[D];}else if(h.bLoading&&!H[D]&&p[D]){return p[D];}else if(this.isLanguageInitialized(D)){p[D]=new Promise(function(F,G){r(D,C,F);});}else{p[D]=new Promise(function(F,G){if(!h.bIsInitialized){c.push({sLanguage:D,oConfig:C,resolve:F});}else{i(D,C,F);}});}h.bLoading=true;return p[D];}else{var E="Language "+x(A)+" can not be initialized. It is either not supported by the third-party module or an error occurred";y(E);return new Promise(function(F,G){G(E);});}};z.getInstance=function(){if(!h){h=new z();h.bIsInitialized=false;h.bLoading=false;}return h;};return z;});
