sap.ui.define([
	"sap/ui/core/mvc/XMLView"
], function (XMLView) {
	"use strict";
	debugger;
    var oView = sap.ui.htmlview({
		viewContent: '<div data-sap-ui-type="sap.m.Page" ><div data-sap-ui-type="data-sap-ui-type="sap.m.content"><div data-sap-ui-type="sap.ui.commons.Button" id="Button2" data-text="Hello"></div></div></div></div>'
	});
	 oView.placeAt('content');

});