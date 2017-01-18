var app = angular.module('plunker', ['nvd3', 'smart-table']);

app.controller('MainCtrl', function($scope, $http) {

  sc = $scope
  $scope.filters = {date:"",
    checkbox:{morepodiy:false, afisha:false,dou:false}
  };
  $scope.chartOptions = {
            chart: {
                type: 'historicalBarChart',
                height: 450,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 65,
                    left: 50
                },
                x: function(d){return d[0];},
                y: function(d){return d[1];},
                showValues: true,
                valueFormat: function(d){
                    return d3.format(',.1f')(d);
                },
                duration: 100,
                xAxis: {
                    axisLabel: 'X Axis',
                    tickFormat: function(d) {
                        return d3.time.format('%x')(new Date(d));
                    },
                    rotateLabels: 30,
                    showMaxMin: false
                },
                yAxis: {
                    axisLabel: 'Y Axis',
                    axisLabelDistance: -10,
                    tickFormat: function(d){
                        return d3.format('.2')(d);
                    }
                },
                tooltip: {
                    keyFormatter: function(d) {
                        return d3.time.format('%x')(new Date(d));
                    }
                },
                zoom: {
                    enabled: true,
                    scaleExtent: [1, 10],
                    useFixedDomain: false,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: true,
                    unzoomEventType: 'dblclick.zoom'
                },
                bars: {
                  dispatch: {
                    //chartClick: function(e) {console.log("! chart Click !")},
                    elementClick: function(e) {
                      var dt = new Date(e.data[0])
                      $scope.filters.date = dt.toISOString().substring(0, 10);
                      $scope.$apply();
                      },
                  }
                },
                //callback: function(e){console.log('! callback !')}
            }
        };

$scope.eventData = {objects:[], num_results:0};
$scope.eventDataFiltered = {objects:[], num_results:0};


        $http({
          method: 'GET',
          url: '/api/events?q={"filters":[{"name":"start_date","op":"ge","val":"2016-01-01"},{"name":"start_date","op":"le","val":"2017-01-01"}]}'
        }).then(function successCallback(response) {
          $scope.eventData = response.data;
          $scope.filters.checkbox = {morepodiy:true, afisha:true,dou:true};
            // this callback will be called asynchronously
            // when the response is available
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
          });
          
          
        $scope.dataValues = {
                "key" : "Quantity" ,
                "bar": true,
                "values" : [[1451606400000, 0], [1483228800000, 0]]
            };
        $scope.chartData = [$scope.dataValues];

        $scope.$watch('filters', function(newValue, oldValue){

          var filtered = _.filter($scope.eventData.objects, function(item){
            return _.some(newValue.checkbox, function(value, key){
              if (item.source == key && value === true) {return true}
            });
          });

          if (filtered.length){
            values = _.map(
              _.countBy(filtered, 'start_date'),
              function(value, key){
                return [Date.parse(key),value];
              });
            $scope.chartData[0].values = values;
          } else {
            $scope.chartData[0].values = $scope.dataValues.values;
          }

          filtered = _.filter(filtered, function(item){
            if (item.start_date == newValue.date || newValue.date == ""){ return true}
          });

          $scope.eventDataFiltered.objects = filtered;


        },true);
});

