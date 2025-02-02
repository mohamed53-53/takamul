/** @odoo-module **/

import AbstractAction from "web.AbstractAction";
import { action_registry, qweb, _lt } from "web.core";
import framework from "web.framework";
import session from "web.session";

const kpiHistoryWidget = AbstractAction.extend({
    template: "kpi.scorecard.report",
    hasControlPanel: true,
    loadControlPanel: true,
    withSearchBar: true,
    searchMenuTypes: ["filter", "favorite"],
    jsLibs: [
        "/kpi_scorecard/static/lib/jstree/jstree.js",
        "/web/static/lib/Chart/Chart.js",
    ],
    cssLibs: [
        "/kpi_scorecard/static/lib/jstree/themes/default/style.css",
    ],
    /*
     * @override to initialize our own action
    */
    init(parent, action, options={}) {
        this._super(...arguments);
        this.action = action;
        this.actionManager = parent;
        this.searchModelConfig.modelName = "kpi.scorecard.line";
        this.options = options;
        this.searchDomain = [];
        this.kpiTargets = {};
        this.kpiChartType = "line";
        this.kpiPeriodType = false;
        this.kpiCategories = [];
        this.showKPItargets = true;
        this.showKPIactual = true;
    },    
    /**
     * @override to render targets graph at the first initiation
    */
    async start() {
        await this._super(...arguments);
        this.kpiScreen = this.$el.find(".kpi_report_screen")[0];
        this.kpiPeriodsNav = this.$el.find("#kpi_periods")[0];
        await this._renderNavigationPanel();
        await this._refreshKPIs();
        this.$el.on("change", "#kpi_period", ev => this._onChangePeriodType(ev));
        this.$el.on("click", "#clear_kpi_categories", ev => this._onClearCategories(ev));
        this.$el.on("change", "#kpi_show_targets", ev => this._onChangeShowTargets(ev));
        this.$el.on("change", "#kpi_show_actual", ev => this._onChangeShowActual(ev));
        this.$el.on("change", "#kpi_graph_type", ev => this._onChangeGraphType(ev));
        this.$el.on("click", ".kpi_expand_graph", ev => this._onClickExpandGraph(ev));
        this.$el.on("click", ".kpi_change_graph_type_to_bar", ev => this._onClickChangeGraphTypeBar(ev));
        this.$el.on("click", ".kpi_change_graph_type_to_line", ev => this._onClickChangeGraphTypeLine(ev));
    },
    /**
     * @override to trigger KPI refreshing
    */
    _onSearch: function(searchQuery) {
        this.searchDomain = searchQuery.domain;
        this._refreshKPIs();
    },
    /*
     * The method to render left navigation panel
    */
    async _renderNavigationPanel() {
        var scrollTop = this.$(".kpi-kanban-navigation").scrollTop();        
        await this._renderPeriods();
        await this._renderCategories()
        this.$(".kpi-kanban-navigation").scrollTop(scrollTop || 0);
    },
    /*
     * The method to render period type selection
    */
    async _renderPeriods() {
        var self = this;
        var periodsDict = await self._rpc({
            model: "kpi.period",
            method: "action_return_period_types",
            args: [],
        });
        this.kpiPeriodType = periodsDict.this_period;
        this.kpiPeriodsNav.innerHTML = qweb.render("kpi.report.navigation.periods", periodsDict);       
    },
    /*
     * The method triggered when period type is selected
    */
    _onChangePeriodType: function(ev) {
        this.kpiPeriodType = parseInt(this.$("#kpi_period")[0].value,10);
        this._refreshKPIs();
    },
    /*
     * The method to render jstree of categories
    */
    async _renderCategories() {
        var self = this;
        this.$("#kpi_report_categories").jstree("destroy");
        var kpiCategories = await this._rpc({
            model: "kpi.category",
            method: "action_return_nodes",
            args: [],
        });
        var jsTreeOptions = {
            "core" : {
                "themes": {"icons": false},
                "check_callback" : true,
                "data": kpiCategories,
                "multiple" : true,
            },
            "plugins" : [
                "checkbox",
                "state",
                "search",
            ],
            "state" : { "key" : "kpi_categories" },
            "checkbox" : {
                "three_state" : false,
                "cascade": "down",
                "tie_selection" : false,
            },
        };
        var ref = this.$("#kpi_report_categories").jstree(jsTreeOptions);
        this.$("#kpi_report_categories").on("state_ready.jstree", self, function (event, data) {
            self._selectCategories()
            // We register "checks" only after restoring the tree to avoid multiple checked events
            self.$("#kpi_report_categories").on("check_node.jstree uncheck_node.jstree", self, function (event, data) {
                self._selectCategories();
            })
        });
    },
    /**
    * The method to update chosen categories
    */
    _selectCategories: function() {
        var checkedCategoriesIDS = [];
        var refS = this.$("#kpi_report_categories").jstree(true);
        if (refS) {
            var checkedCategories = refS.get_checked();
            checkedCategoriesIDS = checkedCategories.map(function(item) {
                return parseInt(item, 10);
            });
        };
        this.kpiCategories = checkedCategoriesIDS; 
        this._refreshKPIs();     
    },
    /*
     * The method clear all checked sections
    */
    _onClearCategories: function(event) {
        var ref = this.$("#kpi_report_categories").jstree(true);
        ref.uncheck_all();
        ref.save_state();
        this._selectCategories();
    },
    /**
    * The method to hide/show target values
    */
    _onChangeShowTargets: function(event) {
        this.showKPItargets = this.$("#kpi_show_targets")[0].checked;
        this._changeChartDatasets();
    },
    /**
    * The method to hide/show planned values
    */
    _onChangeShowActual: function(event) {
        this.showKPIactual = this.$("#kpi_show_actual")[0].checked;
        this._changeChartDatasets();
    },
    /**
    * The method to trigger data (targets/actual) updated
    */
    _changeChartDatasets: function() {
        var self = this;
        _.each($("canvas.kpi_canvas"), function (kpiCanvas) {
            var chartDataKey;
            var kpiID = kpiCanvas.id;
            var kpiChartType = self.$(".kpi_change_graph_type_to_line#"+kpiID).hasClass("kpi_icon_not_active") ? "line" : "bar";

            if (kpiChartType == "bar") {
                chartDataKey = "barsDataSet";
                if (self.showKPIactual && !self.showKPItargets) {
                    chartDataKey = "barsDataSetActual";
                }
                else if (!self.showKPIactual && self.showKPItargets) {
                    chartDataKey = "barsDataSetTargets";
                }
            }
            else {
                chartDataKey = "lineDataSet";
                if (self.showKPIactual && !self.showKPItargets) {
                    chartDataKey = "lineDataSetActual";
                }
                else if (!self.showKPIactual && self.showKPItargets) {
                    chartDataKey = "lineDataSetTargets";
                }
            };
            var kpiChart = $(kpiCanvas).data("kpiChart");
            if (kpiChart) {
                kpiChart.data.datasets = $(kpiCanvas).data(chartDataKey);
                kpiChart.update();
            };
        });
    },
    /**
    * The method to change graph type
    */
    _onChangeGraphType: function(event) {
        this.kpiChartType = this.$("#kpi_graph_type")[0].value;
        $(".kpi_change_graph_type_to_"+this.kpiChartType+":not([kpi_icon_not_active])").click();
    },
    /**
     * The method to render KPIs view
    */
    async _refreshKPIs() {
        var self = this;
        if (this.showKPItargets || this.showKPIactual) {
            this.kpiTargets = await this._rpc({
                model: "kpi.scorecard.line",
                method: "action_get_targets_history",
                args: [this.searchDomain, this.kpiCategories, this.kpiPeriodType],
            });
            this.kpiScreen.innerHTML = qweb.render(
                "kpi.report.screen", 
                {"kpiTargets": this.kpiTargets, "kpiChartType": this.kpiChartType,},
            );
            _.each(this.kpiTargets, function (kpiTar) {
                self._activateChart(kpiTar.kpi_id, kpiTar.targets, kpiTar.kpi_order);
            });
        }
        else {
            this.kpiScreen.innerHTML = qweb.render(
                "kpi.report.screen", 
                {"kpiTargets": [], "kpiChartType": this.kpiChartType,},
            );
        }
    },
    /**
     * The method to render chart for each specific KPI
    */
    _activateChart: function(targetID, bars, kpiOrder) {
        var data = [];
        var labels = [];
        var backgroud_colors = [];
        var target_data = [];
        var barsDataSet = [];
        var barsDataSetTargets = {};
        var barsDataSetActual = {};

        var lineDataSet = [];
        var lineDataSetTargets = [];
        var lineDataSetActual = [];
        
        bars.forEach(function (pt) {
            labels.push(pt.date);
            data.push(pt.value);
            target_data.push(pt.target_value);
            backgroud_colors.push(pt.background);
        });

        // bar data sets
        barsDataSetActual = {
            data: data,
            fill: "start",
            label: _lt("Actual"),
            backgroundColor: backgroud_colors,                   
        };
        barsDataSetTargets = {
            data: target_data,
            fill: "start",
            label: _lt("Target"),
            backgroundColor: "#0180a5",                   
        };
        if (this.showKPIactual) {
            barsDataSet.push(barsDataSetActual);
        };
        if (this.showKPItargets) {
            barsDataSet.push(barsDataSetTargets);
        };
        // line data sets
        lineDataSetActual = {
            data: data,
            fill: "start",
            label: _lt("Actual"),
            backgroundColor: "#0180a5",                
        };
        lineDataSetTargets = {
            data: target_data,
            fill: "start",
            label: _lt("Target"),
            backgroundColor: "#0180a5",                    
        };     
        // have to check everything again, since colors differ for different options
        if (kpiOrder) {
            lineDataSet = [
                {
                    data: data,
                    fill: "start",
                    label: _lt("Actual"),
                    backgroundColor: "rgb(0, 136, 24, 0.7)" ,
                },
                {
                    data: target_data,
                    fill: "start",
                    label: _lt("Target"),
                    backgroundColor: "rgb(210, 63, 58)",                      
                },
            ];
        }
        else {
            lineDataSet = [
                {
                    data: target_data,
                    fill: "start",
                    label: _lt("Target"),
                    backgroundColor: "rgb(0, 136, 24, 0.7)",                     
                },
                {
                    data: data,
                    fill: "start",
                    label: _lt("Actual"),
                    backgroundColor: "rgb(210, 63, 58)", 
                }
            ];
        };

        var config = {
            type: this.kpiChartType,
            data: {
                labels: labels,
                datasets: this.kpiChartType == "bar" ? barsDataSet : lineDataSet,
            },
            options: {
                maintainAspectRatio: false,
                responsive: true,
                scales: {
                    xAxes: [{
                        offset: this.kpiChartType == "bar" ? true : false,
                    }],
                }
            },
        };
        var kpiCanvas = this.$(".kpi_canvas#kpi_" + targetID);
        var context = kpiCanvas[0].getContext("2d");
        var kpiChart = new Chart(context, config);
        kpiCanvas.data("kpiChart", kpiChart);
        kpiCanvas.data("barsDataSet", barsDataSet);
        kpiCanvas.data("barsDataSetActual", [barsDataSetActual]);
        kpiCanvas.data("barsDataSetTargets", [barsDataSetTargets]);
        kpiCanvas.data("lineDataSet", lineDataSet);
        kpiCanvas.data("lineDataSetActual", [lineDataSetActual]);
        kpiCanvas.data("lineDataSetTargets", [lineDataSetTargets]);
    },
    /**
     * The method to open a specific KPI to the full view
     */
    _onClickExpandGraph(ev) {
        var kpiID = ev.currentTarget.id;
        var currentCanvasDiv = this.$el.find(".kpi_report_item#"+kpiID);
        if (currentCanvasDiv.hasClass("kpi_report_item_full_screen")) {
            currentCanvasDiv.removeClass("kpi_report_item_full_screen");
            currentCanvasDiv.addClass("kpi_report_item_normal");
        }
        else {
            currentCanvasDiv.addClass("kpi_report_item_full_screen");
            currentCanvasDiv.removeClass("kpi_report_item_normal");
        };
        var kpiChart = $(".kpi_canvas#" + kpiID).data('kpiChart');
        kpiChart.resize();
    },
    /**
     * The method to change to bar type
     */
    _onClickChangeGraphTypeBar(ev) {
        var chartDataKey = "barsDataSet";
        if (this.showKPIactual && !this.showKPItargets) {
            chartDataKey = "barsDataSetActual";
        }
        else if (!this.showKPIactual && this.showKPItargets) {
            chartDataKey = "barsDataSetTargets";
        }
        this._changeSpecificChartType(ev, "bar", chartDataKey);    
    },    
    /**
     * The method to change to line type
     */
    _onClickChangeGraphTypeLine(ev) {
        var chartDataKey = "lineDataSet";
        if (this.showKPIactual && !this.showKPItargets) {
            chartDataKey = "lineDataSetActual";
        }
        else if (!this.showKPIactual && this.showKPItargets) {
            chartDataKey = "lineDataSetTargets";
        };
        this._changeSpecificChartType(ev, "line", chartDataKey);
    }, 
    /**
    * Basic method to adapt chart
    */
    _changeSpecificChartType(ev, newChartType, dataSetKey) {
        if (!$(ev.currentTarget).hasClass("kpi_icon_not_active")) {
            var kpiID = ev.currentTarget.id;
            $(".kpi_change_graph_type#" + kpiID).removeClass("kpi_icon_not_active");
            $(ev.currentTarget).addClass("kpi_icon_not_active");           
            var kpiCanvas = $(".kpi_canvas#" + kpiID);
            var kpiChart = kpiCanvas.data("kpiChart");
            kpiChart.config.type = newChartType;
            kpiChart.data.datasets = kpiCanvas.data(dataSetKey);
            kpiChart.options.scales = {
                xAxes: [{
                    offset: newChartType == "bar" ? true : false,
                }],
            }
            kpiChart.update();
        };
    },
});

action_registry.add("kpi.scorecard.report", kpiHistoryWidget);

export default kpiHistoryWidget;
