$(document).ready(function() {
	
	var width = screen.width; // Obtiene el tamaño de la pantalla
	
	//Para cuando la pantalla sea pequeña
	if(width < 900){
		$("#small").hide();
		$("#little").hide();	
	}
	//Para cuando la pantalla sea grande
	if(width >901){
		$("#little").hide();
	}
	$("#enviar").click(function (evt) {

	//Se obtiene el texto ingresado para ser mandado a python
	var dic = {cadena :$("#texto").val()};
	$.ajax({
		url:"/gText",
		type:"POST",
  		data : JSON.stringify(dic),
    	contentType: "application/json",

    	success:function(response){
    		var json = $.parseJSON(response);
    		console.log(json);   		
			$(".texto2").val(json.t);
			$("#little").show();
    	},
    	error:function(response){
    		console.log("Ha sucedido un problema");
    	}

	})
})

});