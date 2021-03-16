$(document).ready(function() {
	
	var width = screen.width; // Obtiene el tamaño de la pantalla
	var html  = $("#div_cont").html();
	//Para cuando la pantalla sea pequeña
	if(width < 900){
		$("#small").hide();
		$("#little").hide();	
	}
	//Para cuando la pantalla sea grande
	if(width >901){
		$("#little").hide();
	}


	//Detecta si el html de historial esta vacio 


	$("#enviar").click(function (evt) {

	//Se obtiene el texto ingresado para ser mandado a python
	var dic = {cadena :$("#texto").val()};
	$.ajax({
		url:"/gText",
		type:"POST",
  		data : JSON.stringify(dic),
    	contentType: "application/json",

    	success:function(response){

    		var cadena = $("#texto").val();
    		var json = $.parseJSON(response);
    		console.log(json);   		
			

			//Oculta el div que muestra que no se han realizado traducciones
    		$("#tVacio").hide();

			$(".texto2").val(json.t);

			if(width < 900){
				$("#little").show();
			}

			html += '<div class="cont col-11 col-lg-11 shadow-lg bg-white rounded">'
			html +='<li class="trad_or">'+cadena+'</li>'
			html+='<li class="trad">'+json.t+'</li></div>'
			$("#historial").html(html);
			
    	},
    	error:function(response){
    		console.log("Ha sucedido un problema");
    	}

	})
})

});