	$(function() {
		// meter_title, chisizm		
		var updateInterval = 15000;
		var oReq = new XMLHttpRequest();
		var response;
		var param = 2; // чтобы температура отображалась первой
		var chizm = 400;
		var critic = 637;
		var param_a=1;
		var param_b=2;
		var param_c=3;
		var cow_name="NoName";
		var chizm=100;
		var legendContainer = document.getElementById("legendContainer");
	        var legendSettings = {
				position: "nw",
                		show: true,
		                noColumns: 2,
 		                container: legendContainer
			        };		

		
		function getSyncScriptParams() {
  			 var scripts = document.getElementsByTagName('script');
		         var lastScript = scripts[scripts.length-1];
		         var scriptName = lastScript;
			 cow_name = scriptName.getAttribute('param_a'),
		         chizm = scriptName.getAttribute('param_b')			 
	         return param_a       		     		         
		 }		

		getSyncScriptParams();			

		function getData(){
			// alert('getData');
			oReq.open("GET", "http://192.168.1.49:8000/my_data?login=00001&meter_title="+cow_name+"&chisizm="+String(chizm)+"&param="+String(param));
			
			oReq.responseType = 'json';
			oReq.send();
			oReq.onload = alertContents;
		}


		function alertContents() {
			 // alert('oReq.readyState = ');
			 // alert(oReq.readyState);
			 // alert('cow_name=')
			 // alert(cow_name)
			if (cow_name == 'Mumuka') {			
				critic = 637;
			}
			if (cow_name == 'Francheska') {			
				critic = 141.5;
			}
			if (cow_name == 'Yarushka') {			
				critic = 62.5;
			}
			if (cow_name == 'Vestka') {			
				critic = 26.7;
			}


 		 if (oReq.readyState == XMLHttpRequest.DONE) {
 		 	  // alert(oReq.status);
    		if (oReq.status == 200) {
      			response = oReq.response;
      			var d1 = [];
				var d2 = [];
				var d3 = [];
				var d4 = [];
				var d5 = [];
				var d6 = [];

				for (var i = 0; i < chizm; ++i) {
					d1.push([i, response[i]]);
					d2.push([i, 32.5]);					
				}

				for (var i = chizm; i < 2*chizm; ++i) {
					d3.push([i-chizm, response[i]]);
					d4.push([i-chizm, 63.5]);
				}

				for (var i = 2*chizm; i < 3*chizm; ++i) {
					d5.push([i-2*chizm, response[i]]);
					d6.push([i-2*chizm, critic]);
				}
				 data1 = [ d1, d2 ];
				 
				 $.plot("#placeholder",  data1);
				 $.plot("#placeholder_2", [ d3, d4 ], {color: "red"});
				 $.plot("#placeholder_3", [ d5, d6 ]);

    		} else {
      			alert('There was a problem with the request.');
    		}
  		}
  			// alert('There was a problem with XMLHttpRequest.DONE.');
		}


		$("#footer").prepend("Sensors on-line " + " &ndash; ");
		;


		function update() {
			++param;
			getData();
			setTimeout(update, updateInterval);
		}

		update();
		// getData();
		// setInterval(getData, updateInterval);

	});