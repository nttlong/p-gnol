/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2018 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./InputBase','./DateTimeField','./MaskInputRule','./ResponsivePopover','sap/ui/core/EnabledPropagator','sap/ui/core/IconPool','./TimePickerSliders','./MaskEnabler','sap/ui/Device','sap/ui/core/format/DateFormat','sap/ui/core/Locale','sap/m/library','sap/ui/core/LocaleData','./TimePickerRenderer',"sap/ui/events/KeyCodes","sap/base/Log","sap/ui/core/InvisibleText","sap/ui/thirdparty/jquery"],function(I,D,M,R,E,a,T,b,c,d,L,l,e,f,K,g,h,q){"use strict";var P=l.PlacementType,j=l.TimePickerMaskMode,k=1;var m=D.extend("sap.m.TimePicker",{metadata:{library:"sap.m",designtime:"sap/m/designtime/TimePicker.designtime",properties:{localeId:{type:"string",group:"Data"},title:{type:"string",group:"Misc",defaultValue:null},minutesStep:{type:"int",group:"Misc",defaultValue:k},secondsStep:{type:"int",group:"Misc",defaultValue:k},placeholderSymbol:{type:"string",group:"Misc",defaultValue:"_"},mask:{type:"string",group:"Misc",defaultValue:null},maskMode:{type:"sap.m.TimePickerMaskMode",group:"Misc",defaultValue:j.On},support2400:{type:"boolean",group:"Misc",defaultValue:false}},aggregations:{rules:{type:"sap.m.MaskInputRule",multiple:true,singularName:"rule"},_picker:{type:"sap.m.ResponsivePopover",multiple:false,visibility:"hidden"}}}});a.insertFontFaceStyle();E.call(m.prototype,true);b.call(m.prototype);var n={Short:"short",Medium:"medium",Long:"long"},o={Hour:"hour",Minute:"minute",Second:"second"},p='-';m.prototype.init=function(){D.prototype.init.apply(this,arguments);b.init.apply(this,arguments);this.setDisplayFormat(s());this._oResourceBundle=sap.ui.getCore().getLibraryResourceBundle("sap.m");this._bValid=false;this._sUsedDisplayPattern=null;this._sUsedValuePattern=null;this._oDisplayFormat=null;this._sValueFormat=null;this._oPopoverKeydownEventDelegate=null;this._rPlaceholderRegEx=new RegExp(p,'g');this._sLastChangeValue=null;var i=this.addEndIcon({id:this.getId()+"-icon",src:this.getIconSrc(),noTabStop:true,title:""});this._bShouldClosePicker=false;i.addEventDelegate({onmousedown:function(t){this._bShouldClosePicker=this.isOpen();}},this);i.attachPress(function(){this.toggleOpen(this._bShouldClosePicker);},this);};m.prototype.onBeforeRendering=function(){D.prototype.onBeforeRendering.apply(this,arguments);var v=this._getValueHelpIcon();if(v){v.setProperty("visible",this.getEnabled(),true);}};m.prototype.exit=function(){if(this._oTimeSemanticMaskHelper){this._oTimeSemanticMaskHelper.destroy();}b.exit.apply(this,arguments);this._removePickerEvents();this._oResourceBundle=null;this._bValid=false;this._sUsedDisplayPattern=null;this._oDisplayFormat=null;this._oPopoverKeydownEventDelegate=null;this._sUsedValuePattern=null;this._sValueFormat=null;this._sLastChangeValue=null;};m.prototype.getIconSrc=function(){return a.getIconURI("time-entry-request");};m.prototype.isOpen=function(){return this._getPicker()&&this._getPicker().isOpen();};m.prototype.toggleOpen=function(O){this[O?"_closePicker":"_openPicker"]();};m.prototype.onfocusin=function(i){var t=this._getPicker();var u=this._isIconClicked(i);b.onfocusin.apply(this,arguments);if(t&&t.isOpen()&&!u){this._closePicker();}};m.prototype._isIconClicked=function(i){return q(i.target).hasClass("sapUiIcon")||q(i.target).hasClass("sapMInputBaseIconContainer");};m.prototype.onBeforeOpen=function(){var S=this._getSliders(),i=this.getDateValue(),t=this._$input.val(),F=this.getValueFormat(),u=F.indexOf("HH"),v=F.indexOf("H");S.setValue(t);if(this._shouldSetInitialFocusedDateValue()){i=this.getInitialFocusedDateValue();}S._setTimeValues(i,T._isHoursValue24(t,u,v));S.collapseAll();this.$().addClass(I.ICON_PRESSED_CSS_CLASS);};m.prototype.onAfterOpen=function(){var S=this._getSliders();if(S){S.openFirstSlider();this._handleAriaOnExpandCollapse();}};m.prototype.onAfterClose=function(){this.$().removeClass(I.ICON_PRESSED_CSS_CLASS);this._handleAriaOnExpandCollapse();};m.prototype._getValueHelpIcon=function(){var v=this.getAggregation("_endIcon");return v&&v[0];};m.prototype._handleInputChange=function(v){var i,t,u,F=this.getValueFormat(),w=F.indexOf("HH"),x=F.indexOf("H");v=v||this._$input.val();t=v;u=T._isHoursValue24(t,w,x);this._bValid=true;if(v!==""){i=this._parseValue(T._isHoursValue24(v,w,x)?T._replace24HoursWithZero(v,w,x):v,true);if(!i){this._bValid=false;}else{v=this._formatValue(i);}}t=this.getSupport2400()&&u?"24:"+v.replace(/[0-9]/g,"0").slice(0,-3):v;this.updateDomValue(t);if(i){t=v=this._formatValue(i,true);}this.setProperty("value",t,true);this._lastValue=v;if(this._bValid){this.setProperty("dateValue",i,true);}this.fireChangeEvent(t,{valid:this._bValid});return true;};m.prototype.onChange=function(i){var v=i?i.value:null;if(this.getEditable()&&this.getEnabled()){return this._handleInputChange(v);}return false;};m.prototype.setMinutesStep=function(i){var S=this._getSliders();i=Math.max(k,i||k);if(S){S.setMinutesStep(i);}return this.setProperty("minutesStep",i,true);};m.prototype.setSecondsStep=function(i){var S=this._getSliders();i=Math.max(k,i||k);if(S){S.setSecondsStep(i);}return this.setProperty("secondsStep",i,true);};m.prototype.setTitle=function(t){var S=this._getSliders();if(S){S.setLabelText(t);}this.setProperty("title",t,true);return this;};m.prototype._handleDateValidation=function(i){if(!i){this._bValid=false;g.warning("Value can not be converted to a valid date",this);}else{this._bValid=true;this.setProperty("dateValue",i,true);var v=this._formatValue(i);if(this.isActive()){this.updateDomValue(v);}else{this.setProperty("value",v,true);this._lastValue=v;this._sLastChangeValue=v;}}};m.prototype.setSupport2400=function(S){var i=this._getSliders();this.setProperty("support2400",S,true);if(i){i.setSupport2400(S);}this._initMask();return this;};m.prototype.setDisplayFormat=function(i){var S=this._getSliders();this.setProperty("displayFormat",i,true);this._initMask();if(S){S.setDisplayFormat(i);}var t=this.getDateValue();if(!t){return this;}var O=this._formatValue(t);this.updateDomValue(O);this._lastValue=O;return this;};m.prototype.setValue=function(v){var i,O,F=this.getValueFormat(),t=F.indexOf("HH"),u=F.indexOf("H"),S=this._getSliders();v=this.validateProperty("value",v);this._initMask();b.setValue.call(this,v);this._sLastChangeValue=v;this._bValid=true;if(v){i=this._parseValue(T._isHoursValue24(v,t,u)?T._replace24HoursWithZero(v,t,u):v);if(!i){this._bValid=false;g.warning("Value can not be converted to a valid date",this);}}if(this._bValid){this.setProperty("dateValue",i,true);}if(i&&!this.getSupport2400()){O=this._formatValue(i);}else{O=v;}if(S){S.setValue(v);}this.updateDomValue(O);this._lastValue=O;return this;};m.prototype.setTooltip=function(t){var i=this.getDomRef(),u;this._refreshTooltipBaseDelegate(t);this.setAggregation("tooltip",t,true);if(!i){return this;}u=this.getTooltip_AsString();if(u){i.setAttribute("title",u);}else{i.removeAttribute("title");}this._handleTooltipHiddenTextLifecycle();return this;};m.prototype._handleTooltipHiddenTextLifecycle=function(){var i,t,A,H,C,u;if(!sap.ui.getCore().getConfiguration().getAccessibility()){return;}i=this.getRenderer();t=i.getAriaDescribedBy(this);A=i.getDescribedByAnnouncement(this);H=this.getId()+"-describedby";C=t.indexOf(H)>-1;u=this.getDomRef("describedby");if(C){u=document.createElement("span");u.id=H;u.setAttribute("aria-hidden","true");u.className="sapUiInvisibleText";u.textContent=A;this.getDomRef().appendChild(u);}else{this.getDomRef().removeChild(u);}this._$input.attr("aria-describedby",t);};m.prototype.setLocaleId=function(i){var C=this.getValue(),S=this._getSliders();this.setProperty("localeId",i,true);this._initMask();this._oDisplayFormat=null;this._sValueFormat=null;if(C){this.setValue(C);}if(S){S.setLocaleId(i);}return this;};m.prototype._getDefaultDisplayStyle=function(){return n.Medium;};m.prototype._getDefaultValueStyle=function(){return n.Medium;};m.prototype._getLocale=function(){var i=this.getLocaleId();return i?new L(i):sap.ui.getCore().getConfiguration().getFormatSettings().getFormatLocale();};m.prototype._getFormatterInstance=function(F,i,t,C,u){var v=this._getLocale();if(i===n.Short||i===n.Medium||i===n.Long){F=d.getTimeInstance({style:i,strictParsing:true,relative:t},v);}else{F=d.getTimeInstance({pattern:i,strictParsing:true,relative:t},v);}if(u){this._sUsedDisplayPattern=i;this._oDisplayFormat=F;}else{this._sUsedValuePattern=i;this._sValueFormat=F;}return F;};m.prototype._getFormat=function(){var F=this._getDisplayFormatPattern();if(!F){F=n.Medium;}if(Object.keys(n).indexOf(F)!==-1){F=s();}return F;};m.prototype.onsappageup=function(i){this._increaseTime(1,o.Hour);i.preventDefault();};m.prototype.onsappageupmodifiers=function(i){if(!(i.ctrlKey||i.metaKey||i.altKey)&&i.shiftKey){this._increaseTime(1,o.Minute);}if(!i.altKey&&i.shiftKey&&(i.ctrlKey||i.metaKey)){this._increaseTime(1,o.Second);}i.preventDefault();};m.prototype.onsappagedown=function(i){this._increaseTime(-1,o.Hour);i.preventDefault();};m.prototype.onsappagedownmodifiers=function(i){if(!(i.ctrlKey||i.metaKey||i.altKey)&&i.shiftKey){this._increaseTime(-1,o.Minute);}if(!i.altKey&&i.shiftKey&&(i.ctrlKey||i.metaKey)){this._increaseTime(-1,o.Second);}i.preventDefault();};m.prototype.onkeydown=function(i){var t=K,u=i.which||i.keyCode,A=i.altKey,v;if(u===t.F4||(A&&(u===t.ARROW_UP||u===t.ARROW_DOWN))){v=this._getPicker()&&this._getPicker().isOpen();if(!v){this._openPicker();}else{this._closePicker();}i.preventDefault();}else{b.onkeydown.call(this,i);}};m.prototype._getPicker=function(){return this.getAggregation("_picker");};m.prototype._removePickerEvents=function(){var i,t=this._getPicker();if(t){i=t.getAggregation("_popup");if(typeof this._oPopoverKeydownEventDelegate==='function'){i.removeEventDelegate(this._oPopoverKeydownEventDelegate);}}};m.prototype._openPicker=function(){var i=this._getPicker(),S;if(!i){i=this._createPicker(this._getDisplayFormatPattern());}i.open();S=this._getSliders();setTimeout(S._updateSlidersValues.bind(S),0);return i;};m.prototype._closePicker=function(){var i=this._getPicker();if(i){i.close();}else{g.warning("There is no picker to close.");}return i;};m.prototype._createPicker=function(F){var t=this,i,u,v,O,C,w,x=this.getAggregation("_endIcon")[0],y=this._getLocale().getLanguage();v=sap.ui.getCore().getLibraryResourceBundle("sap.m");O=v.getText("TIMEPICKER_SET");C=v.getText("TIMEPICKER_CANCEL");w=this.getTitle();u=new R(t.getId()+"-RP",{showCloseButton:false,showHeader:false,horizontalScrolling:false,verticalScrolling:false,placement:P.VerticalPreferedBottom,beginButton:new sap.m.Button({text:O,press:q.proxy(this._handleOkPress,this)}),endButton:new sap.m.Button({text:C,press:q.proxy(this._handleCancelPress,this)}),content:[new T(this.getId()+"-sliders",{support2400:this.getSupport2400(),displayFormat:F,valueFormat:this.getValueFormat(),labelText:w?w:"",localeId:y,minutesStep:this.getMinutesStep(),secondsStep:this.getSecondsStep()})._setShouldOpenSliderAfterRendering(true)],contentHeight:m._PICKER_CONTENT_HEIGHT,ariaLabelledBy:h.getStaticId("sap.m","TIMEPICKER_SET_TIME")});i=u.getAggregation("_popup");if(i.setShowArrow){i.setShowArrow(false);}i.oPopup.setAutoCloseAreas([x]);u.addStyleClass(this.getRenderer().CSS_CLASS+"DropDown").attachBeforeOpen(this.onBeforeOpen,this).attachAfterOpen(this.onAfterOpen,this).attachAfterClose(this.onAfterClose,this);u.open=function(){return this.openBy(t);};if(c.system.desktop){this._oPopoverKeydownEventDelegate={onkeydown:function(z){var A=K,B=z.which||z.keyCode,G=z.altKey;if((G&&(B===A.ARROW_UP||B===A.ARROW_DOWN))||B===A.F4){this._handleOkPress(z);this.focus();z.preventDefault();}}};i.addEventDelegate(this._oPopoverKeydownEventDelegate,this);i._afterAdjustPositionAndArrowHook=function(){t._getSliders()._onOrientationChanged();};}this.setAggregation("_picker",u,true);return u;};m.prototype._getSliders=function(){var i=this._getPicker();if(!i){return null;}return i.getContent()[0];};m.prototype._handleOkPress=function(i){var t=this._getSliders().getTimeValues(),v=this._formatValue(t);if(this.getSupport2400()){v=this._getSliders().getValue();}this.updateDomValue(v);this._handleInputChange();this._closePicker();};m.prototype._handleCancelPress=function(i){this._closePicker();};m.prototype._getLocaleBasedPattern=function(i){return e.getInstance(sap.ui.getCore().getConfiguration().getFormatSettings().getFormatLocale()).getTimePattern(i);};m.prototype._parseValue=function(v,i){if(i){v=this._oTimeSemanticMaskHelper.stripValueOfLeadingSpaces(v);v=v.replace(this._rPlaceholderRegEx,'');}return D.prototype._parseValue.call(this,v,i);};m.prototype._formatValue=function(i,v){var V=D.prototype._formatValue.apply(this,arguments),F=this.getValueFormat(),t=F.indexOf("HH"),u=F.indexOf("H");if(i){if(!v&&this._oTimeSemanticMaskHelper){V=this._oTimeSemanticMaskHelper.formatValueWithLeadingTrailingSpaces(V);}}if(this.getSupport2400()&&T._isHoursValue24(this.getValue(),t,u)&&T._replaceZeroHoursWith24(V,t,u)===this.getValue()){V=this.getValue();}return V;};m.prototype._handleAriaOnExpandCollapse=function(){this.getFocusDomRef().setAttribute("aria-expanded",this._getPicker().isOpen());};m.prototype._increaseTime=function(N,u){var O=this.getDateValue(),i,t;if(O&&this.getEditable()&&this.getEnabled()){i=new Date(O.getTime());switch(u){case o.Hour:i.setHours(i.getHours()+N);t=60*60*1000;break;case o.Minute:i.setMinutes(i.getMinutes()+N);t=60*1000;break;case o.Second:t=1000;i.setSeconds(i.getSeconds()+N);}if(N<0&&i.getTime()-O.getTime()!==N*t){i=new Date(O.getTime()+N*t);}this.setDateValue(i);this.fireChangeEvent(this.getValue(),{valid:true});}};m.prototype._initMask=function(){if(this._oTimeSemanticMaskHelper){this._oTimeSemanticMaskHelper.destroy();}this._oTimeSemanticMaskHelper=new r(this);};m.prototype._isMaskEnabled=function(){return this.getMaskMode()===j.On;};m.prototype._shouldSetInitialFocusedDateValue=function(){if(!this._isValidValue()){return true;}return!this.getValue()&&!!this.getInitialFocusedDateValue();};m.prototype._isValidValue=function(){return this._bValid;};m.prototype.fireChangeEvent=function(v,i){if(v){v=v.trim();}if(v!==this._sLastChangeValue){this._sLastChangeValue=v;I.prototype.fireChangeEvent.call(this,v,i);}};var r=function(t){var u=t._getDisplayFormatPattern(),v,A,w=t._getLocale(),i;if(t._checkStyle(u)){v=e.getInstance(w).getTimePattern(u);}else{u=u.replace(/'/g,"");v=u;}this._oTimePicker=t;this.aOriginalAmPmValues=e.getInstance(w).getDayPeriods("abbreviated");this.aAmPmValues=this.aOriginalAmPmValues.slice(0);this.iAmPmValueMaxLength=Math.max(this.aAmPmValues[0].length,this.aAmPmValues[1].length);for(i=0;i<this.aAmPmValues.length;i++){while(this.aAmPmValues[i].length<this.iAmPmValueMaxLength){this.aAmPmValues[i]+=" ";}}this.b24H=u.indexOf("H")!==-1;this.bLeadingZero=u.indexOf("HH")!==-1||u.indexOf("hh")!==-1;this.sLeadingChar=this.bLeadingZero?"0":" ";this.sAlternativeLeadingChar=this.bLeadingZero?" ":"0";this.sLeadingRegexChar=this.bLeadingZero?"0":"\\s";t.setPlaceholderSymbol(p);v=v.replace(/hh/ig,"h").replace(/h/ig,"h9");if(this.b24H){A="["+this.sLeadingRegexChar+"012]";}else{A="["+this.sLeadingRegexChar+"1]";}this._maskRuleHours=new M({maskFormatSymbol:"h",regex:A});t.addRule(this._maskRuleHours);this.iHourNumber1Index=v.indexOf("h9");this.iHourNumber2Index=this.iHourNumber1Index!==-1?this.iHourNumber1Index+1:-1;this.iMinuteNumber1Index=v.indexOf("mm");v=v.replace(/mm/g,"59");this.iSecondNumber1Index=v.indexOf("ss");v=v.replace(/ss/g,"59");this._maskRuleMinSec=new M({maskFormatSymbol:"5",regex:"[0-5]"});t.addRule(this._maskRuleMinSec);this.aAllowedHours=G.call(this,this.b24H,this.sLeadingChar);this.aAllowedMinutesAndSeconds=H.call(this);this.iAmPmChar1Index=v.indexOf("a");this.iAfterAmPmValueIndex=-1;if(this.iAmPmChar1Index!==-1){this.iAfterAmPmValueIndex=this.iAmPmChar1Index+this.iAmPmValueMaxLength;var C=this.iAmPmValueMaxLength-"a".length;this.shiftIndexes(C);var x=65;var y="";var z="";var B="";for(i=0;i<this.iAmPmValueMaxLength;i++){z="[";if(this.aAmPmValues[0][i]){z+=this.aAmPmValues[0][i];}else{z+="\\s";}if(this.aAmPmValues[1][i]!==this.aAmPmValues[0][i]){if(this.aAmPmValues[1][i]){z+=this.aAmPmValues[1][i];}else{z+="\\s";}}z+="]";B=String.fromCharCode(x++);y+=B;this._maskRuleChars=new M({maskFormatSymbol:B,regex:z});t.addRule(this._maskRuleChars);}v=v.replace(/a/g,y);}t.setMask(v);function F(S,J,N){var O=[],Q,i;for(i=S;i<=J;i++){Q=i.toString();if(i<10){Q=N+Q;}O.push(Q);}return O;}function G(J,N){var S=J?0:1,O=this._oTimePicker.getSupport2400()?24:23,Q=J?O:12;return F(S,Q,N);}function H(){return F(0,59,"0");}};r.prototype.replaceChar=function(C,t,u){var A=t-this.iAmPmChar1Index,v,w,x,S,y,z,i;if(t===this.iHourNumber1Index&&this.sAlternativeLeadingChar===C){if(this.aAllowedHours.indexOf(this.sLeadingChar+C)!==-1){return this.sLeadingChar+C;}else{return this.sLeadingChar;}}else if(t===this.iHourNumber1Index&&!this._oTimePicker._isCharAllowed(C,t)&&this.aAllowedHours.indexOf(this.sLeadingChar+C)!==-1){return this.sLeadingChar+C;}else if(t===this.iHourNumber2Index&&this.aAllowedHours.indexOf(u[this.iHourNumber1Index]+C)===-1){return"";}else if((t===this.iMinuteNumber1Index||t===this.iSecondNumber1Index)&&!this._oTimePicker._isCharAllowed(C,t)&&this.aAllowedMinutesAndSeconds.indexOf("0"+C)!==-1){return"0"+C;}else if(A>=0&&t<this.iAfterAmPmValueIndex){v=u.slice(this.iAmPmChar1Index,t);w=this.aAmPmValues[0].slice(0,A);x=this.aAmPmValues[1].slice(0,A);y=this.aAmPmValues[0].slice(A,this.iAfterAmPmValueIndex);z=this.aAmPmValues[1].slice(A,this.iAfterAmPmValueIndex);S=(w===x);var B="";for(i=A;i<this.iAmPmValueMaxLength;i++){if(this.aAmPmValues[0][i]===this.aAmPmValues[1][i]){B+=this.aAmPmValues[0][i];}else{break;}}if(i===this.iAmPmValueMaxLength||i!==A){return B;}else{if(!S){if(v===w){return y;}else if(v===x){return z;}else{return C;}}else{if(this.aAmPmValues[0][A].toLowerCase()===C.toLowerCase()&&this.aAmPmValues[0]===v+y){return y;}else if(this.aAmPmValues[1][A].toLowerCase()===C.toLowerCase()&&this.aAmPmValues[1]===v+z){return z;}else{return C;}}}}else{return C;}};r.prototype.formatValueWithLeadingTrailingSpaces=function(v){var i=this._oTimePicker.getMask().length;if(this.aOriginalAmPmValues[0]!==this.aAmPmValues[0]){v=v.replace(this.aOriginalAmPmValues[0],this.aAmPmValues[0]);}if(this.aOriginalAmPmValues[1]!==this.aAmPmValues[1]){v=v.replace(this.aOriginalAmPmValues[1],this.aAmPmValues[1]);}while(i>v.length){v=[v.slice(0,this.iHourNumber1Index)," ",v.slice(this.iHourNumber1Index)].join('');}return v;};r.prototype.stripValueOfLeadingSpaces=function(v){if(v[this.iHourNumber1Index]===" "){v=[v.slice(0,this.iHourNumber1Index),v.slice(this.iHourNumber1Index+1)].join('');}return v;};r.prototype.shiftIndexes=function(i){if(this.iAmPmChar1Index<this.iHourNumber1Index){this.iHourNumber1Index+=i;this.iHourNumber2Index+=i;}if(this.iAmPmChar1Index<this.iMinuteNumber1Index){this.iMinuteNumber1Index+=i;}if(this.iAmPmChar1Index<this.iSecondNumber1Index){this.iSecondNumber1Index+=i;}};r.prototype.destroy=function(){if(this._maskRuleHours){this._maskRuleHours.destroy();this._maskRuleHours=null;}if(this._maskRuleMinSec){this._maskRuleMinSec.destroy();this._maskRuleMinSec=null;}if(this._maskRuleChars){this._maskRuleChars.destroy();this._maskRuleChars=null;}};m.prototype._feedReplaceChar=function(C,i,t){return this._oTimeSemanticMaskHelper.replaceChar(C,i,t);};m.prototype._getAlteredUserInputValue=function(v){return v?this._formatValue(this._parseValue(v),true):v;};m.prototype.getAccessibilityInfo=function(){var i=this.getRenderer();var t=I.prototype.getAccessibilityInfo.apply(this,arguments);var v=this.getValue()||"";if(this._bValid){var u=this.getDateValue();if(u){v=this._formatValue(u);}}q.extend(true,t,{role:i.getAriaRole(this),type:sap.ui.getCore().getLibraryResourceBundle("sap.m").getText("ACC_CTR_TYPE_TIMEINPUT"),description:[v,i.getLabelledByAnnouncement(this),i.getDescribedByAnnouncement(this)].join(" ").trim(),multiline:false,autocomplete:"none",expanded:false,haspopup:true,owns:this.getId()+"-sliders"});return t;};function s(){var i=sap.ui.getCore().getConfiguration().getFormatSettings().getFormatLocale(),t=e.getInstance(i);return t.getTimePattern(n.Medium);}m._PICKER_CONTENT_HEIGHT="25rem";return m;});
