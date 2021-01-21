$(document).ready(function() {
	
	var height = $(window).height(); // Obtiene el tamaño de la pantalal
	$('section').height(height);




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
    			$("#texto2").val(json.t);
        	},
        	error:function(response){
        		console.log("Ha sucedido un problema");
        	}

		})
	})
});