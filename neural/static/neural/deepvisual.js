              
const labels = ['January', 'February', 'March', 'April'];
const labelsQuant = [10, 40, 80, 50];
const ctx = document.getElementById('bar_exam_canva');
const ctl = document.getElementById('line_exam_canva');
const ctp = document.getElementById('pie_exam_canva');
const ctpl = document.getElementById('polar_pie_exam_canva');
const cts = document.getElementById('scatter_exam_canva');
const clq = document.getElementById('linequant_exam_canva');
const cbq = document.getElementById('bubblequant_exam_canva');
const hsq = document.getElementById('histquant_exam_canva');         
const plotsForSelectionList = ['bar_exam_canva', 'line_exam_canva', 'pie_exam_canva', 'polar_pie_exam_canva'];
const plotsForQuantSelectionList = ['scatter_exam_canva', 'linequant_exam_canva', 'bubblequant_exam_canva', 'histquant_exam_canva'];
const plotsFrequencyObjects = [ctx, ctl, ctp, ctpl];
const plotsQuantitativeObjects = [cts, clq, cbq, hsq];
const chartInfoCopy = JSON.parse(document.getElementById("chart-data").textContent);
const chartElements = document.querySelector("#chart_selector_parent");
const chartSelector = document.getElementById("user-selector"); 
const userSelectorCharts = document.getElementById("user-selector-charts");
const userSelectorChartsQuant = document.getElementById("user-selector-charts-quant");
const chartSelectorQuant = document.getElementById("user-selector-quant"); 
const chartSelectionSign = document.getElementById("Select-Chart-Sign");
const changeDatasetbtn = document.getElementById("change-datasetbtn");
const userChartSelector = document.getElementById('user-chart-selector');
const chartSelectionConst = document.getElementById('Select-Chart-Const');
const changeDatasetbtnQuant = document.getElementById('change-datasetbtn-quant');

const barExampleConfig = {
      type: "bar",
      data: {
      labels: labels,
      datasets: [
                 {
                label: 'Bar Plot',
                data: [65, 59, 80, 81],
                backgroundColor: 'rgb(255, 99, 132)',
                          },
                       ],
                    },
                    options: {
                       animation: false,
                       responsive: true,
                       maintainAspectRatio: true,
                       scales: {
                        y: {
                          beginAtZero: true
                        }
                       },
                      plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      },
                      scales: {
                        xAxes: [
                          {
                            ticks: {
                              maxTicksLimit: 2000
                            }
                          }
                        ]
                      }
                    }
                };
                
                const lineExampleConfig = {
                  type: "line",
                    data: {
                      labels: labels,
                       datasets: [
                          {
                            label: 'Line Plot',
                            data: [65, 59, 80, 81],
                          backgroundColor: 'rgb(255, 99, 132)',
                          },
                       ],
                    },
                    options: {
                       animation: false,
                       responsive: true,
                       maintainAspectRatio: true,
                       scales: {
                        y: {
                          beginAtZero: true
                        }
                       },
                      plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                    }
                };
        
                const pieExampleConfig = {
                  type: "pie",
                    data: {
                      labels: labels,
                       datasets: [
                          {
                            label: 'Pie Plot',
                            data: [65, 59, 80, 81],
                            backgroundColor: [
                              'rgb(255, 99, 132)',
                              'rgb(54, 162, 235)',
                              'rgb(255, 205, 86)',
                              'rgb(0, 255, 255)'
                             ],
                             hoverOffset: 4,       
                          },
                       ],
                    },
                    options: {
                       responsive: true,
                       maintainAspectRatio: true,
                       plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                    }
                };
        
              const polarExampleConfig = {
                  type: "polarArea",
                    data: {
                      labels: labels,
                       datasets: [
                          {
                            label: 'Pie Plot',
                            data: [65, 59, 80, 81],
                            backgroundColor: [
                              'rgb(255, 99, 132)',
                              'rgb(54, 162, 235)',
                              'rgb(255, 205, 86)',
                              'rgb(0, 255, 255)'
                             ],       
                          },
                       ],
                    },
                    options: {
                       responsive: true,
                       maintainAspectRatio: true,
                       plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                    }
                };
        
                //Configurations for numerical plots
        
                const scatterExampleConfig = {
                  type: "scatter",
                    data: {
                      labels: labels,
                       datasets: [
                          {
                            label: 'Scatter Plot',
                            data: [{
                              x: -10,
                              y: 0
                            }, {
                              x: 0,
                              y: 10
                            }, {
                              x: 10,
                              y: 5
                            }, {
                              x: 0.5,
                              y: 5.5
                            }],
                          backgroundColor: 'rgb(255, 99, 132)',
                          },
                       ],
                    },
                    options: {
                       animation: false,
                       responsive: true,
                       scales: {
                        x: {
                          type:'linear',
                          position: 'bottom'
                        }
                       },
                      plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                    }
                };
        
                const lineExampleQuantConfig = {
                  type: "line",
                    data: {
                      labels: labelsQuant,
                       datasets: [
                          {
                            label: 'Line Plot',
                            data: [65, 59, 80, 81],
                          backgroundColor: 'rgb(255, 99, 132)',
                          },
                       ],
                    },
                    options: {
                       animation:false,
                       responsive: true,
                       scales: {
                        y: {
                          beginAtZero: true
                        }
                       },
                      plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                    }
                };
        
                const BubbleChartQuantConfig = {
                  type:'bubble',
                  data: {
                    datasets: [{
                      label: 'Bubble Chart',
                      data: [{
                        x: 20,
                        y: 30,
                        r: 15
                      }, {
                        x: 40,
                        y: 10,
                        r: 10
                      }],
                      backgroundColor: 'rgb(255, 99, 132)' 
                    }]
                  },
                  options: {
                    animation:false,
                    animations: {
                      onComplete: function () {
                      console.log(myChart.toBase64Image('image/jpeg', 1));
                      },
                    },
                    plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          enabled: false
                        }
                      }
                  }
                };
        
              const histogramChartQuantConfig = {
                  type: "bar",
                    data: {
                      labels: labelsQuant,
                       datasets: [
                          {
                            label: 'Histogram Plot',
                            data: [65, 59, 80, 81],
                          backgroundColor: 'rgb(255, 99, 132)',
                          },
                       ],
                    },
                    options: {
                       animation:false,
                       responsive: true,
                       scales: {
                        y: {
                          beginAtZero: true
                        }
                       },
                    plugins: {
                    legend: {
                        display: false
                      },
                    tooltip: {
                        enabled: false
                    }
                   }  
                  }
                };

        //Create the list of configurations
        const configFiles = [barExampleConfig, lineExampleConfig, pieExampleConfig, polarExampleConfig];
        const quantConfigFiles = [scatterExampleConfig, lineExampleQuantConfig, BubbleChartQuantConfig, histogramChartQuantConfig];
        const canvaCharts = document.querySelectorAll(".canva_example");
        const canvaChartsQuand = document.querySelectorAll(".canva_example_quand");
        const chartSelectorMain = document.getElementById("chart-selector-primary");
        var ctx_plot = ctx.getContext('2d');
        var ctl_plot = ctl.getContext('2d');
        var ctp_plot = ctp.getContext('2d');
        var ctpl_plot = ctpl.getContext('2d');
        var cts_plot = cts.getContext('2d');
        var clq_plot = clq.getContext('2d');
        var cbq_plot = cbq.getContext('2d');
        var hsq_plot = hsq.getContext('2d');

        const downloadButton = document.getElementById("download-button");
        const downloadButtonSec = document.getElementById("download-button_sec");
        
        //TO DO: Move to the end of the script later
      function imageDownloader (chart) {
           const a = document.createElement("a");
           setTimeout(() => {
           a.href = chart.toBase64Image('image/png', 1);
           a.download = "My_Image.png";
           a.click();
       }, 500);
      }
      
      function downloadButtonEvent (button, chart, event="click") {
              button.removeEventListener(event, imageDownloader);
               button.addEventListener(event, () => {
                  imageDownloader(chart);
               });
      }

      //Method #2 - Since we know the object chartInfoCopy will never be undefined (due to the backend)
        var chartPicked = '';
        plotsFrequencyObjects.forEach((plot) => {
          plot.addEventListener('click', function(e) {
          e.preventDefault();
          chartPicked = e.target.id; 
          plotsForSelectionList.forEach((chart, index) => {
              chartSelectorMain.style.display = "none";
              if (chartPicked === chart) {
                userChartSelector.style.display = 'flex';
                chartElements.style.display = 'none';
                chartSelectionSign.style.display = "block";
                changeDatasetbtn.style.display = "block";
                chartSelectorQuant.style.display = "none";
                //Only display this chart
                // Check if chart if chartInfoCopy JSON object is not empty, proceed with the rest 
                if (chartInfoCopy) { 
                 //if the data is available, update everything in the chart config
                 var chartMain = document.getElementById('main-chart').getContext('2d');
                 let selectedChartConfig = configFiles[index];
                 selectedChartConfig.data.labels = chartInfoCopy.labels; 
                 selectedChartConfig.data.datasets[0].data = chartInfoCopy.data;
                 window.chart = new Chart(chartMain, selectedChartConfig);
                 downloadButtonEvent(downloadButton, window.chart);
                 //Display the actual canva of each of the other charts which is currently not selected
                 for (canva of canvaCharts) {
                    //Add each canva to the right-side of the main chart
                    //If the chartSelector component has elements remove them 
                    canva.style.cursor = "pointer";
                    canva.style.marginBottom = "30px";
                    if (userSelectorCharts.contains(canva)) {
                       userSelectorCharts.removeChild(canva);
                    }
                    userSelectorCharts.appendChild(canva);
                    //For each canva, add an eventlistener                  
                    canva.addEventListener("click", (e)=>{
                        e.preventDefault();
                        let id = e.target.id;
                        //For each id of the charts list, update the main chart
                        plotsForSelectionList.forEach((chart, i) =>{
                           if (chart === id) {
                              let selectedChartConfig = configFiles[i];
                              //Activate all tooltips and animations
                              selectedChartConfig.options.plugins.legend.display = true;
                              selectedChartConfig.options.plugins.tooltip.enabled = true;
                              selectedChartConfig.data.labels = chartInfoCopy.labels; 
                              selectedChartConfig.data.datasets[0].data = chartInfoCopy.data; 
                              window.chart.destroy();
                              window.chart = new Chart(chartMain, selectedChartConfig);
                              downloadButtonEvent(downloadButton, window.chart);
                           }
                        });
                    });
                 }     
                } //End of main object if statement
                else {
                  window.location.href = "/neural/file_uploader/"; 
                }
              } 
              else { //Check if this else statement makes logical sense
                plotsFrequencyObjects[index].style.display = "block";
              }
          });
        });     
      });

      let chartPickedQuant = ''
      plotsQuantitativeObjects.forEach((plotSec) => {
        plotSec.addEventListener('click', function(e) {
          chartPickedQuant = e.target.id; 
          plotsForQuantSelectionList.forEach((chart, index) => {
              if (chartPickedQuant === chart) {
                chartSelectorMain.style.display = "none";
                userChartSelector.style.display = 'flex';
                chartElements.style.display = 'none';
                chartSelectionConst.style.display = "block";
                changeDatasetbtnQuant.style.display = "block";
                //Also remove the frequency charts from selection
                chartSelector.style.display = "none";
                // Then check if the data for this chart is empty or not, if so, redirect user to fill the data
                if (chartInfoCopy) {   
                 //if the data is available, update everything in the chart config
                 var chartMain = document.getElementById('main-chart').getContext('2d');
                 let selectedChartConfigQuant = quantConfigFiles[index];
                 selectedChartConfigQuant.data.labels = chartInfoCopy.labels; 
                 selectedChartConfigQuant.data.datasets[0].data = chartInfoCopy.data; 
                 window.chart = new Chart(chartMain, selectedChartConfigQuant);  
                 downloadButtonEvent(downloadButtonSec, window.chart);
                 //Display the actual canva of each of the other charts which is currently not selected
                 for (canva of canvaChartsQuand) {
                    //Add each canva to the right-side of the main chart
                    //If the chartSelector component has elements remove them 
                    canva.style.cursor = "pointer";
                    if (userSelectorChartsQuant.contains(canva)) {
                       userSelectorChartsQuant.removeChild(canva);
                    }
                    userSelectorChartsQuant.appendChild(canva);
                    //For each canva, add an eventlistener                  
                    canva.addEventListener("click", (e)=>{
                        e.preventDefault();
                        let id = e.target.id;
                        //For each id of the charts list, update the main chart
                        plotsForQuantSelectionList.forEach((chart, i) =>{
                           if (chart === id) {
                              window.chart.destroy();
                              let selectedChartConfigQuant = quantConfigFiles[i];
                              selectedChartConfigQuant.options.plugins.legend.display = true;
                              selectedChartConfigQuant.options.plugins.tooltip.enabled = true;
                              selectedChartConfigQuant.data.labels = chartInfoCopy.labels; 
                              selectedChartConfigQuant.data.datasets[0].data = chartInfoCopy.data; 
                              window.chart = new Chart(chartMain, selectedChartConfigQuant);
                              downloadButtonEvent(downloadButtonSec, window.chart);
                           }
                        });
                    });
                 }     
                } else {
                  //Create a new form for numerical data only to fix bugs
                  window.location.href = "/neural/file_uploader/"; 
                }
              } 
              else { //Check if this else statement makes logical sense
                plotsQuantitativeObjects[index].style.display = "block";
              }
          });
        });     
      });

      //Add an event listener to the change dataset button
    changeDatasetbtn.addEventListener("click", ()=> {
          window.location.href = "/neural/file_uploader/"; 
      });

    changeDatasetbtnQuant.addEventListener("click", ()=> {
          window.location.href = "/neural/file_uploader/"; 
      }); 

    chartSelectionSign.addEventListener("click", () => {
         //Add a timeout before changing screens
        window.location.href = "/neural/file_uploader/deep_visual/";
    });

    chartSelectionConst.addEventListener("click", () =>{
         window.location.href = "/neural/file_uploader/deep_visual/";
    });   

 window.onload = function() {
      ctx_plot;
      ctl_plot;
      ctp_plot;
      ctpl_plot;
      cts_plot;
      clq_plot;
      cbq_plot;
      hsq_plot;
      new Chart(ctx_plot, barExampleConfig);
      new Chart(ctl_plot, lineExampleConfig);
      new Chart(ctp_plot, pieExampleConfig);
      new Chart(ctpl_plot, polarExampleConfig);

      new Chart(cts_plot, scatterExampleConfig);
      new Chart(clq_plot, lineExampleQuantConfig);
      new Chart(cbq_plot, BubbleChartQuantConfig);
      new Chart(hsq_plot, histogramChartQuantConfig);          
};
