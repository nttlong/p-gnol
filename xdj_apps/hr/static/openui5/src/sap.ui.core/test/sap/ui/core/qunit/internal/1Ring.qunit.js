/*!
 * ${copyright}
 */
/*global QUnit */

QUnit.config.autostart = false;

// Note: to cover "sap/ui/base", this MUST happen after "qunit-coverage.js" is included!
sap.ui.require([
	"sap/ui/core/Core"
], function (Core) {
	"use strict";

	Core.boot();

	// Note: cannot require these above as data-sap-ui-resourceroots is ignored until boot
	sap.ui.require([
		// alphabetic sort order according to module names
		// base
		"sap/ui/core/qunit/BindingParser.qunit",
		"sap/ui/core/qunit/ExpressionParser.qunit",
		"sap/ui/core/qunit/util/SyncPromise.qunit",
		// core
		"sap/ui/core/qunit/util/XMLPreprocessor.qunit",
		// OData types
		"sap/ui/core/qunit/odata/type/Boolean.qunit",
		"sap/ui/core/qunit/odata/type/Date.qunit",
		"sap/ui/core/qunit/odata/type/DateTimeBase.qunit",
		"sap/ui/core/qunit/odata/type/Decimal.qunit",
		"sap/ui/core/qunit/odata/type/Double.qunit",
		"sap/ui/core/qunit/odata/type/Guid.qunit",
		"sap/ui/core/qunit/odata/type/Int.qunit",
		"sap/ui/core/qunit/odata/type/Int64.qunit",
		"sap/ui/core/qunit/odata/type/ODataType.qunit",
		"sap/ui/core/qunit/odata/type/Raw.qunit",
		"sap/ui/core/qunit/odata/type/Single.qunit",
		"sap/ui/core/qunit/odata/type/Stream.qunit",
		"sap/ui/core/qunit/odata/type/String.qunit",
		"sap/ui/core/qunit/odata/type/Time.qunit",
		"sap/ui/core/qunit/odata/type/TimeOfDay.qunit",
		// OData V2
		// Note: some types use lazy loading and are used by AnnotationHelper tests!
		"sap/ui/core/qunit/odata/AnnotationHelper.qunit",
		"sap/ui/core/qunit/odata/ODataMetaModel.qunit",
		"sap/ui/core/qunit/odata/_AnnotationHelperBasics.qunit",
		"sap/ui/core/qunit/odata/_AnnotationHelperExpression.qunit",
		"sap/ui/core/qunit/odata/_ODataMetaModelUtils.qunit",
		// OData V4
		"sap/ui/core/qunit/internal/ODataV4.qunit",
		// test
		"sap/ui/test/qunit/TestUtils.qunit"
	], function () {
		function start() {
			Core.detachThemeChanged(start);
			QUnit.start();
		}

		if (Core.isThemeApplied()) {
			QUnit.start();
		} else {
			Core.attachThemeChanged(start);
		}
	});
});