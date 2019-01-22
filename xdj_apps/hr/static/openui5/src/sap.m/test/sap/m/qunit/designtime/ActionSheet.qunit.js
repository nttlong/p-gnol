sap.ui.define([
	"sap/ui/qunit/utils/createAndAppendDiv",
	"sap/m/Button",
	"sap/ui/dt/test/report/QUnit",
	"sap/ui/dt/test/ElementEnablementTest",
	"sap/m/ActionSheet",
	"sap/m/Text",
	"sap/ui/rta/test/controlEnablingCheck"
], function(createAndAppendDiv, Button, QUnitReport, ElementEnablementTest, ActionSheet, Text, rtaControlEnablingCheck) {
	"use strict";
	createAndAppendDiv("content");

	var oElementEnablementTest = new ElementEnablementTest({
		type: "sap.m.ActionSheet",
		create: function () {
			return new ActionSheet("sheet", {
				buttons: [
					new Button({ text: "text1" }),
					new Button({ text: "text2" }),
					new Button({ text: "text3" })
				]
			});
		}
	});

	return oElementEnablementTest.run()

	.then(function (oData) {
		new QUnitReport({
			data: oData
		});
	})

	.then(function() {
		// Move action
		var fnConfirmElement1IsOn3rdPosition = function (oUiComponent, oViewAfterAction, assert) {
			assert.strictEqual(oViewAfterAction.byId("button1").getId(),
				oViewAfterAction.byId("sheet").getButtons()[2].getId(),
				"then the control has been moved to the right position");
		};
		var fnConfirmElement1IsOn1stPosition = function (oUiComponent, oViewAfterAction, assert) {
			assert.strictEqual(oViewAfterAction.byId("button1").getId(),
				oViewAfterAction.byId("sheet").getButtons()[0].getId(),
				"then the control has been moved to the previous position");
		};

		rtaControlEnablingCheck("Checking the move action for ActionSheet control", {
			xmlView:
			'<mvc:View xmlns:mvc="sap.ui.core.mvc" xmlns="sap.m">' +
				'<ActionSheet id="sheet">' +
					'<Button id="button1" />' +
					'<Button id="button2" />' +
					'<Button id="button3" />' +
				'</ActionSheet>' +
			'</mvc:View>'
			,
			action: {
				name: "move",
				controlId: "sheet",
				parameter: function (oView) {
					return {
						movedElements: [{
							element: oView.byId("button1"),
							sourceIndex: 0,
							targetIndex: 2
						}],
						source: {
							aggregation: "buttons",
							parent: oView.byId("sheet"),
							publicAggregation: "buttons",
							publicParent: oView.byId("sheet")
						},
						target: {
							aggregation: "buttons",
							parent: oView.byId("sheet"),
							publicAggregation: "buttons",
							publicParent: oView.byId("sheet")
						}
					};
				}
			},
			afterAction: fnConfirmElement1IsOn3rdPosition,
			afterUndo: fnConfirmElement1IsOn1stPosition,
			afterRedo: fnConfirmElement1IsOn3rdPosition
		});
	});
});
